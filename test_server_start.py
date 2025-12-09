#!/usr/bin/env python
"""Quick test to see if web_app can start"""
import sys
import traceback

try:
    print("Testing imports...")
    import web_app
    print("✓ web_app imported successfully")
    
    print("\nTesting Flask app creation...")
    app = web_app.app
    print(f"✓ Flask app created: {app}")
    
    print("\nTesting config...")
    import config
    host = config.Config.HOST
    port = config.Config.PORT
    print(f"✓ Config loaded: HOST={host}, PORT={port}")
    
    print("\n✓ All checks passed! Server should start successfully.")
    print(f"\nTo start server, run: python web_app.py")
    print(f"Then visit: http://{host}:{port}")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
