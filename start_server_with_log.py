#!/usr/bin/env python
"""Start Flask server and log everything to server.log"""
import sys
import traceback
import os
from datetime import datetime

# Redirect stdout and stderr to log file
log_file = open('server.log', 'w', encoding='utf-8')
sys.stdout = log_file
sys.stderr = log_file

try:
    print("=" * 60)
    print(f"AZone Flask Server Startup - {datetime.now()}")
    print("=" * 60)
    print(f"Working Directory: {os.getcwd()}")
    print(f"Python Version: {sys.version}")
    print("=" * 60)
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Changed to: {os.getcwd()}")
    
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
    
    # Also print to console
    print(f"\n✓ Server starting at http://{host}:{port}", file=sys.__stdout__)
    print("Check server.log for full output", file=sys.__stdout__)
    
    web_app.app.run(debug=debug, host=host, port=port, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\nServer stopped by user.")
    log_file.close()
    sys.exit(0)
except Exception as e:
    error_msg = f"\n✗ ERROR starting server:\n  {type(e).__name__}: {e}\n\nFull traceback:\n"
    print(error_msg)
    traceback.print_exc()
    print(error_msg, file=sys.__stdout__)
    traceback.print_exc(file=sys.__stdout__)
    log_file.close()
    sys.exit(1)
