# VPS Account Lockout Fix Script
# Run this via AWS Systems Manager Session Manager

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🔓 VPS Account Unlock Script" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "   Please run PowerShell as Administrator" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Running as Administrator" -ForegroundColor Green
Write-Host ""

# Step 1: Check current account lockout policy
Write-Host "Step 1: Checking current account lockout policy..." -ForegroundColor Yellow
$accounts = net accounts
Write-Host $accounts -ForegroundColor Cyan
Write-Host ""

# Step 2: Disable account lockout (temporarily)
Write-Host "Step 2: Disabling account lockout..." -ForegroundColor Yellow
net accounts /lockoutthreshold:0
Start-Sleep -Seconds 2

# Step 3: Set lockout duration to 0
Write-Host "Step 3: Setting lockout duration to 0..." -ForegroundColor Yellow
net accounts /lockoutduration:0
Start-Sleep -Seconds 2

# Step 4: Ensure Administrator account is active
Write-Host "Step 4: Ensuring Administrator account is active..." -ForegroundColor Yellow
net user Administrator /active:yes
Start-Sleep -Seconds 2

# Step 5: Verify changes
Write-Host "Step 5: Verifying changes..." -ForegroundColor Yellow
$accountsAfter = net accounts
Write-Host $accountsAfter -ForegroundColor Cyan
Write-Host ""

# Step 6: Check Administrator account status
Write-Host "Step 6: Checking Administrator account status..." -ForegroundColor Yellow
$adminStatus = net user Administrator
Write-Host $adminStatus -ForegroundColor Cyan
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Account Unlock Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Try RDP connection again" -ForegroundColor White
Write-Host "   2. If still locked, wait 5 minutes and try again" -ForegroundColor White
Write-Host ""
Write-Host "💡 Recommendation:" -ForegroundColor Yellow
Write-Host "   For better security, set lockout threshold to 10-15:" -ForegroundColor White
Write-Host "   net accounts /lockoutthreshold:10" -ForegroundColor Cyan
Write-Host "   net accounts /lockoutduration:30" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
