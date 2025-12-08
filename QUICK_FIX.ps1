# Quick Fix - Check and Restart Services on VPS
# NO PASSWORD - Uses SSH key only
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
    Write-Host "   Run this first to setup passwordless access:" -ForegroundColor Yellow
    Write-Host "   powershell.exe -ExecutionPolicy Bypass -NoProfile -File SETUP_SSH_KEY.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "   (You'll enter password ONCE, then never again!)" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ Using SSH key - NO password needed!" -ForegroundColor Green
Write-Host ""

# Restart services
$restartCmd = @'
cd ~/Azone
echo "=== Restarting Services ==="
echo ""
echo "1. Restarting PM2..."
if pm2 restart azone-bot 2>/dev/null; then true; elif pm2 start web_app.py --name azone-bot --interpreter python3 2>/dev/null; then true; else echo "PM2 restart failed"; fi
echo ""
echo "2. Restarting Nginx..."
if sudo systemctl restart nginx 2>/dev/null; then true; else echo "Nginx restart failed"; fi
echo ""
echo "3. Checking status..."
echo "PM2 Status:"
if pm2 list 2>/dev/null | grep azone-bot; then true; else echo "PM2 not running"; fi
echo ""
echo "Nginx Status:"
if sudo systemctl is-active nginx 2>/dev/null; then true; else echo "Nginx not active"; fi
echo ""
echo "Ports:"
if ss -tuln 2>/dev/null | grep -E ":(80|443|8000)"; then true; else echo "No ports listening"; fi
'@

Write-Host "Restarting services on VPS..." -ForegroundColor Yellow
Write-Host ""

$sshTarget = $VPS_USER + "@" + $VPS_IP
ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH $sshTarget $restartCmd

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
