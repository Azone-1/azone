# Cleanup Unnecessary Files for VPS
# This removes documentation, old scripts, and temporary files

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🧹 Cleaning Up Unnecessary Files" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$deletedCount = 0
$keptCount = 0

# Files to KEEP (Essential for VPS)
$keepFiles = @(
    "web_app.py",
    "requirements.txt",
    "README.md",
    "MASTER_DEPLOY.sh",
    "SETUP_SSH_KEY.ps1",
    "SIMPLE_DEPLOY.ps1",
    "DEPLOY_INSTRUCTIONS.md"
)

# Patterns to DELETE
$deletePatterns = @(
    "*.md",           # All markdown except README.md
    "*.ps1",          # PowerShell scripts (except essential ones)
    "*.sh",           # Shell scripts (except MASTER_DEPLOY.sh)
    "*.txt",          # Text files (except requirements.txt)
    "*.bat",          # Batch files
    "*.log",          # Log files
    "*.bak*",         # Backup files
    "test_*.py",      # Test files
    "check_*.ps1",    # Check scripts
    "check_*.sh",     # Check scripts
    "QUICK_*.ps1",    # Quick scripts
    "QUICK_*.sh",     # Quick scripts
    "QUICK_*.md",     # Quick guides
    "FIX_*.ps1",      # Fix scripts
    "FIX_*.md",       # Fix guides
    "DEPLOY_*.ps1",   # Old deploy scripts
    "DEPLOY_*.sh",    # Old deploy scripts (except MASTER)
    "DEPLOY_*.md",    # Old deploy guides
    "VPS_*.ps1",      # VPS PowerShell scripts
    "VPS_*.sh",       # VPS shell scripts (except MASTER)
    "VPS_*.md",       # VPS guides
    "CURSOR_*.ps1",   # Cursor scripts
    "CURSOR_*.md",    # Cursor guides
    "AUTO_*.ps1",     # Auto scripts
    "UPLOAD_*.ps1",   # Upload scripts
    "DELETE_*.ps1",   # Delete scripts
    "SETUP_*.ps1",    # Setup scripts (except SETUP_SSH_KEY)
    "setup-*.ps1",    # Setup scripts
    "deploy-*.ps1",   # Deploy scripts
    "deploy-*.sh",    # Deploy scripts
    "run-*.ps1",      # Run scripts
    "upload-*.ps1",   # Upload scripts
    "cursor-*.ps1",   # Cursor scripts
    "cursor-*.sh",    # Cursor scripts
    "*.html",         # HTML files (if not in templates)
    "*.js",           # JS files (if not in static)
    "*.css",          # CSS files (if not in static)
    "*.db.bak*"       # Database backups
)

Write-Host "Step 1: Deleting unnecessary documentation files..." -ForegroundColor Yellow

