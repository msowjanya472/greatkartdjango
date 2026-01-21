# PayPal Integration Setup Guide

This guide will help you set up PayPal payment integration for your Greatkart e-commerce application.

## Step 1: Create a PayPal Business Account

1. Go to [PayPal Developer](https://developer.paypal.com/)
2. Sign up or log in with your PayPal business account
3. Navigate to **Dashboard** > **My Apps & Credentials**

## Step 2: Create a PayPal App

1. Click **Create App** (or use an existing app)
2. Fill in the app details:
   - **App Name**: Greatkart (or your preferred name)
   - **Merchant**: Select your business account
3. Click **Create App**

## Step 3: Get Your PayPal Credentials

After creating the app, you'll see:
- **Client ID** (for sandbox or live)
- **Secret** (for sandbox or live)

**For Testing (Sandbox Mode):**
- Use the **Sandbox** Client ID and Secret
- Test with PayPal sandbox accounts

**For Production (Live Mode):**
- Use the **Live** Client ID and Secret
- Requires PayPal business account approval

## Step 4: Configure Settings

Open `greatkart/settings.py` and update the PayPal settings:

```python
# PayPal Settings
PAYPAL_CLIENT_ID = 'YOUR_SANDBOX_CLIENT_ID'  # Replace with your PayPal Client ID
PAYPAL_SECRET = 'YOUR_SANDBOX_SECRET'  # Replace with your PayPal Secret
PAYPAL_MODE = 'sandbox'  # Use 'sandbox' for testing, 'live' for production
```

**Important:** 
- For testing, use sandbox credentials and set `PAYPAL_MODE = 'sandbox'`
- For production, use live credentials and set `PAYPAL_MODE = 'live'`
- Never commit your PayPal credentials to version control!

## Step 5: Test the Integration

1. Start your Django server: `python manage.py runserver`
2. Add items to cart
3. Go through checkout process
4. On the payment page, you'll see the PayPal button
5. Click the PayPal button to test the payment flow

### Testing with Sandbox Accounts

1. Go to [PayPal Sandbox](https://developer.paypal.com/dashboard/accounts)
2. Create test buyer and seller accounts
3. Use the buyer account email to test payments
4. Use the seller account to receive test payments

## How It Works

1. **Place Order**: Customer fills out order form and clicks "Place Order"
2. **Payment Page**: Customer is redirected to payment page with PayPal button
3. **PayPal Payment**: Customer clicks PayPal button and completes payment on PayPal
4. **Payment Processing**: After successful payment, order is marked as paid
5. **Order Complete**: Customer is redirected to order confirmation page
6. **Cart Cleared**: Cart items are moved to OrderProduct and cart is cleared

## Features Implemented

✅ PayPal JavaScript SDK integration
✅ Secure payment processing
✅ Order creation and tracking
✅ Payment record storage
✅ Cart to order conversion
✅ Stock management (reduces product stock after order)
✅ Order completion page
✅ Error handling

## Security Notes

- Always use HTTPS in production
- Store PayPal credentials securely (use environment variables)
- Never expose your PayPal Secret in client-side code
- Test thoroughly in sandbox mode before going live

## Troubleshooting

**PayPal button not showing:**
- Check that your PayPal Client ID is correctly set in settings.py
- Verify the PayPal SDK script is loading (check browser console)

**Payment not processing:**
- Check browser console for JavaScript errors
- Verify your PayPal credentials are correct
- Ensure you're using the correct mode (sandbox/live)

**Order not completing:**
- Check Django server logs for errors
- Verify database migrations are applied
- Check that all required models are properly set up

## Support

For PayPal API issues, visit: https://developer.paypal.com/docs/
For Django issues, visit: https://docs.djangoproject.com/
