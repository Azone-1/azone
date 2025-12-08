# VPN Deployment Guide - Azone Project

## ⚠️ Important: VPN Requirements

Your VPS requires VPN to be connected. Follow these steps carefully.

## 📋 Deployment Steps

### Before Starting:
1. **Turn ON VPN** - Make sure VPN is connected and stable
2. **Check VPN Status** - Wait 10-15 seconds after connecting
3. **Keep VPN ON** - Do NOT turn off VPN during deployment

### Step 1: Run Deployment
```powershell
.\DEPLOY_SIMPLE.bat
```

### Step 2: When Password Prompt Appears
Password: `IL3KuNuXji2WlgrgpYMoJz.v(Tp=NvH(`

**Copy and paste this password when asked!**

### Step 3: Keep VPN ON
- **DO NOT** turn off VPN during deployment
- Deployment takes 5-10 minutes
- If VPN disconnects, deployment will fail

## 🔧 Troubleshooting

### Connection Reset Error
If you see "Connection reset by 18.138.169.114 port 22":

1. **Check VPN:**
   - Make sure VPN is ON
   - Wait 10 seconds for VPN to stabilize
   - Try again

2. **Check VPS Status:**
   - EC2 instance should be running
   - SSH port 22 should be open
   - Security group allows your IP

3. **Retry:**
   - Close and reopen VPN
   - Wait 15 seconds
   - Run `.\DEPLOY_SIMPLE.bat` again

### VPN Keeps Disconnecting
- Use a stable VPN connection
- Avoid switching VPN servers during deployment
- Consider using SSH key (run `SETUP_SSH_KEY.ps1` first)

## ✅ After Deployment

Once deployment completes:
- VPN can be turned off
- Access your app: http://paing.xyz
- Or: http://18.138.169.114

## 🔑 Setup SSH Key (Recommended)

To avoid password prompts and VPN issues:

```powershell
powershell.exe -ExecutionPolicy Bypass -NoProfile -File SETUP_SSH_KEY.ps1
```

This will:
- Generate SSH key
- Copy to VPS (enter password ONCE)
- After this, no more passwords needed!

Then use:
```powershell
.\QUICK_FIX.ps1
```

## 📝 Notes

- **VPN is required** for initial connection
- **EC2 instance** must be running
- **Keep VPN ON** during entire deployment process
- **Password** will be shown clearly in script output