# Delete all .md files except README.md and DEPLOY_INSTRUCTIONS.md
Get-ChildItem -Path . -Filter "*.md" -File | ForEach-Object {
    if ($_.Name -notin @("README.md", "DEPLOY_INSTRUCTIONS.md")) {
        Remove-Item $_.FullName -Force
        $deletedCount++
        Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
    } else {
        $keptCount++
        Write-Host "   ✅ Kept: $($_.Name)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Step 2: Deleting unnecessary PowerShell scripts..." -ForegroundColor Yellow

# Delete .ps1 files except essential ones
Get-ChildItem -Path . -Filter "*.ps1" -File | ForEach-Object {
    if ($_.Name -notin @("SETUP_SSH_KEY.ps1", "SIMPLE_DEPLOY.ps1")) {
        Remove-Item $_.FullName -Force
        $deletedCount++
        Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
    } else {
        $keptCount++
        Write-Host "   ✅ Kept: $($_.Name)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Step 3: Deleting unnecessary shell scripts..." -ForegroundColor Yellow

# Delete .sh files except MASTER_DEPLOY.sh
Get-ChildItem -Path . -Filter "*.sh" -File | ForEach-Object {
    if ($_.Name -ne "MASTER_DEPLOY.sh") {
        Remove-Item $_.FullName -Force
        $deletedCount++
        Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
    } else {
        $keptCount++
        Write-Host "   ✅ Kept: $($_.Name)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Step 4: Deleting text files..." -ForegroundColor Yellow

# Delete .txt files except requirements.txt
Get-ChildItem -Path . -Filter "*.txt" -File | ForEach-Object {
    if ($_.Name -ne "requirements.txt") {
        Remove-Item $_.FullName -Force
        $deletedCount++
        Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
    } else {
        $keptCount++
        Write-Host "   ✅ Kept: $($_.Name)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Step 5: Deleting batch files..." -ForegroundColor Yellow

Get-ChildItem -Path . -Filter "*.bat" -File | ForEach-Object {
    Remove-Item $_.FullName -Force
    $deletedCount++
    Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Step 6: Deleting log files..." -ForegroundColor Yellow

Get-ChildItem -Path . -Filter "*.log" -File | ForEach-Object {
    Remove-Item $_.FullName -Force
    $deletedCount++
    Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Step 7: Deleting backup files..." -ForegroundColor Yellow

Get-ChildItem -Path . -Filter "*.bak*" -File | ForEach-Object {
    Remove-Item $_.FullName -Force
    $deletedCount++
    Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Step 8: Deleting test files..." -ForegroundColor Yellow

Get-ChildItem -Path . -Filter "test_*.py" -File | ForEach-Object {
    Remove-Item $_.FullName -Force
    $deletedCount++
    Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Step 9: Cleaning __pycache__..." -ForegroundColor Yellow

if (Test-Path "__pycache__") {
    Remove-Item "__pycache__" -Recurse -Force
    $deletedCount++
    Write-Host "   ❌ Deleted: __pycache__/" -ForegroundColor Red
}

Write-Host ""
Write-Host "Step 10: Cleaning root HTML/JS/CSS files..." -ForegroundColor Yellow

Get-ChildItem -Path . -Filter "*.html" -File | Where-Object { $_.Name -notlike "*template*" } | ForEach-Object {
    Remove-Item $_.FullName -Force
    $deletedCount++
    Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
}

Get-ChildItem -Path . -Filter "*.js" -File | Where-Object { $_.FullName -notlike "*static*" } | ForEach-Object {
    Remove-Item $_.FullName -Force
    $deletedCount++
    Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
}

Get-ChildItem -Path . -Filter "*.css" -File | Where-Object { $_.FullName -notlike "*static*" } | ForEach-Object {
    Remove-Item $_.FullName -Force
    $deletedCount++
    Write-Host "   ❌ Deleted: $($_.Name)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Cleanup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Yellow
Write-Host "   Deleted: $deletedCount files" -ForegroundColor Red
Write-Host "   Kept: $keptCount essential files" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Essential files kept:" -ForegroundColor Yellow
Write-Host "   ✅ web_app.py" -ForegroundColor Green
Write-Host "   ✅ requirements.txt" -ForegroundColor Green
Write-Host "   ✅ MASTER_DEPLOY.sh" -ForegroundColor Green
Write-Host "   ✅ SETUP_SSH_KEY.ps1" -ForegroundColor Green
Write-Host "   ✅ SIMPLE_DEPLOY.ps1" -ForegroundColor Green
Write-Host "   ✅ README.md" -ForegroundColor Green
Write-Host "   ✅ DEPLOY_INSTRUCTIONS.md" -ForegroundColor Green
Write-Host "   ✅ All Python files (*.py)" -ForegroundColor Green
Write-Host "   ✅ templates/ folder" -ForegroundColor Green
Write-Host "   ✅ static/ folder" -ForegroundColor Green
Write-Host "   ✅ Database files (*.db)" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Project is now clean and ready for VPS!" -ForegroundColor Cyan
Write-Host ""

