# start-server

Starts the Flask web application server.

This command will be available in chat with /start-server

```bash
# Stop any existing Python processes
taskkill /F /IM python.exe 2>$null
Start-Sleep -Seconds 1

# Start Flask server in background
Start-Process python -ArgumentList "web_app.py" -WindowStyle Hidden

# Wait for server to start, then open browser
Start-Sleep -Seconds 3
Start-Process "http://localhost:5000"
```
