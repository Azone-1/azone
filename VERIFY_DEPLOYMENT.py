#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify deployment configuration and test URLs"""
import sys
import os
import requests
from urllib.parse import urlparse

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("=" * 60)
    print("CHECK 1: Environment Configuration")
    print("=" * 60)
    
    env_file = '.env'
    env_example = 'env.example'
    
    if not os.path.exists(env_file):
        print(f"⚠ .env file not found")
        if os.path.exists(env_example):
            print(f"✓ env.example found - Copy it to .env and update values")
            return False
        else:
            print(f"✗ env.example also not found!")
            return False
    else:
        print(f"✓ .env file exists")
        
        # Check for key variables
        required_vars = ['DOMAIN', 'SECRET_KEY', 'GEMINI_API_KEY']
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            for var in required_vars:
                if f'{var}=' in content:
                    print(f"✓ {var} found")
                else:
                    print(f"⚠ {var} not found in .env")
        
        return True

def check_railway_files():
    """Check if Railway deployment files exist"""
    print("\n" + "=" * 60)
    print("CHECK 2: Railway Deployment Files")
    print("=" * 60)
    
    files = {
        'Procfile': 'web: python web_app.py',
        'railway.json': 'Railway configuration',
        '.gitignore': 'Git ignore file'
    }
    
    all_ok = True
    for filename, description in files.items():
        if os.path.exists(filename):
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing - {description}")
            all_ok = False
    
    return all_ok

def check_config():
    """Check config.py for domain support"""
    print("\n" + "=" * 60)
    print("CHECK 3: Application Configuration")
    print("=" * 60)
    
    try:
        import config
        print(f"✓ config.py imported")
        print(f"✓ HOST: {config.Config.HOST}")
        print(f"✓ PORT: {config.Config.PORT}")
        print(f"✓ DOMAIN: {config.Config.DOMAIN}")
        print(f"✓ USE_HTTPS: {config.Config.USE_HTTPS}")
        return True
    except Exception as e:
        print(f"✗ Error importing config: {e}")
        return False

def test_local_server():
    """Test if local server is running"""
    print("\n" + "=" * 60)
    print("CHECK 4: Local Server Test")
    print("=" * 60)
    
    try:
        response = requests.get('http://localhost:5000', timeout=3)
        print(f"✓ Local server is RUNNING")
        print(f"✓ Status Code: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"⚠ Local server not running (this is OK if deploying to Railway)")
        return None
    except Exception as e:
        print(f"⚠ Error checking local server: {e}")
        return None

def generate_webhook_url():
    """Generate webhook URL based on domain"""
    print("\n" + "=" * 60)
    print("CHECK 5: Webhook URLs")
    print("=" * 60)
    
    try:
        import config
        domain = config.Config.DOMAIN
        use_https = config.Config.USE_HTTPS
        
        protocol = 'https' if use_https else 'http'
        base_url = f"{protocol}://{domain}"
        
        print(f"✓ Domain: {domain}")
        print(f"✓ Protocol: {protocol}")
        print(f"\nWebhook URLs:")
        print(f"  Facebook: {base_url}/webhook/facebook")
        print(f"  Main App: {base_url}")
        print(f"  Dashboard: {base_url}/dashboard")
        
        return True
    except Exception as e:
        print(f"✗ Error generating URLs: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("AZone Deployment Verification")
    print("=" * 60)
    print()
    
    results = []
    
    # Run checks
    results.append(("Environment Config", check_env_file()))
    results.append(("Railway Files", check_railway_files()))
    results.append(("App Configuration", check_config()))
    local_server = test_local_server()
    if local_server is not None:
        results.append(("Local Server", local_server))
    results.append(("Webhook URLs", generate_webhook_url()))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓✓✓ All checks PASSED! Ready for deployment. ✓✓✓")
        print("\nNext steps:")
        print("1. Push to GitHub: git push")
        print("2. Deploy on Railway.app")
        print("3. Configure domain: paing.xyz")
        return 0
    else:
        print("\n⚠ Some checks failed. Please fix issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
