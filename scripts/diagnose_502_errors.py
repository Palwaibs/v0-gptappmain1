#!/usr/bin/env python3
"""
Script untuk mendiagnosis masalah 502 Bad Gateway
"""
import os
import sys
import requests
import subprocess
import json
from datetime import datetime

def check_environment_variables():
    """Check if all required environment variables are set"""
    print("🔍 CHECKING ENVIRONMENT VARIABLES")
    print("=" * 50)
    
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL', 
        'TRIPAY_API_KEY',
        'TRIPAY_MERCHANT_CODE',
        'TRIPAY_PRIVATE_KEY',
        'TRIPAY_CALLBACK_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var}: NOT SET")
        else:
            # Show partial value for security
            if 'KEY' in var or 'PASSWORD' in var:
                display_value = value[:8] + "..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
    
    if missing_vars:
        print(f"\n🚨 CRITICAL: {len(missing_vars)} required environment variables are missing!")
        print("Create a .env file in the backend directory with these variables:")
        for var in missing_vars:
            print(f"  {var}=your_value_here")
        return False
    
    print("✅ All required environment variables are set")
    return True

def check_docker_services():
    """Check Docker services status"""
    print("\n🐳 CHECKING DOCKER SERVICES")
    print("=" * 50)
    
    try:
        # Check if docker-compose is running
        result = subprocess.run(['docker-compose', 'ps'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode != 0:
            print("❌ Docker Compose not running or not found")
            print("Run: docker-compose up -d")
            return False
        
        print("Docker Compose Status:")
        print(result.stdout)
        
        # Check specific services
        services = ['backend', 'postgres', 'redis']
        for service in services:
            result = subprocess.run(['docker-compose', 'ps', service], 
                                  capture_output=True, text=True, cwd='.')
            if 'Up' in result.stdout:
                print(f"✅ {service}: Running")
            else:
                print(f"❌ {service}: Not running or unhealthy")
        
        return True
        
    except FileNotFoundError:
        print("❌ Docker or docker-compose not found")
        return False
    except Exception as e:
        print(f"❌ Error checking Docker services: {e}")
        return False

def check_backend_logs():
    """Check backend container logs for errors"""
    print("\n📋 CHECKING BACKEND LOGS")
    print("=" * 50)
    
    try:
        result = subprocess.run(['docker-compose', 'logs', '--tail=50', 'backend'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            logs = result.stdout
            print("Recent backend logs:")
            print(logs)
            
            # Look for common error patterns
            error_patterns = [
                'ERROR',
                'CRITICAL',
                'Exception',
                'Traceback',
                'Connection refused',
                'No module named',
                'ImportError',
                'ValueError'
            ]
            
            errors_found = []
            for pattern in error_patterns:
                if pattern in logs:
                    errors_found.append(pattern)
            
            if errors_found:
                print(f"\n🚨 Found error patterns: {', '.join(errors_found)}")
                return False
            else:
                print("✅ No obvious errors in recent logs")
                return True
        else:
            print("❌ Could not retrieve backend logs")
            return False
            
    except Exception as e:
        print(f"❌ Error checking logs: {e}")
        return False

def test_database_connection():
    """Test database connectivity"""
    print("\n🗄️ TESTING DATABASE CONNECTION")
    print("=" * 50)
    
    try:
        # Try to connect to database using environment variables
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not set")
            return False
        
        # Simple connection test
        if 'postgresql' in database_url:
            try:
                import psycopg2
                conn = psycopg2.connect(database_url)
                conn.close()
                print("✅ PostgreSQL connection successful")
                return True
            except ImportError:
                print("⚠️ psycopg2 not installed, skipping direct DB test")
            except Exception as e:
                print(f"❌ PostgreSQL connection failed: {e}")
                return False
        
        print("⚠️ Database connection test skipped (unsupported DB type)")
        return True
        
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def test_internal_health():
    """Test backend health endpoint internally"""
    print("\n🏥 TESTING INTERNAL HEALTH ENDPOINT")
    print("=" * 50)
    
    try:
        # Test internal Docker network
        result = subprocess.run([
            'docker-compose', 'exec', '-T', 'backend', 
            'curl', '-f', 'http://localhost:5000/health'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Internal health check passed")
            print(f"Response: {result.stdout}")
            return True
        else:
            print("❌ Internal health check failed")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Internal health test error: {e}")
        return False

def generate_fix_commands():
    """Generate commands to fix common issues"""
    print("\n🔧 SUGGESTED FIX COMMANDS")
    print("=" * 50)
    
    print("1. Restart all services:")
    print("   docker-compose down && docker-compose up -d")
    
    print("\n2. Rebuild backend container:")
    print("   docker-compose build backend && docker-compose up -d backend")
    
    print("\n3. Check backend container directly:")
    print("   docker-compose exec backend python app.py")
    
    print("\n4. View real-time logs:")
    print("   docker-compose logs -f backend")
    
    print("\n5. Reset everything (CAUTION - will lose data):")
    print("   docker-compose down -v && docker-compose up -d")

def main():
    print("🚨 DIAGNOSING 502 BAD GATEWAY ERRORS")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("Docker Services", check_docker_services),
        ("Backend Logs", check_backend_logs),
        ("Database Connection", test_database_connection),
        ("Internal Health", test_internal_health)
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} check failed with exception: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSIS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed < total:
        print("\n🚨 SYSTEM NOT READY - Issues found that need fixing")
        generate_fix_commands()
    else:
        print("\n✅ ALL CHECKS PASSED - 502 errors might be network/proxy related")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
