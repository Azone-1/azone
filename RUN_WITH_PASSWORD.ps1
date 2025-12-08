# Helper script to run SSH/SCP commands with automatic password entry
# Uses Plink (PuTTY) if available, otherwise uses expect-like approach

param(
    [string]$Command,
    [string]$Password = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(",
    [string]$VPS_IP = "18.138.169.114",
    [string]$VPS_USER = "Administrator"
)

# Check if Plink is available
$plinkPath = Get-Command plink -ErrorAction SilentlyContinue

if ($plinkPath) {
    # Use Plink with password
    $plinkCmd = $Command -replace "ssh ", ""
    & plink -ssh -pw $Password "${VPS_USER}@${VPS_IP}" $plinkCmd
} else {
    # Use standard SSH (will prompt for password)
    Write-Host "⚠️  Plink not found. Password will need to be entered manually." -ForegroundColor Yellow
    Write-Host "   Password: $Password" -ForegroundColor Cyan
    Invoke-Expression $Command
}
