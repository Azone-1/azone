#!/usr/bin/env python3
"""
Auto-start script for AZone Bot Builder
Opens browser automatically and keeps server running
"""
import subprocess
import time
import webbrowser
import sys
import os

def start_server():
    """Start the Flask server and open browser"""
    print("=" * 50)
    print("  AZone Bot Builder Server")
    print("  Auto-Start Mode")
    print("=" * 50)
    print()
    print("Server is starting...")
    print("Browser will open automatically in 3 seconds...")
    print()
    print("To stop: Press Ctrl+C")
    print()
    
    # Wait 3 seconds then open browser
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:5000')
        print("✓ Browser opened!")
    except Exception as e:
        print(f"⚠ Could not open browser automatically: {e}")
        print("  Please open http://localhost:5000 manually")
    
    print()
    print("Server is running. Press Ctrl+C to stop.")
    print("-" * 50)
    print()
    
    # Start Flask server
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Run Flask app
        subprocess.run([sys.executable, 'web_app.py'])
    except KeyboardInterrupt:
        print()
        print("Server stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
        print("Restarting in 5 seconds...")
        time.sleep(5)
        start_server()

if __name__ == '__main__':
    start_server()

