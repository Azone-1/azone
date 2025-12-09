#!/usr/bin/env python
"""Start the Flask server with full error logging"""
import sys
import traceback
import os

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    print("=" * 60)
    print("AZone Flask Server Startup")
    print("=" * 60)
    print(f"Working Directory: {os.getcwd()}")
    print(f"Python Version: {sys.version}")
    print("=" * 60)
    
    # Try importing web_app
    print("\n[1/3] Importing web_app module...")
    import web_app
    print("✓ web_app imported successfully")
    
    # Get config
    print("\n[2/3] Loading configuration...")
    import config
    host = config.Config.HOST
    port = config.Config.PORT
    debug = config.Config.DEBUG
    print(f"✓ Config loaded: HOST={host}, PORT={port}, DEBUG={debug}")
    
    # Start server
    print("\n[3/3] Starting Flask server...")
    print(f"\n{'='*60}")
    print(f"🚀 AZone Bot Builder Server")
    print(f"{'='*60}")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"{'='*60}\n")
    print("Server is starting... Press Ctrl+C to stop.\n")
    
    web_app.app.run(debug=debug, host=host, port=port, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\nServer stopped by user.")
    sys.exit(0)
except Exception as e:
    print(f"\n✗ ERROR starting server:")
    print(f"  {type(e).__name__}: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
