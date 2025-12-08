# VPN မလိုဘဲ VPS Connection Test Script
# Run this on your LOCAL machine to test connection

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🧪 Testing VPN-Free VPS Connection" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$vpsIP = "18.138.169.114"
$vpsUser = "Administrator"
$sshKey = "$env:USERPROFILE\.ssh\id_ed25519_azone"

# Test 1: Network connectivity
Write-Host "Test 1: Checking network connectivity..." -ForegroundColor Yellow
$pingResult = Test-Connection -ComputerName $vpsIP -Count 2 -Quiet

if ($pingResult) {
    Write-Host "✅ Ping successful - Network is reachable" -ForegroundColor Green
} else {
    Write-Host "❌ Ping failed - Network may be blocked" -ForegroundColor Red
    Write-Host "   Try checking:" -ForegroundColor Yellow
    Write-Host "   - VPN is OFF" -ForegroundColor White
    Write-Host "   - AWS Security Group allows your IP" -ForegroundColor White
    Write-Host "   - VPS is running" -ForegroundColor White
}
Write-Host ""

# Test 2: Port 22 connectivity
Write-Host "Test 2: Checking SSH port (22)..." -ForegroundColor Yellow
$portTest = Test-NetConnection -ComputerName $vpsIP -Port 22 -WarningAction SilentlyContinue

if ($portTest.TcpTestSucceeded) {
    Write-Host "✅ Port 22 is open and accessible" -ForegroundColor Green
} else {
    Write-Host "❌ Port 22 is not accessible" -ForegroundColor Red
    Write-Host "   Possible issues:" -ForegroundColor Yellow
    Write-Host "   - AWS Security Group blocking port 22" -ForegroundColor White
    Write-Host "   - Windows Firewall on VPS blocking port 22" -ForegroundColor White
    Write-Host "   - Network firewall blocking SSH" -ForegroundColor White
}
Write-Host ""

# Test 3: SSH Key exists
Write-Host "Test 3: Checking SSH key..." -ForegroundColor Yellow
if (Test-Path $sshKey) {
    Write-Host "✅ SSH key found: $sshKey" -ForegroundColor Green
} else {
    Write-Host "❌ SSH key not found: $sshKey" -ForegroundColor Red
    Write-Host "   Generate key with: ssh-keygen -t ed25519 -f `"$sshKey`"" -ForegroundColor Yellow
}
Write-Host ""

# Test 4: SSH Connection
Write-Host "Test 4: Testing SSH connection..." -ForegroundColor Yellow
Write-Host "   Attempting connection (this may take 10 seconds)..." -ForegroundColor Cyan

$sshCommand = "ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new -i `"$sshKey`" ${vpsUser}@${vpsIP} echo 'Connection successful'"

try {
    $sshResult = Invoke-Expression $sshCommand 2>&1
    
    if ($LASTEXITCODE -eq 0 -or $sshResult -match "Connection successful") {
        Write-Host "✅ SSH connection successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🎉 You can now connect without VPN!" -ForegroundColor Green
        Write-Host "   Use: ssh azone-vps-direct" -ForegroundColor Cyan
    } else {
        Write-Host "❌ SSH connection failed" -ForegroundColor Red
        Write-Host "   Error details:" -ForegroundColor Yellow
        Write-Host $sshResult -ForegroundColor White
        Write-Host ""
        Write-Host "💡 Troubleshooting:" -ForegroundColor Yellow
        Write-Host "   1. Make sure public key is in VPS authorized_keys" -ForegroundColor White
        Write-Host "   2. Check AWS Security Group allows port 22" -ForegroundColor White
        Write-Host "   3. Verify VPS SSH service is running" -ForegroundColor White
    }
} catch {
    Write-Host "❌ SSH connection error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
