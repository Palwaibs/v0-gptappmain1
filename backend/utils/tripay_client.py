import os
import hmac
import hashlib
import json
import requests
import logging
from datetime import datetime
from flask import current_app

logger = logging.getLogger(__name__)

class TripayClient:
    def __init__(self):
        self.api_key = current_app.config.get('TRIPAY_API_KEY')
        self.merchant_code = current_app.config.get('TRIPAY_MERCHANT_CODE')
        self.private_key = current_app.config.get('TRIPAY_PRIVATE_KEY')
        self.is_production = current_app.config.get('TRIPAY_IS_PRODUCTION', False)
        self.base_url = current_app.config.get('TRIPAY_BASE_URL', 'https://tripay.co.id/api')
        self.callback_url = current_app.config.get('TRIPAY_CALLBACK_URL')
        
        if not all([self.api_key, self.merchant_code, self.private_key]):
            logger.error("Tripay credentials not properly configured")
            raise ValueError("Missing Tripay credentials in configuration")
    
    def _build_signature(self, merchant_ref, amount):
        """
        Build signature for Tripay transaction creation
        Formula: HMAC-SHA256(key=TRIPAY_PRIVATE_KEY, message=TRIPAY_MERCHANT_CODE + merchant_ref + amount)
        """
        try:
            message = str(self.merchant_code) + str(merchant_ref) + str(amount)
            signature = hmac.new(
                self.private_key.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            logger.info(f"Generated signature for merchant_ref: {merchant_ref}, amount: {amount}")
            return signature
            
        except Exception as e:
            logger.error(f"Error generating signature: {str(e)}")
            return ""
    
    def create_transaction(self, order_dict, method="QRIS"):
        """
        Create transaction with Tripay
        
        Args:
            order_dict (dict): Order information containing:
                - merchant_ref: unique order identifier
                - amount: transaction amount
                - customer_email: customer email
                - customer_name: customer name (optional)
                - phone_number: customer phone (optional)
            method (str): Payment method (QRIS, BRIVA, BNIVA, etc.)
        
        Returns:
            dict: Transaction result with success, checkout_url, reference, etc.
        """
        try:
            # Build URLs
            api_base_url = current_app.config.get('API_BASE_URL', 'http://localhost:5000')
            callback_url = self.callback_url or f"{api_base_url}/callback/tripay"
            return_url = f"{current_app.config.get('FRONTEND_URL', api_base_url)}/confirmation?order_id={order_dict['merchant_ref']}"
            
            # Generate signature
            signature = self._build_signature(order_dict['merchant_ref'], order_dict['amount'])
            
            # Prepare request payload
            payload = {
                'method': method,
                'merchant_ref': order_dict['merchant_ref'],
                'amount': int(order_dict['amount']),
                'customer_name': order_dict.get('customer_name', order_dict.get('name', 'Customer')),
                'customer_email': order_dict['customer_email'],
                'customer_phone': order_dict.get('phone_number', order_dict.get('phone', '')),
                'order_items': [
                    {
                        'sku': order_dict.get('package_id', 'chatgpt_plus'),
                        'name': order_dict.get('package_name', 'ChatGPT Plus Subscription'),
                        'price': int(order_dict['amount']),
                        'quantity': 1
                    }
                ],
                'return_url': return_url,
                'expired_time': int((datetime.now().timestamp() + 24 * 3600)),  # 24 hours
                'signature': signature
            }
            
            # Add callback URL
            if callback_url:
                payload['callback_url'] = callback_url
            
            # Make request to Tripay
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}/transaction/create"
            
            logger.info(f"Creating Tripay transaction: {payload['merchant_ref']}")
            logger.info(f"Tripay URL: {url}")
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            logger.info(f"Tripay response status: {response.status_code}")
            logger.info(f"Tripay response body: {response.text}")
            
            if response.status_code != 200:
                error_detail = {
                    'status_code': response.status_code,
                    'response_body': response.text
                }
                logger.error(f"Tripay API error: {error_detail}")
                return {
                    'success': False,
                    'error': 'Payment gateway error',
                    'details': error_detail
                }
            
            result = response.json()
            
            if not result.get('success', False):
                error_detail = {
                    'tripay_message': result.get('message', 'Unknown error'),
                    'tripay_data': result.get('data', {})
                }
                logger.error(f"Tripay transaction failed: {error_detail}")
                return {
                    'success': False,
                    'error': 'Payment gateway error',
                    'details': error_detail
                }
            
            data = result.get('data', {})
            
            return {
                'success': True,
                'reference': data.get('reference'),
                'checkout_url': data.get('checkout_url'),
                'qr_string': data.get('qr_string'),  # For QRIS
                'pay_code': data.get('pay_code'),    # For VA
                'pay_url': data.get('pay_url'),      # Alternative payment URL
                'payment_method': method,
                'amount': int(order_dict['amount']),
                'expired_time': data.get('expired_time'),
                'status': data.get('status', 'UNPAID')
            }
            
        except requests.exceptions.RequestException as e:
            error_detail = {'network_error': str(e)}
            logger.error(f"Tripay request error: {error_detail}")
            return {
                'success': False,
                'error': 'Network error',
                'details': error_detail
            }
        except Exception as e:
            error_detail = {'exception': str(e)}
            logger.error(f"Tripay transaction creation failed: {error_detail}")
            return {
                'success': False,
                'error': 'Internal error',
                'details': error_detail
            }
    
    def verify_callback_signature(self, payload_dict):
        """
        Verify Tripay callback signature using HMAC-SHA256
        
        Args:
            payload_dict (dict): Callback payload from Tripay
        
        Returns:
            bool: True if signature is valid, False otherwise
        """
        try:
            received_signature = payload_dict.get('signature')
            if not received_signature:
                logger.error("No signature found in callback payload")
                return False
            
            # Build signature string according to Tripay documentation
            # Format may vary - check Tripay docs for exact format
            # Common format: merchant_ref + reference + total_amount + status + private_key
            signature_string = (
                str(payload_dict.get('merchant_ref', '')) +
                str(payload_dict.get('reference', '')) +
                str(payload_dict.get('total_amount', payload_dict.get('amount', ''))) +
                str(payload_dict.get('status', ''))
            )
            
            # Generate HMAC-SHA256 signature
            calculated_signature = hmac.new(
                self.private_key.encode('utf-8'),
                signature_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            is_valid = hmac.compare_digest(received_signature, calculated_signature)
            
            if not is_valid:
                logger.error(f"Signature verification failed")
                logger.error(f"Expected: {calculated_signature}")
                logger.error(f"Received: {received_signature}")
                logger.error(f"Signature string: {signature_string}")
                # Log payload without sensitive data
                safe_payload = {k: v for k, v in payload_dict.items() if k != 'signature'}
                logger.error(f"Callback payload: {safe_payload}")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Signature verification error: {str(e)}")
            return False
    
    def get_payment_channels(self):
        """
        Get available payment channels from Tripay
        
        Returns:
            dict: Available payment channels
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}/merchant/payment-channel"
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'data': result.get('data', [])
                }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}: {response.text}'
                }
                
        except Exception as e:
            logger.error(f"Failed to get payment channels: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

# Global client instance
_client = None

def get_tripay_client():
    """Factory function to get Tripay client instance"""
    global _client
    if _client is None:
        _client = TripayClient()
    return _client
