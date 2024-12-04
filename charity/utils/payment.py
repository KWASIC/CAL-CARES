import requests
from django.conf import settings
from decimal import Decimal

class PaystackAPI:
    def __init__(self):
        self.api_key = settings.PAYSTACK_SECRET_KEY
        self.base_url = "https://api.paystack.co"
        
    def initialize_payment(self, email, amount, reference=None, callback_url=None):
        """Initialize a payment transaction
        
        Args:
            email: Customer's email
            amount: Amount in Naira (will be converted to kobo)
            reference: Unique transaction reference
            callback_url: URL to redirect to after payment
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Convert amount to kobo (multiply by 100)
        amount_in_kobo = int(Decimal(str(amount)) * 100)
        
        data = {
            "email": email,
            "amount": amount_in_kobo,
            "currency": "NGN",
            "callback_url": callback_url,
            "channels": ["card", "bank", "ussd", "qr", "mobile_money", "bank_transfer"]
        }
        
        if reference:
            data["reference"] = reference
            
        try:
            response = requests.post(
                f"{self.base_url}/transaction/initialize",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Paystack API Error: {str(e)}")
            if hasattr(e.response, 'json'):
                print(f"Paystack Error Response: {e.response.json()}")
            raise Exception(f"Payment initialization failed: {str(e)}")
            
    def verify_payment(self, reference):
        """Verify a payment transaction"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/transaction/verify/{reference}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Paystack API Error: {str(e)}")
            if hasattr(e.response, 'json'):
                print(f"Paystack Error Response: {e.response.json()}")
            raise Exception(f"Payment verification failed: {str(e)}")
            
    def get_payment_url(self, email, amount, reference=None, callback_url=None):
        """Get payment URL for redirect"""
        response = self.initialize_payment(email, amount, reference, callback_url)
        if response.get('status'):
            return response['data']['authorization_url']
        raise Exception("Could not get payment URL")
