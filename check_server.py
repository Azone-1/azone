#!/usr/bin/env python
"""Check if server is running on port 5000"""
import socket
import sys

def check_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error checking port: {e}")
        return False

if __name__ == '__main__':
    host = 'localhost'
    port = 5000
    
    print(f"Checking if server is running on {host}:{port}...")
    
    if check_port(host, port):
        print(f"✓ Server IS running on port {port}!")
        print(f"Visit: http://{host}:{port}")
        sys.exit(0)
    else:
        print(f"✗ Server is NOT running on port {port}")
        print("Please start the server with: python web_app.py")
        sys.exit(1)
