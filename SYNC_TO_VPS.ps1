# Complete Sync Script - Upload All Azone Files to VPS
# This syncs everything from local to VPS

$VPS_IP = "18.138.169.114"
$VPS_USER = "Administrator"
$VPS_PASSWORD = "IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH("
$REMOTE_FOLDER = "~/Azone"
$LOCAL_FOLDER = "C:\Users\User\Desktop\Azone"
$SSH_KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_azone"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔄 Complete VPS Sync - Azone Project" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check SSH key
$useSSHKey = $false
if (Test-Path $SSH_KEY_PATH) {
    Write-Host "✅ SSH key found: $SSH_KEY_PATH" -ForegroundColor Green
    $useSSHKey = $true
} else {
    Write-Host "⚠️  SSH key not found, will use password" -ForegroundColor Yellow
    Write-Host "   Password: $VPS_PASSWORD" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Starting sync..." -ForegroundColor White

# Step 1: Create remote directory
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 1: Creating remote directory..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

$createDirCmd = "mkdir -p $REMOTE_FOLDER; chmod 755 $REMOTE_FOLDER; echo 'DIR_CREATED'"

if ($useSSHKey) {
    $result = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "${VPS_USER}@${VPS_IP}" $createDirCmd 2>&1
} else {
    Write-Host "⚠️  Type password: $VPS_PASSWORD" -ForegroundColor Yellow
    $result = ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $createDirCmd 2>&1
}

if ($result -match "DIR_CREATED" -or $LASTEXITCODE -eq 0) {
    Write-Host "✅ Remote directory ready" -ForegroundColor Green
} else {
    Write-Host "⚠️  Directory creation result: $result" -ForegroundColor Yellow
}

# Step 2: Upload Python files
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 2: Uploading Python files..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

$pythonFiles = @(
    "web_app.py",
    "auth_manager.py",
    "auth_routes.py",
    "bot_db_manager.py",
    "bot_logic_engine.py",
    "bot_templates.py",
    "config.py",
    "db_manager.py",
    "facebook_service.py",
    "gemini_service.py",
    "session_middleware.py",
    "telegram_service.py",
    "start_server.py",
    "reset_password.py",
    "optimize.py"
)

foreach ($file in $pythonFiles) {
    $localPath = Join-Path $LOCAL_FOLDER $file
    if (Test-Path $localPath) {
        Write-Host "   Uploading $file..." -ForegroundColor White -NoNewline
        
        if ($useSSHKey) {
            scp -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH $localPath "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
        } else {
            scp -o StrictHostKeyChecking=accept-new $localPath "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host " ✅" -ForegroundColor Green
        } else {
            Write-Host " ❌" -ForegroundColor Red
        }
    }
}

# Step 3: Upload requirements.txt and config files
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 3: Uploading config files..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

$configFiles = @(
    "requirements.txt",
    "env.example",
    ".gitignore",
    "MASTER_DEPLOY.sh"
)

foreach ($file in $configFiles) {
    $localPath = Join-Path $LOCAL_FOLDER $file
    if (Test-Path $localPath) {
        Write-Host "   Uploading $file..." -ForegroundColor White -NoNewline
        
        if ($useSSHKey) {
            scp -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH $localPath "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
        } else {
            scp -o StrictHostKeyChecking=accept-new $localPath "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/" 2>&1 | Out-Null
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host " ✅" -ForegroundColor Green
        } else {
            Write-Host " ❌" -ForegroundColor Red
        }
    }
}

# Step 4: Upload templates directory
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 4: Uploading templates..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

$templatesPath = Join-Path $LOCAL_FOLDER "templates"
if (Test-Path $templatesPath) {
    Write-Host "   Creating templates directory on VPS..." -ForegroundColor White
    
    $createTemplatesCmd = "mkdir -p ${REMOTE_FOLDER}/templates; echo 'TEMPLATES_DIR_CREATED'"
    if ($useSSHKey) {
        ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "${VPS_USER}@${VPS_IP}" $createTemplatesCmd 2>&1 | Out-Null
    } else {
        ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $createTemplatesCmd 2>&1 | Out-Null
    }
    
    # Upload template files (exclude backups)
    $templateFiles = Get-ChildItem $templatesPath -File | Where-Object { $_.Name -notlike "*.bak" -and $_.Name -notlike "*_bak" }
    
    foreach ($file in $templateFiles) {
        Write-Host "   Uploading templates/$($file.Name)..." -ForegroundColor White -NoNewline
        
        if ($useSSHKey) {
            scp -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH $file.FullName "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/templates/" 2>&1 | Out-Null
        } else {
            scp -o StrictHostKeyChecking=accept-new $file.FullName "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/templates/" 2>&1 | Out-Null
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host " ✅" -ForegroundColor Green
        } else {
            Write-Host " ❌" -ForegroundColor Red
        }
    }
}

# Step 5: Upload static directory
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 5: Uploading static files..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

$staticPath = Join-Path $LOCAL_FOLDER "static"
if (Test-Path $staticPath) {
    Write-Host "   Creating static directory structure on VPS..." -ForegroundColor White
    
    $createStaticCmd = @"
mkdir -p ${REMOTE_FOLDER}/static/css
mkdir -p ${REMOTE_FOLDER}/static/js
echo 'STATIC_DIRS_CREATED'
"@
    
    if ($useSSHKey) {
        ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "${VPS_USER}@${VPS_IP}" $createStaticCmd 2>&1 | Out-Null
    } else {
        ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $createStaticCmd 2>&1 | Out-Null
    }
    
    # Upload static files recursively
    Write-Host "   Uploading static files..." -ForegroundColor White
    
    if ($useSSHKey) {
        scp -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH -r "$staticPath\*" "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/static/" 2>&1 | Out-Null
    } else {
        scp -o StrictHostKeyChecking=accept-new -r "$staticPath\*" "${VPS_USER}@${VPS_IP}:${REMOTE_FOLDER}/static/" 2>&1 | Out-Null
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Static files uploaded" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Some static files may have failed" -ForegroundColor Yellow
    }
}

# Step 6: Set permissions
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 6: Setting permissions..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

$permCmd = @"
cd $REMOTE_FOLDER
chmod +x MASTER_DEPLOY.sh
chmod 644 *.py
chmod 644 templates/*.html
chmod 644 static/**/*
find . -type f -name '*.py' -exec chmod 644 {} \;
find . -type f -name '*.html' -exec chmod 644 {} \;
find . -type f -name '*.css' -exec chmod 644 {} \;
find . -type f -name '*.js' -exec chmod 644 {} \;
echo 'PERMISSIONS_SET'
"@

if ($useSSHKey) {
    $permResult = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "${VPS_USER}@${VPS_IP}" $permCmd 2>&1
} else {
    $permResult = ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $permCmd 2>&1
}

if ($permResult -match "PERMISSIONS_SET" -or $LASTEXITCODE -eq 0) {
    Write-Host "✅ Permissions set" -ForegroundColor Green
} else {
    Write-Host "⚠️  Permission setting had issues" -ForegroundColor Yellow
}

# Step 7: Verify upload
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 7: Verifying upload..." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

$verifyCmd = @'
cd ~/Azone
echo "===KEY_FILES==="
if [ -f web_app.py ]; then echo "✅ web_app.py"; else echo "❌ web_app.py"; fi
if [ -f requirements.txt ]; then echo "✅ requirements.txt"; else echo "❌ requirements.txt"; fi
if [ -f MASTER_DEPLOY.sh ]; then echo "✅ MASTER_DEPLOY.sh"; else echo "❌ MASTER_DEPLOY.sh"; fi
if [ -d templates ]; then echo "✅ templates/"; else echo "❌ templates/"; fi
if [ -d static ]; then echo "✅ static/"; else echo "❌ static/"; fi
echo ""
echo "===FILE_COUNT==="
echo "Python files: $(find . -name '*.py' -type f 2>/dev/null | wc -l)"
echo "HTML files: $(find templates -name '*.html' -type f 2>/dev/null | wc -l)"
echo "Static files: $(find static -type f 2>/dev/null | wc -l)"
echo "VERIFY_DONE"
'@

if ($useSSHKey) {
    $verifyResult = ssh -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH "${VPS_USER}@${VPS_IP}" $verifyCmd 2>&1
} else {
    $verifyResult = ssh -o StrictHostKeyChecking=accept-new "${VPS_USER}@${VPS_IP}" $verifyCmd 2>&1
}

Write-Host $verifyResult
Write-Host ""

# Final summary
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Sync Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Run deployment: powershell -ExecutionPolicy Bypass -File SIMPLE_DEPLOY.ps1" -ForegroundColor White
    Write-Host "   2. Or run directly: ssh ${VPS_USER}@${VPS_IP} 'cd ~/Azone; bash MASTER_DEPLOY.sh'" -ForegroundColor White
Write-Host ""
Write-Host "🌐 After deployment, access at:" -ForegroundColor Green
Write-Host "   http://paing.xyz" -ForegroundColor White
Write-Host '   http://18.138.169.114' -ForegroundColor White
Write-Host ""
