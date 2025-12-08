# Quick Fix - No Password Prompt
# Uses SSH key for passwordless access

$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$SSH_KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_azone"

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔧 QUICK FIX - Restart Services" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check SSH key
if (-not (Test-Path $SSH_KEY_PATH)) {
    Write-Host "❌ SSH key not found!" -ForegroundColor Red
    Write-Host "   Run: .\SETUP_SSH_KEY.ps1 first" -ForegroundColor Yellow
    Write-Host "   This will setup passwordless access" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Using SSH key for passwordless access" -ForegroundColor Green
Write-Host ""

# Restart services
$restartCmd = @'
cd ~/Azone
echo "=== Restarting Services ==="
echo ""
echo "1. Restarting PM2..."
pm2 restart azone-bot 2>/dev/null || pm2 start web_app.py --name azone-bot --interpreter python3 2>/dev/null || echo "PM2 restart failed"
echo ""
echo "2. Restarting Nginx..."
sudo systemctl restart nginx 2>/dev/null || echo "Nginx restart failed"
echo ""
echo "3. Checking status..."
echo "PM2 Status:"
pm2 list 2>/dev/null | grep azone-bot || echo "PM2 not running"
echo ""
echo "Nginx Status:"
sudo systemctl is-active nginx 2>/dev/null || echo "Nginx not active"
echo ""
echo "Ports:"
ss -tuln 2>/dev/null | grep -E ":(80|443|8000)" || echo "No ports listening"
'@

Write-Host "Restarting services on VPS..." -ForegroundColor Yellow
Write-Host ""

ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "${VPS_USER}@${VPS_IP}" $restartCmd

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Services Restarted!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Try accessing:" -ForegroundColor Green
Write-Host "  http://paing.xyz" -ForegroundColor White
Write-Host "  http://18.138.169.114" -ForegroundColor White
Write-Host ""
Write-Host "Wait 30 seconds for services to start..." -ForegroundColor Yellow
Write-Host ""
