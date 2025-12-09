#!/bin/bash
# Quick VPS Setup Script for AZone
# Run: bash QUICK_VPS_SETUP.sh

set -e

echo "========================================="
echo "🚀 AZone Quick VPS Setup"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get project directory
PROJECT_DIR="${1:-$HOME/Azone}"
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}⚠️  Project directory not found: $PROJECT_DIR${NC}"
    echo "Creating directory..."
    mkdir -p "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

echo -e "${GREEN}📋 Step 1: System Update${NC}"
sudo apt update && sudo apt upgrade -y
echo "✅ System updated"
echo ""

echo -e "${GREEN}📋 Step 2: Install Python & Dependencies${NC}"
sudo apt install -y python3 python3-pip python3-venv git curl

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Python dependencies installed"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found, installing basic packages...${NC}"
    pip install flask flask-login werkzeug
fi
echo ""

echo -e "${GREEN}📋 Step 3: Install Node.js & PM2${NC}"
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

if ! command -v pm2 &> /dev/null; then
    sudo npm install -g pm2
fi
echo "✅ PM2 installed: $(pm2 --version)"
echo ""

echo -e "${GREEN}📋 Step 4: Initialize Database${NC}"
if [ -f "db_manager.py" ]; then
    python3 -c "import db_manager; db_manager.init_database()" || echo "⚠️  Database init failed"
    echo "✅ Database initialized"
else
    echo -e "${YELLOW}⚠️  db_manager.py not found${NC}"
fi
echo ""

echo -e "${GREEN}📋 Step 5: Create .env File${NC}"
if [ ! -f ".env" ]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    cat > .env <<EOF
SECRET_KEY=$SECRET_KEY
GEMINI_API_KEY=AIzaSyD8Zki9uebkYj_WgvsXjwmMnx_P3VvySB0
DEBUG=False
HOST=0.0.0.0
PORT=5000
DOMAIN=localhost
EOF
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi
echo ""

echo -e "${GREEN}📋 Step 6: Start Flask App with PM2${NC}"
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
echo "Setting up PM2 startup..."
pm2 startup systemd -u $USER --hp $HOME | grep "sudo" | bash || echo "⚠️  PM2 startup setup skipped"

echo "✅ Flask app running with PM2"
echo ""

echo -e "${GREEN}📋 Step 7: Install Nginx${NC}"
if ! command -v nginx &> /dev/null; then
    sudo apt install -y nginx
fi

# Get server IP or domain
SERVER_NAME="${2:-_}"
if [ "$SERVER_NAME" = "_" ]; then
    SERVER_NAME=$(curl -s ifconfig.me || hostname -I | awk '{print $1}')
fi

# Create Nginx config
NGINX_CONFIG="/etc/nginx/sites-available/azone"
sudo tee "$NGINX_CONFIG" > /dev/null <<NGINX_EOF
server {
    listen 80;
    listen [::]:80;
    server_name $SERVER_NAME;

    access_log /var/log/nginx/azone.access.log;
    error_log /var/log/nginx/azone.error.log;

    location / {
        proxy_pass http://127.0.0.1:5000;
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
        alias $PROJECT_DIR/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
NGINX_EOF

# Enable site
sudo rm -f /etc/nginx/sites-enabled/default
if [ ! -L /etc/nginx/sites-enabled/azone ]; then
    sudo ln -s "$NGINX_CONFIG" /etc/nginx/sites-enabled/
fi

# Test and restart
if sudo nginx -t; then
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    echo "✅ Nginx configured and running"
else
    echo -e "${YELLOW}⚠️  Nginx configuration error!${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}📋 Step 8: Configure Firewall${NC}"
if command -v ufw &> /dev/null; then
    sudo ufw allow 22/tcp comment "SSH" 2>/dev/null || true
    sudo ufw allow 80/tcp comment "HTTP"
    sudo ufw allow 443/tcp comment "HTTPS"
    echo "✅ Firewall configured"
else
    echo -e "${YELLOW}⚠️  UFW not found${NC}"
fi
echo ""

echo "========================================="
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo "========================================="
echo ""
echo "📊 PM2 Status:"
pm2 status
echo ""
echo "🌐 Access your app:"
echo "  ✅ http://$SERVER_NAME"
echo "  ✅ http://localhost:5000 (Direct Flask)"
echo ""
echo "📝 Useful Commands:"
echo "  pm2 logs azone-bot      # View logs"
echo "  pm2 restart azone-bot   # Restart app"
echo "  pm2 status              # Check status"
echo "  sudo nginx -t            # Test Nginx config"
echo ""
echo "🔒 To setup SSL (optional):"
echo "  sudo apt install certbot python3-certbot-nginx"
echo "  sudo certbot --nginx -d YOUR_DOMAIN"
echo ""
