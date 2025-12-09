# CRM Dashboard Test Guide

## ပြောင်းလဲမှုတွေ မြင်ရအောင်

### 1. Server Restart လုပ်ပါ
```bash
python web_app.py
```

### 2. Browser မှာ URL ကို စစ်ဆေးပါ
- **CRM Dashboard:** `http://localhost:5000/` သို့မဟုတ် `http://localhost:5000/dashboard`
- **Bot Builder:** `http://localhost:5000/bot-builder`

### 3. Browser Cache Clear လုပ်ပါ
- **Chrome/Edge:** `Ctrl + Shift + Delete` → Cached images and files → Clear
- **သို့မဟုတ်** `Ctrl + F5` (Hard Refresh)

### 4. Console ကို စစ်ဆေးပါ
- Browser မှာ `F12` နှိပ်ပါ
- Console tab ကို ဖွင့်ပါ
- အောက်ပါ messages တွေ မြင်ရမယ်:
  - "DOM loaded, initializing dashboard..."
  - "Loading dashboard stats..."
  - "Dashboard stats result: ..."

### 5. Database ကို စစ်ဆေးပါ
```bash
python -c "import db_manager; db_manager.init_database(); print('OK')"
```

## ဘာတွေ ပြောင်းလဲသွားလဲ?

✅ **Database Schema** - leads, customers, projects tables created
✅ **Backend APIs** - All API routes connected to database
✅ **Frontend JavaScript** - Data loading functions added
✅ **Routes** - `/` and `/dashboard` now show CRM dashboard

## မမြင်ရသေးရင်

1. Server restart လုပ်ပါ
2. Browser cache clear လုပ်ပါ
3. Console errors ကို စစ်ဆေးပါ
4. URL ကို စစ်ဆေးပါ (`/` သို့မဟုတ် `/dashboard`)
