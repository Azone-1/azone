# Step-by-Step Deployment Guide

## ✅ Fixed Syntax Errors
All scripts have been fixed. Use these commands:

## Step 1: SSH Key Setup
```powershell
cd C:\Users\User\Desktop\Azone
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "SETUP_SSH_KEY.ps1"
```
**When password prompt appears, enter:**
```
IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(
```

## Step 2: Sync Files
```powershell
cd C:\Users\User\Desktop\Azone
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "SYNC_TO_VPS.ps1"
```

## Step 3: Deploy
```powershell
cd C:\Users\User\Desktop\Azone
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "SIMPLE_DEPLOY.ps1"
```

## Alternative: Run All at Once
```powershell
cd C:\Users\User\Desktop\Azone
.\RUN_DEPLOYMENT.bat
```

**Note:** Always use `powershell.exe -ExecutionPolicy Bypass -NoProfile -File` to avoid execution policy issues.
