#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Start Flask server with proper error handling"""
import sys
import os
import traceback

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("AZone Flask Server - Starting...")
print("=" * 70)
print(f"Working Directory: {os.getcwd()}")
print(f"Python: {sys.executable}")
print(f"Python Version: {sys.version}")
print("=" * 70)

try:
    # Test imports first
    print("\n[Step 1/4] Testing imports...")
    import flask
    print(f"  ✓ Flask {flask.__version__}")
    
    import config
    print("  ✓ config module")
    
    print("\n[Step 2/4] Importing web_app...")
    import web_app
    print("  ✓ web_app imported")
    
    print("\n[Step 3/4] Loading configuration...")
    host = config.Config.HOST
    port = config.Config.PORT
    debug = config.Config.DEBUG
    print(f"  ✓ Host: {host}")
    print(f"  ✓ Port: {port}")
    print(f"  ✓ Debug: {debug}")
    
    print("\n[Step 4/4] Starting Flask server...")
    print("=" * 70)
    print(f"🚀 AZone Bot Builder Server")
    print("=" * 70)
    print(f"📍 URL: http://localhost:{port}")
    print(f"🌐 Network: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print("=" * 70)
    print("\n✓ Server is starting...")
    print("✓ Press Ctrl+C to stop the server\n")
    
    # Start the server
    web_app.app.run(debug=debug, host=host, port=port, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\n✓ Server stopped by user.")
    sys.exit(0)
except ImportError as e:
    print(f"\n✗ IMPORT ERROR: {e}")
    print("\nMissing dependency. Please install requirements:")
    print("  pip install -r requirements.txt")
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    print("\nFull error details:")
    traceback.print_exc()
    sys.exit(1)
