#!/bin/bash
# Master Deployment Script - Complete VPS Setup
# This does EVERYTHING: PM2 + Nginx + SSL + Firewall
# Run on VPS: bash MASTER_DEPLOY.sh

set -e

echo "========================================="
echo "MASTER VPS DEPLOYMENT - Complete Setup"
echo "========================================="
echo ""

# Variables
PROJECT_DIR="$HOME/Azone"
if [ ! -d "$PROJECT_DIR" ]; then
    mkdir -p "$PROJECT_DIR"
fi
cd "$PROJECT_DIR"

# ============================================
# STEP 1: SYSTEM UPDATES
# ============================================
echo "📋 Step 1: Updating system..."
sudo apt update
sudo apt upgrade -y
echo "   ✅ System updated"
echo ""

# ============================================
# STEP 2: INSTALL PYTHON & DEPENDENCIES
# ============================================
echo "📋 Step 2: Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --quiet
    echo "   ✅ Python dependencies installed"
else
    echo "   ⚠️  requirements.txt not found"
fi
echo ""

# ============================================
# STEP 3: INSTALL NODE.JS & PM2
# ============================================
echo "📋 Step 3: Installing Node.js and PM2..."

if ! command -v node &> /dev/null; then
    echo "   Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi
echo "   ✅ Node.js: $(node --version)"

if ! command -v pm2 &> /dev/null; then
    echo "   Installing PM2..."
    sudo npm install -g pm2
fi
echo "   ✅ PM2: $(pm2 --version)"
echo ""

# ============================================
# STEP 4: START FLASK APP WITH PM2
# ============================================
echo "📋 Step 4: Starting Flask app with PM2..."

# Stop existing process
pm2 stop azone-bot 2>/dev/null || true
pm2 delete azone-bot 2>/dev/null || true

# Create logs directory
mkdir -p "$PROJECT_DIR/logs"

# Start with PM2
pm2 start web_app.py \
    --name "azone-bot" \
    --interpreter python3 \
    --cwd "$PROJECT_DIR" \
    --log "$PROJECT_DIR/logs/pm2.log" \
    --error "$PROJECT_DIR/logs/pm2-error.log" \
    --output "$PROJECT_DIR/logs/pm2-out.log" \
    --time \
    --restart-delay=3000 \
    --max-restarts=10 \
    --min-uptime=10000

pm2 save

# Setup PM2 startup
echo "   Setting up PM2 startup..."
pm2 startup systemd -u $USER --hp $HOME | grep "sudo" | bash || true

echo "   ✅ Flask app running with PM2"
echo ""

# ============================================
# STEP 5: INSTALL & CONFIGURE NGINX
# ============================================
echo "📋 Step 5: Installing and configuring Nginx..."

if ! command -v nginx &> /dev/null; then
    sudo apt install -y nginx
fi

# Create Nginx config
NGINX_CONFIG="/etc/nginx/sites-available/paing.xyz"
sudo tee "$NGINX_CONFIG" > /dev/null <<NGINX_EOF
server {
    listen 80;
    listen [::]:80;
    server_name paing.xyz www.paing.xyz;

    access_log /var/log/nginx/paing.xyz.access.log;
    error_log /var/log/nginx/paing.xyz.error.log;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static {
        alias ${PROJECT_DIR}/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
NGINX_EOF

# Enable site
sudo rm -f /etc/nginx/sites-enabled/default
if [ ! -L /etc/nginx/sites-enabled/paing.xyz ]; then
    sudo ln -s "$NGINX_CONFIG" /etc/nginx/sites-enabled/
fi

# Test and restart
if sudo nginx -t; then
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    echo "   ✅ Nginx configured and running"
else
    echo "   ❌ Nginx configuration error!"
    exit 1
fi
echo ""

# ============================================
# STEP 6: CONFIGURE FIREWALL
# ============================================
echo "📋 Step 6: Configuring firewall..."

if command -v ufw &> /dev/null; then
    sudo ufw allow 22/tcp comment "SSH" 2>/dev/null || true
    sudo ufw allow 80/tcp comment "HTTP"
    sudo ufw allow 443/tcp comment "HTTPS"
    sudo ufw allow 8000/tcp comment "Flask Direct" 2>/dev/null || true
    echo "   ✅ Firewall configured"
else
    echo "   ⚠️  UFW not found"
fi
echo ""

# ============================================
# STEP 7: INSTALL SSL CERTIFICATE
# ============================================
echo "📋 Step 7: Installing SSL certificate..."

if ! command -v certbot &> /dev/null; then
    sudo apt install -y certbot python3-certbot-nginx
fi

echo "   Getting SSL certificate from Let's Encrypt..."
sudo certbot --nginx \
    -d paing.xyz \
    -d www.paing.xyz \
    --non-interactive \
    --agree-tos \
    --redirect \
    -m admin@paing.xyz \
    || {
    echo "   ⚠️  SSL installation failed (OK for now)"
    echo "   You can access via HTTP: http://paing.xyz"
}

echo ""

# ============================================
# FINAL STATUS
# ============================================
echo "========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "========================================="
echo ""

echo "📊 PM2 Status:"
pm2 status
echo ""

echo "📊 Nginx Status:"
sudo systemctl status nginx --no-pager | head -3
echo ""

echo "📊 Listening Ports:"
sudo netstat -tuln | grep -E ":(80|443|8000)" || ss -tuln | grep -E ":(80|443|8000)"
echo ""

echo "========================================="
echo "🌐 ACCESS YOUR BOT:"
echo "========================================="
echo "  ✅ http://paing.xyz (No port number!)"
echo "  ✅ http://18.138.169.114"
if [ -d "/etc/letsencrypt/live/paing.xyz" ]; then
    echo "  ✅ https://paing.xyz (HTTPS)"
fi
echo "  ✅ http://paing.xyz:8000 (Direct Flask)"
echo ""

echo "========================================="
echo "Useful Commands:"
echo "========================================="
echo "  pm2 status"
echo "  pm2 logs azone-bot"
echo "  pm2 restart azone-bot"
echo "  sudo systemctl status nginx"
echo "  sudo tail -f /var/log/nginx/paing.xyz.error.log"
echo ""

