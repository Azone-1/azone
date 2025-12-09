# AZone 24/7 Keep-Alive Script
# This script keeps the Flask server running continuously
# It will automatically restart the server if it crashes

$ErrorActionPreference = "Continue"
$script:ServerProcess = $null
$script:RestartCount = 0
$script:MaxRestarts = 1000  # Prevent infinite loops, but allow many restarts
$script:CheckInterval = 10  # Check every 10 seconds
$script:ProjectPath = "C:\Users\User\Desktop\Azone"
$script:LogFile = Join-Path $script:ProjectPath "server_24_7.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $script:LogFile -Value $logMessage -ErrorAction SilentlyContinue
}

function Start-Server {
    Write-Log "Starting Flask server..."
    
    # Change to project directory
    Set-Location $script:ProjectPath
    
    # Start server process
    $script:ServerProcess = Start-Process python -ArgumentList "web_app.py" -WorkingDirectory $script:ProjectPath -PassThru -WindowStyle Hidden
    
    if ($script:ServerProcess) {
        Write-Log "Server started with PID: $($script:ServerProcess.Id)"
        Start-Sleep -Seconds 5  # Wait for server to initialize
        
        # Verify server is running
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:5000" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Log "✓ Server is running and responding!"
                return $true
            }
        } catch {
            Write-Log "⚠ Server started but not responding yet. Will check again..."
        }
        return $true
    } else {
        Write-Log "✗ Failed to start server process"
        return $false
    }
}

function Stop-Server {
    if ($script:ServerProcess -and !$script:ServerProcess.HasExited) {
        Write-Log "Stopping server (PID: $($script:ServerProcess.Id))..."
        try {
            $script:ServerProcess.Kill()
            $script:ServerProcess.WaitForExit(5000)
            Write-Log "Server stopped"
        } catch {
            Write-Log "Error stopping server: $_"
        }
    }
    $script:ServerProcess = $null
}

function Check-Server {
    if ($null -eq $script:ServerProcess -or $script:ServerProcess.HasExited) {
        return $false
    }
    
    # Check if process is still running
    try {
        $process = Get-Process -Id $script:ServerProcess.Id -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Test-ServerHealth {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

# Main loop
Write-Log "=========================================="
Write-Log "AZone 24/7 Keep-Alive Script Started"
Write-Log "=========================================="
Write-Log "Project Path: $script:ProjectPath"
Write-Log "Check Interval: $script:CheckInterval seconds"
Write-Log "Log File: $script:LogFile"
Write-Log "=========================================="

# Initial server start
Start-Server

# Keep-alive loop
while ($true) {
    try {
        if (-not (Check-Server)) {
            Write-Log "⚠ Server process not running!"
            $script:RestartCount++
            
            if ($script:RestartCount -gt $script:MaxRestarts) {
                Write-Log "✗ Maximum restart limit reached ($script:MaxRestarts). Exiting."
                break
            }
            
            Write-Log "Restarting server... (Restart #$script:RestartCount)"
            Stop-Server
            Start-Sleep -Seconds 2
            Start-Server
        } else {
            # Server process exists, check if it's responding
            if (-not (Test-ServerHealth)) {
                Write-Log "⚠ Server process running but not responding to HTTP requests"
                Write-Log "Restarting server..."
                $script:RestartCount++
                Stop-Server
                Start-Sleep -Seconds 2
                Start-Server
            } else {
                # Server is healthy
                if ($script:RestartCount -eq 0 -or ($script:RestartCount % 10 -eq 0)) {
                    Write-Log "✓ Server is running normally (Uptime check)"
                }
            }
        }
        
        # Wait before next check
        Start-Sleep -Seconds $script:CheckInterval
        
    } catch {
        Write-Log "Error in keep-alive loop: $_"
        Start-Sleep -Seconds $script:CheckInterval
    }
}

# Cleanup
Write-Log "Shutting down..."
Stop-Server
Write-Log "24/7 script stopped"

