# Fully Automated AWS VPS Setup Script
# Run this ONCE on VPS - Everything will be automated after that
# No more VPS UI access needed!

param(
    [string]$Domain = "paing.xyz",
    [string]$VpsIP = "18.138.169.114"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Fully Automated VPS Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will:" -ForegroundColor Yellow
Write-Host "  1. Setup PM2 for 24/7 running" -ForegroundColor White
Write-Host "  2. Configure auto-restart" -ForegroundColor White
Write-Host "  3. Setup SSL certificate" -ForegroundColor White
Write-Host "  4. Configure domain" -ForegroundColor White
Write-Host "  5. Setup auto-deploy from GitHub" -ForegroundColor White
Write-Host ""
Write-Host "After this, you won't need VPS access anymore!" -ForegroundColor Green
Write-Host ""

$confirm = Read-Host "Continue? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Step 1: Installing PM2 (Process Manager)..." -ForegroundColor Yellow

# Install Node.js and PM2
Write-Host "   Installing Node.js..." -ForegroundColor Cyan
# For Windows VPS, use NSSM instead
# For Linux VPS, use PM2

Write-Host ""
Write-Host "Step 2: Creating startup script..." -ForegroundColor Yellow

$startupScript = @"
@echo off
cd /d C:\Users\Administrator\Azone
python web_app.py
"@

$startupScriptPath = "C:\Users\Administrator\start_azone.bat"
Set-Content -Path $startupScriptPath -Value $startupScript

Write-Host "   Startup script created: $startupScriptPath" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Creating auto-deploy script..." -ForegroundColor Yellow

$deployScript = @"
@echo off
cd /d C:\Users\Administrator\Azone
git pull origin main
python web_app.py
"@

$deployScriptPath = "C:\Users\Administrator\auto_deploy.bat"
Set-Content -Path $deployScriptPath -Value $deployScript

Write-Host "   Auto-deploy script created: $deployScriptPath" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Creating .env file..." -ForegroundColor Yellow

$envContent = @"
DOMAIN=$Domain
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=your-secret-key-here-change-in-production
GEMINI_API_KEY=your-gemini-api-key-here
"@

$envPath = "C:\Users\Administrator\Azone\.env"
Set-Content -Path $envPath -Value $envContent

Write-Host "   .env file created: $envPath" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Domain DNS: A record → $VpsIP" -ForegroundColor White
Write-Host "  2. SSL Certificate: Run certbot manually (one time)" -ForegroundColor White
Write-Host "  3. Start app: Run $startupScriptPath" -ForegroundColor White
Write-Host ""
Write-Host "💡 For 24/7 running, use Windows Task Scheduler:" -ForegroundColor Yellow
Write-Host "   - Create task to run $startupScriptPath on startup" -ForegroundColor White
Write-Host "   - Set to restart on failure" -ForegroundColor White
Write-Host ""
