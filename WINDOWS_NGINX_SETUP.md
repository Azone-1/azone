# Windows VPS Nginx Setup Guide

Windows VPS မှာ Nginx reverse proxy setup လုပ်နည်း

---

## 📋 Prerequisites

1. **Nginx for Windows** download လုပ်ပါ
   - Download: http://nginx.org/en/download.html
   - Extract to: `C:\nginx`

2. **Flask app** port 5000 မှာ run နေရမယ်

---

## 🔧 Nginx Configuration

### Step 1: Nginx Config File Edit လုပ်ပါ

File: `C:\nginx\conf\nginx.conf`

```nginx
server {
    listen 80;
    server_name paing.xyz www.paing.xyz;

    # Redirect www to non-www
    if ($host = 'www.paing.xyz') {
        return 301 http://paing.xyz$request_uri;
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90;
    }
}
```

**Note:** Windows VPS မှာ port 5000 သုံးပါ (Linux config က 8000 သုံးထားတယ်)

---

## 🚀 Nginx Start လုပ်နည်း

### Method 1: Command Line
```powershell
cd C:\nginx
start nginx
```

### Method 2: Windows Service (Recommended)
```powershell
# Install as Windows Service using NSSM
# Download NSSM from: https://nssm.cc/download

# Install service
nssm install nginx "C:\nginx\nginx.exe"

# Start service
nssm start nginx
```

---

## ✅ Verify

1. **Check Nginx Status:**
   ```powershell
   Get-Process nginx
   ```

2. **Test in Browser:**
   - `http://paing.xyz`
   - `http://18.138.169.114`

---

## 🔄 Restart Nginx

```powershell
cd C:\nginx
nginx -s reload
```

---

## ⚠️ Windows Firewall

Port 80 ကို allow လုပ်ပါ:

```powershell
New-NetFirewallRule -DisplayName "Nginx HTTP" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow
```

---

## 📝 Alternative: IIS Reverse Proxy (Windows Native)

Windows VPS မှာ IIS သုံးလို့ရတယ်:

1. **IIS** install လုပ်ပါ
2. **Application Request Routing (ARR)** install လုပ်ပါ
3. **URL Rewrite** install လုပ်ပါ
4. Reverse proxy rule setup လုပ်ပါ

---

## 🌐 DNS Check

DNS propagation check လုပ်ပါ:

```powershell
.\DNS_CHECK.ps1
```

Or manual:
```powershell
nslookup paing.xyz 1.1.1.1
nslookup paing.xyz 8.8.8.8
```

---

**Note:** Windows VPS မှာ Nginx သို့မဟုတ် IIS reverse proxy သုံးနိုင်တယ်။ Systemd service file က Linux only ဖြစ်တယ်။

