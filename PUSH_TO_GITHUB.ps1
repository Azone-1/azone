# Push AZone files to GitHub (ဖိုင်တွေ update လုပ်ပြီး push လုပ်ရန်)
# Run this script whenever you update files

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Push AZone Files to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "⚠ Git not initialized. Initializing..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git initialized" -ForegroundColor Green
}

# Check current status
Write-Host "[1/4] Checking Git status..." -ForegroundColor Yellow
git status --short

# Add all files
Write-Host ""
Write-Host "[2/4] Adding all files..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green

# Commit
Write-Host ""
Write-Host "[3/4] Committing changes..." -ForegroundColor Yellow
$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Update AZone files - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}
git commit -m $commitMessage
Write-Host "✓ Changes committed" -ForegroundColor Green

# Check if remote exists
Write-Host ""
Write-Host "[4/4] Checking remote repository..." -ForegroundColor Yellow
$remoteExists = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ No remote repository configured" -ForegroundColor Yellow
    $setupRemote = Read-Host "Do you want to add remote repository? (y/n)"
    if ($setupRemote -eq 'y' -or $setupRemote -eq 'Y') {
        $repoUrl = Read-Host "Enter GitHub repository URL (e.g., https://github.com/Apaing9611-arch/azone.git)"
        git remote add origin $repoUrl
        Write-Host "✓ Remote repository added" -ForegroundColor Green
    } else {
        Write-Host "✗ Cannot push without remote repository" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ Remote repository: $remoteExists" -ForegroundColor Green
}

# Push to GitHub
Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✓ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "If Railway is connected, it will auto-deploy in 2-3 minutes!" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "✗ Push failed. Check error above." -ForegroundColor Red
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  - No internet connection" -ForegroundColor Gray
    Write-Host "  - GitHub authentication required" -ForegroundColor Gray
    Write-Host "  - Branch name mismatch (try: git push -u origin main)" -ForegroundColor Gray
}

Write-Host ""
