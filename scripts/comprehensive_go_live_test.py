#!/usr/bin/env python3
"""
Comprehensive Go-Live Test Suite
Tests all critical components after environment configuration
"""

import requests
import json
import time
import sys
from datetime import datetime
from urllib.parse import urlparse

try:
    import pymysql
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("⚠️  Warning: PyMySQL not installed. Database tests will be skipped.")
    print("   Install with: pip install PyMySQL")

class GoLiveTestSuite:
    def __init__(self):
        self.api_base = "https://api.aksesgptmurah.tech"
        self.frontend_url = "https://aksesgptmurah.tech"
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'critical_failures': []
        }
        
    def log_result(self, test_name, status, message, is_critical=False):
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_icon = {
            'PASS': '✅',
            'FAIL': '❌', 
            'WARN': '⚠️',
            'INFO': 'ℹ️',
            'SKIP': '⏭️'
        }
        
        print(f"[{timestamp}] {status_icon.get(status, '?')} {test_name}: {message}")
        
        if status == 'PASS':
            self.results['passed'] += 1
        elif status == 'FAIL':
            self.results['failed'] += 1
            if is_critical:
                self.results['critical_failures'].append(test_name)
        elif status == 'WARN':
            self.results['warnings'] += 1

    def test_backend_health(self):
        """Test backend health and basic connectivity"""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_result("Backend Health", "PASS", "Backend is healthy and responding")
                    return True
                else:
                    self.log_result("Backend Health", "FAIL", f"Backend unhealthy: {data}", True)
            else:
                self.log_result("Backend Health", "FAIL", f"HTTP {response.status_code}: {response.text}", True)
        except requests.exceptions.RequestException as e:
            self.log_result("Backend Health", "FAIL", f"Connection failed: {str(e)}", True)
        return False

    def test_database_connection(self):
        """Test database connectivity"""
        if not MYSQL_AVAILABLE:
            self.log_result("Database Connection", "SKIP", "PyMySQL not available - install with: pip install PyMySQL")
            return False
            
        try:
            # Parse database URL
            db_url = "mysql+pymysql://gptuser:GptUser123!@127.0.0.1:3306/gptapp_db"
            parsed = urlparse(db_url.replace('mysql+pymysql://', 'mysql://'))
            
            conn = pymysql.connect(
                host=parsed.hostname,
                port=parsed.port or 3306,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path.lstrip('/'),
                connect_timeout=10
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            if result and result[0] == 1:
                self.log_result("Database Connection", "PASS", "Database connection successful")
                
                # Check if tables exist
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                
                required_tables = ['orders', 'packages', 'admin_accounts', 'invitation_log']
                missing_tables = [table for table in required_tables if table not in tables]
                
                if missing_tables:
                    self.log_result("Database Schema", "WARN", f"Missing tables: {missing_tables}")
                else:
                    self.log_result("Database Schema", "PASS", "All required tables exist")
                
                conn.close()
                return True
            else:
                self.log_result("Database Connection", "FAIL", "Database query failed", True)
                
        except Exception as e:
            self.log_result("Database Connection", "FAIL", f"Database error: {str(e)}", True)
        return False

    def test_cors_configuration(self):
        """Test CORS headers"""
        try:
            response = requests.options(f"{self.api_base}/api/packages", 
                                      headers={'Origin': self.frontend_url}, 
                                      timeout=10)
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            if cors_headers['Access-Control-Allow-Origin']:
                self.log_result("CORS Configuration", "PASS", "CORS headers present")
                return True
            else:
                self.log_result("CORS Configuration", "FAIL", "Missing CORS headers", True)
                
        except requests.exceptions.RequestException as e:
            self.log_result("CORS Configuration", "FAIL", f"CORS test failed: {str(e)}", True)
        return False

    def test_api_endpoints(self):
        """Test critical API endpoints"""
        endpoints = [
            ('/api/packages', 'GET', 'Package listing'),
            ('/api/orders', 'POST', 'Order creation')
        ]
        
        all_passed = True
        
        for endpoint, method, description in endpoints:
            try:
                if method == 'GET':
                    response = requests.get(f"{self.api_base}{endpoint}", timeout=10)
                elif method == 'POST':
                    # Test with minimal valid data
                    test_data = {
                        'email': 'test@example.com',
                        'package_id': 1
                    }
                    response = requests.post(f"{self.api_base}{endpoint}", 
                                           json=test_data, timeout=10)
                
                if response.status_code in [200, 201, 400]:  # 400 is OK for validation errors
                    self.log_result(f"API {endpoint}", "PASS", f"{description} endpoint responding")
                else:
                    self.log_result(f"API {endpoint}", "FAIL", f"HTTP {response.status_code}", True)
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.log_result(f"API {endpoint}", "FAIL", f"Request failed: {str(e)}", True)
                all_passed = False
                
        return all_passed

    def test_tripay_configuration(self):
        """Test Tripay payment gateway configuration"""
        try:
            # Test order creation with Tripay
            test_order = {
                'email': 'test@example.com',
                'package_id': 1
            }
            
            response = requests.post(f"{self.api_base}/api/orders", 
                                   json=test_order, timeout=15)
            
            if response.status_code == 201:
                data = response.json()
                if 'payment_url' in data and 'qr_code' in data:
                    self.log_result("Tripay Integration", "PASS", "Payment gateway integration working")
                    return True
                else:
                    self.log_result("Tripay Integration", "FAIL", "Missing payment data in response", True)
            else:
                self.log_result("Tripay Integration", "FAIL", f"Order creation failed: HTTP {response.status_code}", True)
                
        except requests.exceptions.RequestException as e:
            self.log_result("Tripay Integration", "FAIL", f"Tripay test failed: {str(e)}", True)
        return False

    def test_webhook_endpoint(self):
        """Test webhook endpoint security"""
        try:
            # Test webhook without signature (should fail)
            test_payload = {
                'merchant_ref': 'test123',
                'status': 'PAID'
            }
            
            response = requests.post(f"{self.api_base}/callback/tripay", 
                                   json=test_payload, timeout=10)
            
            # Should return 400 or 401 for invalid signature
            if response.status_code in [400, 401]:
                self.log_result("Webhook Security", "PASS", "Webhook properly validates signatures")
                return True
            else:
                self.log_result("Webhook Security", "WARN", f"Unexpected webhook response: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.log_result("Webhook Security", "FAIL", f"Webhook test failed: {str(e)}")
        return False

    def test_ssl_certificate(self):
        """Test SSL certificate validity"""
        try:
            response = requests.get(self.api_base, timeout=10, verify=True)
            self.log_result("SSL Certificate", "PASS", "SSL certificate is valid")
            return True
        except requests.exceptions.SSLError as e:
            self.log_result("SSL Certificate", "FAIL", f"SSL error: {str(e)}", True)
        except requests.exceptions.RequestException as e:
            self.log_result("SSL Certificate", "WARN", f"SSL test inconclusive: {str(e)}")
        return False

    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 COMPREHENSIVE GO-LIVE TEST SUITE")
        print("=" * 60)
        print(f"Testing API: {self.api_base}")
        print(f"Testing Frontend: {self.frontend_url}")
        print("=" * 60)
        
        if not MYSQL_AVAILABLE:
            print("⚠️  Missing Dependencies Detected:")
            print("   - PyMySQL: pip install PyMySQL")
            print("   Database tests will be skipped.")
            print()
        
        # Critical tests that must pass
        critical_tests = [
            self.test_backend_health,
            self.test_database_connection,
            self.test_cors_configuration,
            self.test_api_endpoints,
            self.test_tripay_configuration
        ]
        
        # Important but not critical tests
        additional_tests = [
            self.test_webhook_endpoint,
            self.test_ssl_certificate
        ]
        
        print("\n🔥 CRITICAL TESTS (Must Pass for Go-Live)")
        print("-" * 40)
        critical_passed = 0
        for test in critical_tests:
            if test():
                critical_passed += 1
        
        print("\n📋 ADDITIONAL TESTS")
        print("-" * 40)
        for test in additional_tests:
            test()
        
        # Final assessment
        print("\n" + "=" * 60)
        print("📊 FINAL GO-LIVE ASSESSMENT")
        print("=" * 60)
        
        total_critical = len(critical_tests)
        critical_success_rate = (critical_passed / total_critical) * 100
        
        print(f"✅ PASSED: {self.results['passed']}")
        print(f"❌ FAILED: {self.results['failed']}")
        print(f"⚠️  WARNINGS: {self.results['warnings']}")
        print(f"🔥 CRITICAL SUCCESS RATE: {critical_success_rate:.1f}% ({critical_passed}/{total_critical})")
        
        if critical_success_rate >= 100:
            print("\n🎉 READY FOR GO-LIVE!")
            print("All critical tests passed. System is production-ready.")
            return True
        elif critical_success_rate >= 80:
            print("\n⚠️  MOSTLY READY - Minor Issues")
            print("Most critical tests passed. Address warnings before go-live.")
            return False
        else:
            print("\n🚨 NOT READY FOR GO-LIVE")
            print("Critical failures detected. Must fix before production deployment.")
            print(f"Critical failures: {', '.join(self.results['critical_failures'])}")
            return False

if __name__ == "__main__":
    test_suite = GoLiveTestSuite()
    is_ready = test_suite.run_all_tests()
    sys.exit(0 if is_ready else 1)
