# start-server

Starts the Flask web application server.

This command will be available in chat with /start-server

```powershell
# Stop any existing Python processes
try { Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force } catch { }
Start-Sleep -Seconds 1

# Change to project directory
Set-Location "c:\Users\User\Desktop\Azone"

# Start Flask server in background with output logging
$logFile = "server_startup.log"
Start-Process python -ArgumentList "web_app.py" -WorkingDirectory "c:\Users\User\Desktop\Azone" -WindowStyle Normal

# Wait for server to start
Start-Sleep -Seconds 5

# Check if server is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 3
    Write-Host "✓ Server is RUNNING! Status: $($response.StatusCode)"
    Write-Host "📍 Visit: http://localhost:5000"
    Start-Process "http://localhost:5000"
} catch {
    Write-Host "✗ Server not responding yet. Check the Python window for errors."
    Write-Host "Error: $($_.Exception.Message)"
    Write-Host "You can also check server_startup.log for details."
}
```
