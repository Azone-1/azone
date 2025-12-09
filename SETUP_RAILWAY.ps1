# AZone Railway.app Deployment Setup Script
# Run this script to prepare for Railway deployment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AZone Railway Deployment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "[1/5] Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git initialized" -ForegroundColor Green
} else {
    Write-Host "[1/5] Git repository already initialized" -ForegroundColor Green
}

# Check for .env file
if (-not (Test-Path .env)) {
    Write-Host "[2/5] Creating .env file from env.example..." -ForegroundColor Yellow
    Copy-Item env.example .env
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host "⚠ Please edit .env file and add your API keys!" -ForegroundColor Yellow
} else {
    Write-Host "[2/5] .env file already exists" -ForegroundColor Green
}

# Check for Procfile
if (Test-Path Procfile) {
    Write-Host "[3/5] Procfile exists" -ForegroundColor Green
} else {
    Write-Host "[3/5] Creating Procfile..." -ForegroundColor Yellow
    "web: python web_app.py" | Out-File -FilePath Procfile -Encoding utf8
    Write-Host "✓ Procfile created" -ForegroundColor Green
}

# Check for railway.json
if (Test-Path railway.json) {
    Write-Host "[4/5] railway.json exists" -ForegroundColor Green
} else {
    Write-Host "[4/5] Creating railway.json..." -ForegroundColor Yellow
    @"
{
  `"`$schema`": `"https://railway.app/railway.schema.json`",
  `"build`": {
    `"builder`": `"NIXPACKS`"
  },
  `"deploy`": {
    `"startCommand`": `"python web_app.py`",
    `"restartPolicyType`": `"ON_FAILURE`",
    `"restartPolicyMaxRetries`": 10
  }
}
"@ | Out-File -FilePath railway.json -Encoding utf8
    Write-Host "✓ railway.json created" -ForegroundColor Green
}

# Check for .gitignore
if (Test-Path .gitignore) {
    Write-Host "[5/5] .gitignore exists" -ForegroundColor Green
} else {
    Write-Host "[5/5] Creating .gitignore..." -ForegroundColor Yellow
    # Create basic .gitignore
    @"
# Python
__pycache__/
*.py[cod]
.env

# Database
*.db

# Logs
*.log
"@ | Out-File -FilePath .gitignore -Encoding utf8
    Write-Host "✓ .gitignore created" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your API keys" -ForegroundColor White
Write-Host "2. Create GitHub repository:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/azone.git" -ForegroundColor Gray
Write-Host "3. Push to GitHub:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Initial commit'" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host "4. Deploy on Railway.app:" -ForegroundColor White
Write-Host "   - Go to https://railway.app" -ForegroundColor Gray
Write-Host "   - New Project → Deploy from GitHub" -ForegroundColor Gray
Write-Host "   - Select your repository" -ForegroundColor Gray
Write-Host ""
Write-Host "See DEPLOY_COMPLETE.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""
