from django.conf import settings

def paypal_settings(request):
    """Context processor to pass PayPal settings to templates"""
    return {
        'PAYPAL_CLIENT_ID': getattr(settings, 'PAYPAL_CLIENT_ID', 'YOUR_PAYPAL_CLIENT_ID'),
        'PAYPAL_MODE': getattr(settings, 'PAYPAL_MODE', 'sandbox'),
    }
