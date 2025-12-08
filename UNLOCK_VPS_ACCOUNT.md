# VPS Account Unlock လုပ်နည်း

## 🔒 ပြဿနာ
RDP account ကို failed login attempts အများကြီးကြောင့် lock လုပ်ထားပါတယ်။

---

## ✅ နည်းလမ်း ၁: စောင့်ရန် (အလွယ်ဆုံး)

Windows default lockout time က **15-30 minutes** ဖြစ်ပါတယ်။

**ဘာလုပ်ရမလဲ:**
1. 15-30 minutes စောင့်ပါ
2. ပြီးရင် RDP ကို ထပ်စမ်းပါ

---

## ✅ နည်းလမ်း ၂: AWS Systems Manager Session Manager (အဆင့်မြင့်)

AWS Console မှာ:

1. **EC2 Dashboard** → **Instances**
2. VPS instance ကို ရွေးပါ
3. **Connect** button ကို နှိပ်ပါ
4. **Session Manager** tab ကို ရွေးပါ
5. **Connect** button ကို နှိပ်ပါ

PowerShell window ပွင့်လာရင်:

```powershell
# Account lockout policy ကို စစ်ရန်
net accounts

# Account lockout duration ကို ပြင်ရန် (0 = never lock)
net accounts /lockoutduration:0

# သို့မဟုတ် specific user account ကို unlock လုပ်ရန်
net user Administrator /active:yes
```

---

## ✅ နည်းလမ်း ၃: AWS EC2 Instance Connect (Browser-based)

AWS Console မှာ:

1. **EC2 Dashboard** → **Instances**
2. VPS instance ကို ရွေးပါ
3. **Connect** button ကို နှိပ်ပါ
4. **EC2 Instance Connect** tab ကို ရွေးပါ
5. **Connect** button ကို နှိပ်ပါ

Browser-based terminal ပွင့်လာရင် PowerShell commands run လုပ်ပါ။

---

## ✅ နည်းလမ်း ၄: Password Reset via AWS Console

1. **EC2 Dashboard** → **Instances**
2. VPS instance ကို right-click → **Get Windows Password**
3. Private key file ကို upload လုပ်ပါ
4. New password ကို generate လုပ်ပါ
5. New password နဲ့ RDP login လုပ်ပါ

**သတိထားရန်:** Instance ကို stop/start လုပ်ရန် လိုအပ်နိုင်ပါတယ်။

---

## ✅ နည်းလမ်း ၅: Account Lockout Policy ကို ပြင်ရန်

AWS Systems Manager Session Manager နဲ့ ဝင်ပြီး:

```powershell
# Local Security Policy ကို ဖွင့်ရန်
secpol.msc

# သို့မဟုတ် PowerShell မှာ:
# Account lockout threshold ကို မြင့်ရန် (သို့မဟုတ် disable)
net accounts /lockoutthreshold:0

# Lockout duration ကို လျှော့ချရန်
net accounts /lockoutduration:0

# Lockout observation window ကို လျှော့ချရန်
net accounts /lockoutwindow:0
```

---

## ✅ နည်းလမ်း ၆: New Admin User ဖန်တီးရန်

AWS Systems Manager Session Manager နဲ့ ဝင်ပြီး:

```powershell
# New admin user ဖန်တီးရန်
net user AdminUser YourNewPassword123! /add
net localgroup Administrators AdminUser /add

# ပြီးရင် new user နဲ့ RDP login လုပ်ပါ
```

---

## 🔧 Quick Fix Script (VPS မှာ Run လုပ်ရန်)

AWS Systems Manager Session Manager နဲ့ ဝင်ပြီး PowerShell မှာ:

```powershell
# Account lockout policy ကို disable လုပ်ရန်
net accounts /lockoutthreshold:0

# Administrator account ကို unlock လုပ်ရန်
net user Administrator /active:yes

# Account lockout duration ကို လျှော့ချရန်
net accounts /lockoutduration:0

# စစ်ဆေးရန်
net accounts
```

---

## 📋 Step-by-Step Guide (အလွယ်ဆုံး)

### Option A: စောင့်ရန် (15-30 minutes)
1. 15-30 minutes စောင့်ပါ
2. RDP ကို ထပ်စမ်းပါ

### Option B: AWS Systems Manager သုံးရန်
1. AWS Console → EC2 → Instances
2. VPS instance ကို ရွေးပါ
3. **Connect** → **Session Manager** → **Connect**
4. PowerShell window ပွင့်လာရင်:
   ```powershell
   net accounts /lockoutthreshold:0
   net user Administrator /active:yes
   ```
5. RDP ကို ထပ်စမ်းပါ

---

## ⚠️ သတိထားရမည့်အချက်များ

1. **Account lockout threshold**: Default က 5 failed attempts ဖြစ်ပါတယ်
2. **Lockout duration**: Default က 30 minutes ဖြစ်ပါတယ်
3. **Security**: Account lockout policy ကို disable လုပ်ရင် security risk ရှိပါတယ်
4. **Best Practice**: Account lockout threshold ကို 10-15 အထိ မြင့်ထားပါ (0 မဟုတ်)

---

## 🎯 အကြံပြုထားသော နည်းလမ်း

**အလွယ်ဆုံး**: 15-30 minutes စောင့်ပြီး RDP ကို ထပ်စမ်းပါ

**အမြန်ဆုံး**: AWS Systems Manager Session Manager သုံးပြီး account lockout policy ကို ပြင်ပါ

**အန္တရာယ်ကင်းဆုံး**: Account lockout threshold ကို 10-15 အထိ မြင့်ထားပါ (disable မလုပ်ပါ)
