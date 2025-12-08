# Test Syntax - Verify all scripts are correct
Write-Host "Testing script syntax..." -ForegroundColor Cyan

$scripts = @("SETUP_SSH_KEY.ps1", "SYNC_TO_VPS.ps1", "SIMPLE_DEPLOY.ps1")

foreach ($script in $scripts) {
    Write-Host "`nChecking $script..." -ForegroundColor Yellow
    $errors = $null
    $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content $script -Raw), [ref]$errors)
    
    if ($errors.Count -eq 0) {
        Write-Host "  ✅ $script - Syntax OK" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $script - Syntax Errors:" -ForegroundColor Red
        $errors | ForEach-Object { Write-Host "    Line $($_.Token.StartLine): $($_.Message)" -ForegroundColor Red }
    }
}

Write-Host "`n✅ Syntax check complete!" -ForegroundColor Green
