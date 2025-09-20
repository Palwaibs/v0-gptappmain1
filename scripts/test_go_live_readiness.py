#!/usr/bin/env python3
"""
Script untuk tes kesiapan go-live sistem
Menguji semua komponen kritis sebelum deployment production
"""

import requests
import json
import time
import os
from datetime import datetime
import hashlib
import hmac

class GoLiveTestSuite:
    def __init__(self):
        self.api_base = os.getenv('API_URL', 'https://api.aksesgptmurah.tech')
        self.frontend_url = os.getenv('FRONTEND_URL', 'https://aksesgptmurah.tech')
        self.test_results = []
        
    def log_test(self, test_name, status, message="", details=None):
        """Log hasil tes"""
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        
    def test_backend_health(self):
        """Tes 1: Backend Health Check"""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_test("Backend Health", "PASS", "Backend responding correctly")
                else:
                    self.log_test("Backend Health", "FAIL", f"Unhealthy status: {data}")
            else:
                self.log_test("Backend Health", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Backend Health", "FAIL", f"Connection error: {str(e)}")
    
    def test_cors_configuration(self):
        """Tes 2: CORS Configuration"""
        try:
            headers = {
                'Origin': self.frontend_url,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            response = requests.options(f"{self.api_base}/api/orders", headers=headers, timeout=10)
            
            cors_headers = response.headers
            if 'Access-Control-Allow-Origin' in cors_headers:
                allowed_origin = cors_headers['Access-Control-Allow-Origin']
                if allowed_origin == self.frontend_url or allowed_origin == '*':
                    self.log_test("CORS Configuration", "PASS", "CORS properly configured")
                else:
                    self.log_test("CORS Configuration", "FAIL", f"Wrong origin: {allowed_origin}")
            else:
                self.log_test("CORS Configuration", "FAIL", "No CORS headers found")
        except Exception as e:
            self.log_test("CORS Configuration", "FAIL", f"CORS test error: {str(e)}")
    
    def test_packages_endpoint(self):
        """Tes 3: Packages API"""
        try:
            response = requests.get(f"{self.api_base}/api/packages", timeout=10)
            if response.status_code == 200:
                packages = response.json()
                if isinstance(packages, list) and len(packages) > 0:
                    self.log_test("Packages API", "PASS", f"Found {len(packages)} packages")
                else:
                    self.log_test("Packages API", "FAIL", "No packages found")
            else:
                self.log_test("Packages API", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Packages API", "FAIL", f"Error: {str(e)}")
    
    def test_order_creation(self):
        """Tes 4: Order Creation Flow"""
        try:
            test_order = {
                "package_id": 1,
                "customer_email": "test@example.com",
                "customer_name": "Test User",
                "payment_method": "QRIS"
            }
            
            response = requests.post(
                f"{self.api_base}/api/orders",
                json=test_order,
                timeout=15
            )
            
            if response.status_code == 201:
                order_data = response.json()
                required_fields = ['order_id', 'payment_url', 'qr_code', 'amount']
                
                if all(field in order_data for field in required_fields):
                    self.log_test("Order Creation", "PASS", "Order created successfully", 
                                order_data.get('order_id'))
                    return order_data.get('order_id')
                else:
                    self.log_test("Order Creation", "FAIL", "Missing required fields in response")
            else:
                self.log_test("Order Creation", "FAIL", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Order Creation", "FAIL", f"Error: {str(e)}")
        
        return None
    
    def test_order_status(self, order_id):
        """Tes 5: Order Status Check"""
        if not order_id:
            self.log_test("Order Status", "SKIP", "No order ID from previous test")
            return
            
        try:
            response = requests.get(f"{self.api_base}/api/orders/{order_id}/status", timeout=10)
            if response.status_code == 200:
                status_data = response.json()
                if 'status' in status_data:
                    self.log_test("Order Status", "PASS", f"Status: {status_data['status']}")
                else:
                    self.log_test("Order Status", "FAIL", "No status field in response")
            else:
                self.log_test("Order Status", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Order Status", "FAIL", f"Error: {str(e)}")
    
    def test_webhook_endpoint(self):
        """Tes 6: Webhook Endpoint"""
        try:
            # Test webhook dengan signature palsu (harus ditolak)
            test_payload = {
                "merchant_ref": "TEST123",
                "status": "PAID",
                "amount": 10000
            }
            
            response = requests.post(
                f"{self.api_base}/callback/tripay",
                json=test_payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            # Webhook harus menolak request tanpa signature yang valid
            if response.status_code in [400, 401, 403]:
                self.log_test("Webhook Security", "PASS", "Webhook properly validates signatures")
            else:
                self.log_test("Webhook Security", "FAIL", f"Webhook accepts invalid requests: {response.status_code}")
                
        except Exception as e:
            self.log_test("Webhook Security", "FAIL", f"Error: {str(e)}")
    
    def test_database_connection(self):
        """Tes 7: Database Connection"""
        try:
            # Test melalui admin endpoint yang memerlukan database
            response = requests.get(f"{self.api_base}/api/admin/orders", timeout=10)
            
            # Endpoint harus merespons (meskipun mungkin 401 karena tidak ada auth)
            if response.status_code in [200, 401, 403]:
                self.log_test("Database Connection", "PASS", "Database accessible")
            elif response.status_code == 500:
                self.log_test("Database Connection", "FAIL", "Database connection error")
            else:
                self.log_test("Database Connection", "WARN", f"Unexpected response: {response.status_code}")
        except Exception as e:
            self.log_test("Database Connection", "FAIL", f"Error: {str(e)}")
    
    def test_frontend_accessibility(self):
        """Tes 8: Frontend Accessibility"""
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                if 'text/html' in response.headers.get('content-type', ''):
                    self.log_test("Frontend Access", "PASS", "Frontend accessible")
                else:
                    self.log_test("Frontend Access", "WARN", "Frontend returns non-HTML content")
            else:
                self.log_test("Frontend Access", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Frontend Access", "FAIL", f"Error: {str(e)}")
    
    def test_ssl_certificates(self):
        """Tes 9: SSL Certificates"""
        try:
            import ssl
            import socket
            from urllib.parse import urlparse
            
            for url in [self.api_base, self.frontend_url]:
                parsed = urlparse(url)
                if parsed.scheme == 'https':
                    context = ssl.create_default_context()
                    with socket.create_connection((parsed.hostname, 443), timeout=10) as sock:
                        with context.wrap_socket(sock, server_hostname=parsed.hostname) as ssock:
                            cert = ssock.getpeercert()
                            self.log_test("SSL Certificate", "PASS", f"Valid SSL for {parsed.hostname}")
                else:
                    self.log_test("SSL Certificate", "WARN", f"No HTTPS for {url}")
        except Exception as e:
            self.log_test("SSL Certificate", "FAIL", f"SSL error: {str(e)}")
    
    def run_all_tests(self):
        """Jalankan semua tes"""
        print("🚀 MEMULAI TES KESIAPAN GO-LIVE")
        print("=" * 50)
        
        # Tes berurutan
        self.test_backend_health()
        self.test_cors_configuration()
        self.test_packages_endpoint()
        order_id = self.test_order_creation()
        self.test_order_status(order_id)
        self.test_webhook_endpoint()
        self.test_database_connection()
        self.test_frontend_accessibility()
        self.test_ssl_certificates()
        
        # Ringkasan hasil
        self.print_summary()
    
    def print_summary(self):
        """Cetak ringkasan hasil tes"""
        print("\n" + "=" * 50)
        print("📊 RINGKASAN HASIL TES")
        print("=" * 50)
        
        passed = len([t for t in self.test_results if t['status'] == 'PASS'])
        failed = len([t for t in self.test_results if t['status'] == 'FAIL'])
        warnings = len([t for t in self.test_results if t['status'] == 'WARN'])
        skipped = len([t for t in self.test_results if t['status'] == 'SKIP'])
        
        print(f"✅ PASSED: {passed}")
        print(f"❌ FAILED: {failed}")
        print(f"⚠️  WARNINGS: {warnings}")
        print(f"⏭️  SKIPPED: {skipped}")
        
        if failed == 0:
            print("\n🎉 SISTEM SIAP GO-LIVE!")
            print("Semua tes kritis berhasil.")
        else:
            print(f"\n🚨 SISTEM BELUM SIAP!")
            print(f"Ada {failed} tes yang gagal. Perbaiki sebelum go-live.")
            
            print("\n❌ TES YANG GAGAL:")
            for test in self.test_results:
                if test['status'] == 'FAIL':
                    print(f"  - {test['test']}: {test['message']}")
        
        if warnings > 0:
            print(f"\n⚠️  PERINGATAN ({warnings} item):")
            for test in self.test_results:
                if test['status'] == 'WARN':
                    print(f"  - {test['test']}: {test['message']}")
        
        # Simpan hasil ke file
        with open('go_live_test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n📄 Hasil lengkap disimpan di: go_live_test_results.json")

if __name__ == "__main__":
    tester = GoLiveTestSuite()
    tester.run_all_tests()
