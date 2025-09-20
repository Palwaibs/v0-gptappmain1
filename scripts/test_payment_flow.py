#!/usr/bin/env python3
"""
Script khusus untuk tes payment flow end-to-end
"""

import requests
import json
import time
import os
from datetime import datetime

class PaymentFlowTester:
    def __init__(self):
        self.api_base = os.getenv('API_URL', 'https://api.aksesgptmurah.tech')
        
    def test_complete_payment_flow(self):
        """Tes complete payment flow"""
        print("🔄 TESTING COMPLETE PAYMENT FLOW")
        print("=" * 40)
        
        # Step 1: Create order
        print("1️⃣ Creating test order...")
        order_data = {
            "package_id": 1,
            "customer_email": "test@example.com",
            "customer_name": "Test User",
            "payment_method": "QRIS"
        }
        
        try:
            response = requests.post(f"{self.api_base}/api/orders", json=order_data)
            if response.status_code != 201:
                print(f"❌ Order creation failed: {response.status_code}")
                return False
                
            order = response.json()
            order_id = order.get('order_id')
            print(f"✅ Order created: {order_id}")
            
            # Step 2: Check initial status
            print("2️⃣ Checking initial order status...")
            status_response = requests.get(f"{self.api_base}/api/orders/{order_id}/status")
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"✅ Initial status: {status.get('status')}")
            else:
                print(f"❌ Status check failed: {status_response.status_code}")
                return False
            
            # Step 3: Simulate webhook (manual test)
            print("3️⃣ Testing webhook endpoint...")
            webhook_data = {
                "merchant_ref": order_id,
                "status": "PAID",
                "amount": order.get('amount', 10000)
            }
            
            # Note: Ini akan gagal karena signature, tapi endpoint harus merespons
            webhook_response = requests.post(f"{self.api_base}/callback/tripay", json=webhook_data)
            if webhook_response.status_code in [400, 401, 403]:
                print("✅ Webhook endpoint responding (signature validation working)")
            else:
                print(f"⚠️ Webhook response: {webhook_response.status_code}")
            
            print(f"\n📋 PAYMENT FLOW TEST SUMMARY:")
            print(f"Order ID: {order_id}")
            print(f"Payment URL: {order.get('payment_url', 'N/A')}")
            print(f"QR Code: {'Available' if order.get('qr_code') else 'Not available'}")
            print(f"Amount: Rp {order.get('amount', 0):,}")
            
            return True
            
        except Exception as e:
            print(f"❌ Payment flow test error: {str(e)}")
            return False

if __name__ == "__main__":
    tester = PaymentFlowTester()
    tester.test_complete_payment_flow()
