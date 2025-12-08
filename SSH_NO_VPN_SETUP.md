# VPN မလိုဘဲ VPS ချိတ်ဆက်နည်း

## 🎯 ရည်ရွယ်ချက်
VPN မလိုဘဲ VPS (18.138.169.114) ကို ချိတ်ဆက်ရန်

---

## ✅ နည်းလမ်း ၁: Alternative SSH Port သုံးရန် (အလွယ်ဆုံး)

### VPS မှာ (RDP နဲ့ ဝင်ပြီး):

```powershell
# PowerShell (Administrator) မှာ run ပါ
# Port 2222 (သို့မဟုတ် အခြား port) ကို ဖွင့်ရန်

# Firewall rule ထည့်ရန်
New-NetFirewallRule -Name "SSH-Alt-Port" -DisplayName "SSH Alternative Port" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 2222

# SSH config ကို port 2222 သုံးအောင် ပြင်ရန်
# C:\ProgramData\ssh\sshd_config file ကို notepad နဲ့ ဖွင့်ပါ
notepad C:\ProgramData\ssh\sshd_config
```

`sshd_config` file ထဲမှာ:
```
Port 22
Port 2222
```

ထည့်ပြီး service restart လုပ်ပါ:
```powershell
Restart-Service sshd
```

### Local Machine မှာ:

SSH config file ကို update လုပ်ပါ:
```
Host azone-vps
    HostName 18.138.169.114
    User Administrator
    Port 2222
    IdentityFile C:\Users\User\.ssh\id_ed25519_azone
    StrictHostKeyChecking accept-new
```

---

## ✅ နည်းလမ်း ၂: SSH Tunnel/Proxy သုံးရန်

### Local Machine PowerShell မှာ:

```powershell
# SSH tunnel ဖန်တီးရန် (port 2222 ကို local port 2222 နဲ့ tunnel)
ssh -L 2222:localhost:22 Administrator@18.138.169.114 -i C:\Users\User\.ssh\id_ed25519_azone

# သို့မဟုတ် SOCKS proxy သုံးရန်
ssh -D 1080 Administrator@18.138.169.114 -i C:\Users\User\.ssh\id_ed25519_azone
```

---

## ✅ နည်းလမ်း ၃: AWS Security Group ကို ပြင်ရန်

AWS Console မှာ:

1. **EC2 Dashboard** → **Security Groups**
2. VPS ရဲ့ Security Group ကို ရွေးပါ
3. **Inbound Rules** → **Edit inbound rules**
4. **Add rule:**
   - Type: SSH
   - Port: 22
   - Source: `0.0.0.0/0` (သို့မဟုတ် သင့်ရဲ့ IP address)
   - Description: "Allow SSH from anywhere"

ဒါက VPN မလိုဘဲ ချိတ်ဆက်နိုင်အောင် လုပ်ပေးပါတယ်။

---

## ✅ နည်းလမ်း ၄: RDP Tunnel သုံးရန်

RDP နဲ့ ဝင်ပြီး PowerShell မှာ:

```powershell
# Local machine မှာ SSH server စတင်ရန် (VPS မှာ)
Start-Service sshd

# Local machine က SSH config မှာ:
Host azone-vps-direct
    HostName 18.138.169.114
    User Administrator
    Port 22
    IdentityFile C:\Users\User\.ssh\id_ed25519_azone
    ProxyCommand none
    StrictHostKeyChecking no
```

---

## ✅ နည်းလမ်း ၅: Cloudflare Tunnel (အဆင့်မြင့်)

Cloudflare Tunnel သုံးပြီး VPN မလိုဘဲ ချိတ်ဆက်နိုင်ပါတယ်။

---

## 🔧 SSH Config File ကို Update လုပ်ရန်

Local machine မှာ `C:\Users\User\.ssh\config` file ကို ဖွင့်ပြီး:

```
# VPN မလိုဘဲ ချိတ်ဆက်ရန်
Host azone-vps-no-vpn
    HostName 18.138.169.114
    User Administrator
    Port 22
    IdentityFile C:\Users\User\.ssh\id_ed25519_azone
    StrictHostKeyChecking accept-new
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
    Compression yes
    # Connection timeout
    ConnectTimeout 10
```

---

## 🧪 စမ်းသပ်ရန်

```powershell
# Test connection
ssh azone-vps-no-vpn

# သို့မဟုတ်
ssh -v azone-vps-no-vpn
```

`-v` flag က verbose mode ဖြစ်ပြီး connection details တွေ ပြပေးပါတယ်။

---

## ⚠️ သတိထားရမည့်အချက်များ

1. **Security Group**: AWS Security Group မှာ port 22 ဖွင့်ထားရမည်
2. **Firewall**: VPS Windows Firewall မှာ port 22 (သို့မဟုတ် alternative port) ဖွင့်ထားရမည်
3. **IP Whitelist**: လိုအပ်ရင် specific IP addresses ကို whitelist လုပ်နိုင်ပါတယ်
4. **SSH Key**: Public key ကို VPS `authorized_keys` file ထဲမှာ ထည့်ထားရမည်

---

## 📝 Quick Fix Script

PowerShell script ကို run လုပ်ရန်:

```powershell
# Test connection without VPN
Test-NetConnection -ComputerName 18.138.169.114 -Port 22

# SSH connection test
ssh -o ConnectTimeout=10 Administrator@18.138.169.114 -i C:\Users\User\.ssh\id_ed25519_azone
```

---

## ✅ အကြံပြုထားသော နည်းလမ်း

**အလွယ်ဆုံး**: AWS Security Group ကို update လုပ်ပြီး `0.0.0.0/0` ကို allow လုပ်ပါ (temporary testing အတွက်)

**အန္တရာယ်ကင်းဆုံး**: Alternative SSH port (2222) သုံးပြီး Security Group မှာ specific IP addresses ကို whitelist လုပ်ပါ
