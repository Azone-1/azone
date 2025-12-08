# Railway.app Deployment Guide (အလွယ်ဆုံး)

## 🚀 Railway.app နဲ့ Deploy လုပ်နည်း

### Step 1: Account ဖန်တီးရန်

1. https://railway.app/ သို့ သွားပါ
2. "Start a New Project" button ကို နှိပ်ပါ
3. GitHub account နဲ့ login လုပ်ပါ
4. Railway က GitHub access permission မေးရင် "Authorize" လုပ်ပါ

---

### Step 2: Project Deploy လုပ်ရန်

1. Railway dashboard မှာ "New Project" button ကို နှိပ်ပါ
2. "Deploy from GitHub repo" option ကို ရွေးပါ
3. Your Azone repository ကို search လုပ်ပြီး select လုပ်ပါ
4. Railway automatically detect လုပ်ပါမယ်:
   - Python project
   - `requirements.txt` file
   - `web_app.py` entry point

---

### Step 3: Environment Variables ထည့်ရန်

Railway dashboard → Your project → Variables tab:

```
DOMAIN=yourdomain.tk
USE_HTTPS=True
PORT=5000
HOST=0.0.0.0
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
```

**Important:** `DOMAIN` variable က webhook URL အတွက် အရေးကြီးပါတယ်!

---

### Step 4: Custom Domain ထည့်ရန်

1. Railway dashboard → Your project → Settings
2. "Domains" section → "Add Domain"
3. Custom domain ထည့်ပါ: `yourdomain.tk`
4. Railway က DNS records ပေးပါမယ်:
   ```
   Type: CNAME
   Name: @
   Value: your-project.up.railway.app
   ```

5. Freenom domain manager မှာ:
   - Login → My Domains → Manage Domain
   - "Manage Freenom DNS" → Add Record
   - Type: CNAME
   - Name: @
   - Target: `your-project.up.railway.app`
   - TTL: 3600
   - Save

6. Wait 5-10 minutes for DNS propagation

---

### Step 5: Verify Deployment

1. Railway dashboard → Your project → Deployments
2. Latest deployment က "Active" status ဖြစ်ရမယ်
3. Browser မှာ `https://yourdomain.tk` ကို ဖွင့်ပါ
4. Login page ပေါ်ရင် successful!

---

### Step 6: Webhook URL Test

Facebook webhook URL:
```
https://yourdomain.tk/webhook/facebook
```

Test လုပ်ရန်:
```bash
curl "https://yourdomain.tk/webhook/facebook?hub.mode=subscribe&hub.verify_token=azone_bot_verify_token&hub.challenge=test123"
```

Response: `test123` ပြန်ရမယ်

---

## 📋 Railway.app Features

✅ **Automatic HTTPS**: SSL certificate automatic
✅ **Auto-deploy**: GitHub push လုပ်ရင် auto deploy
✅ **Free tier**: $5 credit/month
✅ **Custom domain**: Free subdomain + custom domain
✅ **Environment variables**: Easy configuration
✅ **Logs**: Real-time logs viewing

---

## 💰 Cost

- **Free tier**: $5 credit/month
- **Usage**: ~500 hours/month free
- **Over limit**: Pay as you go

**Your Flask app**: ~$0-2/month (free tier နဲ့ လုံလောက်ပါတယ်)

---

## 🔧 Troubleshooting

### Deployment Failed:
1. Check logs: Railway dashboard → Deployments → View logs
2. Check `requirements.txt` file
3. Check environment variables

### Domain Not Working:
1. Check DNS records (CNAME)
2. Wait 10-15 minutes for DNS propagation
3. Check Railway domain settings

### Webhook Not Working:
1. Check `DOMAIN` environment variable
2. Check HTTPS (must be https://)
3. Check Facebook webhook configuration

---

## ✅ Advantages

1. **Easy**: GitHub integration, auto-deploy
2. **Free**: $5 credit/month
3. **HTTPS**: Automatic SSL
4. **Custom domain**: Easy setup
5. **No server management**: Railway handles everything

---

## 🎯 Next Steps

1. Deploy to Railway
2. Add custom domain
3. Configure environment variables
4. Test webhook URL
5. Update Facebook webhook settings

Done! 🎉
