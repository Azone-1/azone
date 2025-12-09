# Sync Local Code to VPS
# This script syncs your local AZone code to VPS via Git
# Run from local PC: .\SYNC_TO_VPS.ps1

Write-Host "=========================================" -ForegroundColor Green
Write-Host "🚀 AZone Local to VPS Sync" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if Git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git not found!" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Get current directory
$LOCAL_DIR = Get-Location
Write-Host "📁 Local Directory: $LOCAL_DIR" -ForegroundColor Cyan

# Check if this is a Git repository
if (-not (Test-Path ".git")) {
    Write-Host ""
    Write-Host "⚠️  Not a Git repository. Initializing..." -ForegroundColor Yellow
    
    # Check if remote exists
    $remoteUrl = git remote get-url origin 2>$null
    if (-not $remoteUrl) {
        Write-Host "❌ No Git remote found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please choose:" -ForegroundColor Yellow
        Write-Host "  1. Initialize Git and push to GitHub" -ForegroundColor White
        Write-Host "  2. Use manual copy method (see DEPLOY_VIA_RDP.md)" -ForegroundColor White
        Write-Host ""
        $choice = Read-Host "Enter choice (1 or 2)"
        
        if ($choice -eq "1") {
            Write-Host ""
            Write-Host "📋 Initializing Git repository..." -ForegroundColor Cyan
            git init
            Write-Host "Enter GitHub repository URL:" -ForegroundColor Yellow
            $repoUrl = Read-Host "Repository URL"
            git remote add origin $repoUrl
            Write-Host "✅ Git initialized" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "📋 Manual Copy Instructions:" -ForegroundColor Cyan
            Write-Host "  1. ZIP your local folder: $LOCAL_DIR" -ForegroundColor White
            Write-Host "  2. RDP to VPS (18.138.169.114)" -ForegroundColor White
            Write-Host "  3. Copy ZIP to C:\Azone" -ForegroundColor White
            Write-Host "  4. Extract and run: .\WINDOWS_VPS_SETUP.ps1" -ForegroundColor White
            exit 0
        }
    }
}

Write-Host ""
Write-Host "📋 Step 1: Checking Git status..." -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "📋 Step 2: Staging changes..." -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "📋 Step 3: Committing changes..." -ForegroundColor Cyan
$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Sync to VPS - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}
git commit -m $commitMessage

Write-Host ""
Write-Host "📋 Step 4: Pushing to GitHub..." -ForegroundColor Cyan
$branch = git branch --show-current
Write-Host "Current branch: $branch" -ForegroundColor Yellow

try {
    git push origin $branch
    Write-Host "✅ Code pushed to GitHub successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Push failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Trying to set upstream..." -ForegroundColor Yellow
    git push -u origin $branch
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "✅ LOCAL SYNC COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps on VPS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. RDP to VPS (18.138.169.114)" -ForegroundColor White
Write-Host "2. Open PowerShell as Administrator" -ForegroundColor White
Write-Host "3. Run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "   cd C:\Azone" -ForegroundColor Yellow
Write-Host "   git pull origin $branch" -ForegroundColor Yellow
Write-Host "   python web_app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or run the setup script:" -ForegroundColor White
Write-Host "   .\WINDOWS_VPS_SETUP.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 After sync, access Bot Builder at:" -ForegroundColor Cyan
Write-Host "   http://18.138.169.114:5000/bot-builder" -ForegroundColor Green
Write-Host ""
