from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from carts.models import CartItem
from .models import Order, Payment, OrderProduct
from .forms import OrderForm
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@login_required
def payments(request, order_number):
    """Display payment page with order details"""
    order = get_object_or_404(
        Order,
        user=request.user,
        order_number=order_number,
        is_ordered=False
    )

    # Get cart items for display
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculate totals
    total = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)

    tax = order.tax
    grand_total = order.order_total

    context = {
        'order': order,
        'cart_items': cart_items,
        'total': f"{total:.2f}",
        'tax': f"{tax:.2f}",
        'grand_total': f"{grand_total:.2f}",
    }
    return render(request, 'orders/payments.html', context)

#
#    if request.method == 'GET':
#        # Display payment page
#        if order_number:
#            try:
#                order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
#                cart_items = CartItem.objects.filter(user=request.user)
#                total = 0
#                for cart_item in cart_items:
#                    total += (cart_item.product.price * cart_item.quantity)
#                tax = order.tax
#                grand_total = order.order_total
#
#                context = {
#                    'order': order,
#                    'cart_items': cart_items,
#                    'total': total,
#                    'tax': tax,
#                    'grand_total': f"{order.order_total:.2f}",
#                }
#                return render(request, 'orders/payments.html', context)
#            except Order.DoesNotExist:
#                return redirect('store')
#        else:
#            return redirect('store')
#
#    return redirect('store')
#
@csrf_exempt
@require_POST
@login_required
def payment_complete(request):
    try:
        body = json.loads(request.body)
        order_number = body.get('orderID')
        trans_id = body.get('transID')
        payment_method = body.get('payment_method', 'PayPal')
        status = body.get('status')

        # Get the order
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

        # Store transaction details inside Payment model
        payment = Payment(
            user=request.user,
            payment_id=trans_id,
            payment_method=payment_method,
            amount_paid=str(order.order_total),
            status=status,
        )
        payment.save()

        # Link payment to order
        order.payment = payment
        order.is_ordered = True
        order.status = 'COMPLETED'
        order.save()

        # Move cart items to OrderProduct table
        cart_items = CartItem.objects.filter(user=request.user)

        for cart_item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order = order
            orderproduct.payment = payment
            orderproduct.user = request.user
            orderproduct.product = cart_item.product
            orderproduct.quantity = cart_item.quantity
            orderproduct.product_price = cart_item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # Add variations if any
            cart_item_variations = cart_item.variations.all()
            orderproduct.variations.set(cart_item_variations)
            orderproduct.save()

            # Reduce the quantity of sold products
            product = Product.objects.get(id=cart_item.product.id)
            product.stock -= cart_item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

        # Send order recieved email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()


        # Send order number and transaction id back to sendData() via JsonResponse
        data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'status': 'success',
        }
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def place_order(request, total=0, quantity=0):
    current_user = request.user

    # if the cart count is less than or equal to zero, redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    total = 0
    quantity = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20260113
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # Redirect to payments page with order number
            return redirect('payments', order_number=data.order_number)
    else:
        return redirect('checkout')

@login_required
def order_complete(request):

    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True, user=request.user)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for item in ordered_products:
            subtotal += item.product_price * item.quantity

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': transID,
            'subtotal': f"{subtotal:.2f}",
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
