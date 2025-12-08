# VPN မလိုဘဲ VPS ချိတ်ဆက်ရန် Setup Script
# Run this script on VPS (via RDP) to configure SSH for direct access

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🔧 VPN-Free SSH Setup for VPS" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "   Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Running as Administrator" -ForegroundColor Green
Write-Host ""

# Step 1: Ensure OpenSSH Server is installed and running
Write-Host "Step 1: Checking OpenSSH Server..." -ForegroundColor Yellow
$sshService = Get-Service -Name sshd -ErrorAction SilentlyContinue

if (-not $sshService) {
    Write-Host "   Installing OpenSSH Server..." -ForegroundColor Cyan
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
}

if ($sshService.Status -ne 'Running') {
    Write-Host "   Starting SSH service..." -ForegroundColor Cyan
    Start-Service sshd
    Set-Service -Name sshd -StartupType Automatic
}

Write-Host "✅ OpenSSH Server is running" -ForegroundColor Green
Write-Host ""

# Step 2: Configure Firewall for SSH
Write-Host "Step 2: Configuring Firewall..." -ForegroundColor Yellow

# Check if firewall rule exists
$firewallRule = Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue

if (-not $firewallRule) {
    Write-Host "   Creating firewall rule for port 22..." -ForegroundColor Cyan
    New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -DisplayName "OpenSSH Server (sshd)" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
} else {
    Write-Host "   Firewall rule already exists" -ForegroundColor Cyan
    # Ensure it's enabled
    Enable-NetFirewallRule -Name "OpenSSH-Server-In-TCP"
}

# Optional: Add alternative port (2222) for testing
Write-Host "   Adding alternative port 2222..." -ForegroundColor Cyan
$altPortRule = Get-NetFirewallRule -Name "SSH-Alt-Port-2222" -ErrorAction SilentlyContinue
if (-not $altPortRule) {
    New-NetFirewallRule -Name "SSH-Alt-Port-2222" -DisplayName "SSH Alternative Port 2222" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 2222
}

Write-Host "✅ Firewall configured" -ForegroundColor Green
Write-Host ""

# Step 3: Configure SSH to accept connections from anywhere
Write-Host "Step 3: Configuring SSH settings..." -ForegroundColor Yellow

$sshConfigPath = "C:\ProgramData\ssh\sshd_config"
$sshConfigBackup = "$sshConfigPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Backup existing config
if (Test-Path $sshConfigPath) {
    Copy-Item $sshConfigPath $sshConfigBackup
    Write-Host "   Backup created: $sshConfigBackup" -ForegroundColor Cyan
}

# Read current config
$configContent = Get-Content $sshConfigPath -Raw

# Ensure Port 22 is enabled
if ($configContent -notmatch "^\s*Port\s+22") {
    $configContent = "Port 22`n" + $configContent
}

# Add alternative port 2222
if ($configContent -notmatch "^\s*Port\s+2222") {
    $configContent = $configContent + "`nPort 2222"
}

# Ensure PasswordAuthentication is enabled (for initial setup)
if ($configContent -notmatch "^\s*PasswordAuthentication") {
    $configContent = $configContent + "`nPasswordAuthentication yes"
}

# Ensure PubkeyAuthentication is enabled
if ($configContent -notmatch "^\s*PubkeyAuthentication") {
    $configContent = $configContent + "`nPubkeyAuthentication yes"
}

# Save updated config
Set-Content -Path $sshConfigPath -Value $configContent -NoNewline
Write-Host "✅ SSH configuration updated" -ForegroundColor Green
Write-Host ""

# Step 4: Restart SSH service
Write-Host "Step 4: Restarting SSH service..." -ForegroundColor Yellow
Restart-Service sshd
Start-Sleep -Seconds 2

if ((Get-Service sshd).Status -eq 'Running') {
    Write-Host "✅ SSH service restarted successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: SSH service may not be running properly" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Display connection information
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Connection Information:" -ForegroundColor Yellow
Write-Host "   IP Address: 18.138.169.114" -ForegroundColor White
Write-Host "   Port: 22 (or 2222 for alternative)" -ForegroundColor White
Write-Host "   User: Administrator" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Make sure your public key is in:" -ForegroundColor White
Write-Host "      C:\Users\Administrator\.ssh\authorized_keys" -ForegroundColor Cyan
Write-Host ""
Write-Host "   2. On local machine, test connection:" -ForegroundColor White
Write-Host "      ssh azone-vps-direct" -ForegroundColor Cyan
Write-Host ""
Write-Host "   3. If connection fails, check AWS Security Group:" -ForegroundColor White
Write-Host "      - Go to AWS Console → EC2 → Security Groups" -ForegroundColor Cyan
Write-Host "      - Add Inbound Rule: SSH (port 22) from 0.0.0.0/0" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
