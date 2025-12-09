# 🚀 Quick Start Guide - AZone Flask Server

## Method 1: Double-Click Batch File (Easiest)
1. Double-click `start_server.bat` in the Azone folder
2. A window will open showing server status
3. Visit: http://localhost:5000

## Method 2: Command Line
Open PowerShell or Command Prompt in the Azone folder and run:
```bash
python web_app.py
```

## Method 3: Using Cursor Command
Type `/start-server` in Cursor chat

## Verify Server is Running
1. Open your browser
2. Go to: http://localhost:5000
3. You should see the AZone dashboard

## If Server Doesn't Start
1. Check if Python is installed: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Check for errors in the terminal window
4. Make sure port 5000 is not already in use

## Server Configuration
- **Host**: 0.0.0.0 (accessible from network)
- **Port**: 5000
- **URL**: http://localhost:5000

## Stop Server
Press `Ctrl+C` in the terminal window, or close the window.
