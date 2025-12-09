# Auto Login Guide

## Login Credentials
- **Username:** `admin`
- **Password:** `admin123`

## Quick Steps

1. Browser မှာ login form ကို fill in လုပ်ပါ:
   - Username: `admin`
   - Password: `admin123`

2. "ဝင်ရောက်ရန်" button ကို click လုပ်ပါ

3. Login အောင်မြင်ရင် `/dashboard` ကို automatically redirect ဖြစ်သွားမယ်

## Alternative: Direct URL After Login

Login ဝင်ပြီးရင် browser address bar မှာ:
```
http://localhost:5000/dashboard
```
သို့မဟုတ်
```
http://localhost:5000/
```

## If Admin User Doesn't Exist

Run this to create admin user:
```bash
python -c "import bot_db_manager; from werkzeug.security import generate_password_hash; bot_db_manager.init_bot_database(); conn = bot_db_manager.get_bot_db_connection(); cursor = conn.cursor(); cursor.execute('INSERT OR IGNORE INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)', ('admin', 'admin@azone.com', generate_password_hash('admin123'), 'owner')); conn.commit(); conn.close(); print('Admin user created!')"
```
