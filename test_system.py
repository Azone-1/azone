#!/usr/bin/env python
"""System test for AZone Flask application"""
import sys
import socket
import requests
from datetime import datetime
import io

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_imports():
    """Test if all required modules can be imported"""
    print("=" * 60)
    print("TEST 1: Module Imports")
    print("=" * 60)
    try:
        import web_app
        print("✓ web_app imported")
        
        import config
        print("✓ config imported")
        
        import db_manager
        print("✓ db_manager imported")
        
        import bot_db_manager
        print("✓ bot_db_manager imported")
        
        print("\n✓ All imports successful!")
        return True
    except Exception as e:
        print(f"\n✗ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_server_running(host='localhost', port=5000):
    """Test if server is running and responding"""
    print("\n" + "=" * 60)
    print("TEST 2: Server Status")
    print("=" * 60)
    
    # Check if port is listening
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✓ Port {port} is open and listening")
        else:
            print(f"✗ Port {port} is not accessible")
            return False
    except Exception as e:
        print(f"✗ Socket error: {e}")
        return False
    
    # Try HTTP request
    try:
        response = requests.get(f'http://{host}:{port}', timeout=5)
        print(f"✓ Server responded with status: {response.status_code}")
        print(f"✓ Server is RUNNING and accessible!")
        return True
    except requests.exceptions.ConnectionError:
        print(f"✗ Server not responding on http://{host}:{port}")
        return False
    except Exception as e:
        print(f"✗ HTTP request error: {e}")
        return False

def main():
    print(f"\nAZone System Test - {datetime.now()}")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test server
    server_ok = test_server_running()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Imports: {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"Server:  {'✓ PASS' if server_ok else '✗ FAIL'}")
    
    if imports_ok and server_ok:
        print("\n✓✓✓ All tests PASSED! System is ready. ✓✓✓")
        return 0
    else:
        print("\n✗✗✗ Some tests FAILED. Please check errors above. ✗✗✗")
        return 1

if __name__ == '__main__':
    sys.exit(main())
