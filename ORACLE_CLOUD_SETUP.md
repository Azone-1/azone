# Oracle Cloud Free Tier Setup Guide

## 🎯 Oracle Cloud Always Free - Complete Setup

### Step 1: Account Registration

1. https://www.oracle.com/cloud/free/ သို့ သွားပါ
2. "Start for Free" button ကို နှိပ်ပါ
3. Account information ဖြည့်ပါ:
   - Email address
   - Password
   - Country: Myanmar
   - Phone number
4. Credit card information ထည့်ပါ:
   - **Important**: Credit card က verification အတွက်သာ (charge မလုပ်ဘူး)
   - Always Free resources က free forever
5. Email verification လုပ်ပါ

---

### Step 2: Create Always Free VM

1. Oracle Cloud Console → "Create a VM Instance"
2. **Image**: Oracle Linux 8
3. **Shape**: VM.Standard.A1.Flex (Always Free)
   - OCPUs: 4
   - Memory: 24 GB
4. **Networking**: 
   - Public IP: Assign a public IPv4 address
   - SSH keys: Generate new key pair (download private key)
5. **Create** button ကို နှိပ်ပါ

---

### Step 3: SSH Connection

**Windows PowerShell မှာ:**

```powershell
# SSH key permission သတ်မှတ်ရန်
icacls "C:\Users\User\Downloads\ssh-key-xxxxx.key" /inheritance:r
icacls "C:\Users\User\Downloads\ssh-key-xxxxx.key" /grant "$env:USERNAME:(R)"

# SSH connection
ssh -i "C:\Users\User\Downloads\ssh-key-xxxxx.key" opc@your-vps-ip
```

**Note:** `opc` က Oracle Cloud default user ဖြစ်ပါတယ်

---

### Step 4: Install Dependencies

```bash
# Update system
sudo yum update -y

# Install Python 3.11
sudo yum install python3.11 python3.11-pip git -y

# Install firewall tools
sudo yum install firewalld -y
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Open port 5000
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

---

### Step 5: Deploy Project

```bash
# Clone project (or upload via SCP)
git clone https://github.com/yourusername/azone.git
cd azone

# Install dependencies
pip3.11 install -r requirements.txt

# Create .env file
nano .env
```

`.env` file content:
```
DOMAIN=yourdomain.tk
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
```

---

### Step 6: Setup SSL Certificate (HTTPS)

```bash
# Install Certbot
sudo yum install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.tk -d www.yourdomain.tk

# Auto-renewal
sudo certbot renew --dry-run
```

---

### Step 7: Run Project with PM2 (Background)

```bash
# Install PM2
sudo npm install -g pm2

# Run project
pm2 start web_app.py --interpreter python3.11 --name azone

# Auto-start on boot
pm2 startup
pm2 save
```

---

### Step 8: Domain Configuration

**Freenom Domain Manager:**
1. Login → My Domains → Manage Domain
2. "Manage Freenom DNS"
3. Add A Record:
   ```
   Type: A
   Name: @
   Target: Your Oracle Cloud VPS IP
   TTL: 3600
   ```

---

## 💰 Cost

**Always Free Resources:**
- 2 VMs (AMD or ARM)
- 4 ARM-based OCPUs
- 24 GB memory
- 200 GB storage
- **Total: $0/month forever**

---

## ✅ Advantages

1. **Free Forever**: No time limit
2. **Powerful**: 4 cores, 24GB RAM
3. **Full Control**: Root access
4. **Custom Domain**: Full support
5. **HTTPS**: Let's Encrypt SSL

---

## 🔧 Troubleshooting

### SSH Connection Failed:
- Check Security List (firewall rules)
- Add Inbound Rule: SSH (port 22) from 0.0.0.0/0

### Port 5000 Not Accessible:
- Check firewall: `sudo firewall-cmd --list-ports`
- Add port: `sudo firewall-cmd --permanent --add-port=5000/tcp`

### SSL Certificate Failed:
- Check domain DNS (A record)
- Wait 24 hours after DNS change
- Check port 80 is open (for verification)

---

## 🎯 Recommendation

Oracle Cloud Free Tier က:
- ✅ Powerful resources
- ✅ Forever free
- ✅ Full control
- ✅ Best for production

**Best for:** Advanced users who want full control
