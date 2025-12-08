# Run Now - Simple execution
# Copy this entire file content and paste into PowerShell

cd C:\Users\User\Desktop\Azone
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Starting SSH Key Setup..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Run the script
& ".\SETUP_SSH_KEY.ps1"

Write-Host ""
Write-Host "Script execution completed!" -ForegroundColor Green
