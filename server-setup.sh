#!/bin/bash

# ChatGPT Plus Order System - Server Setup Script
# Run this script on your server after uploading files

echo "🚀 ChatGPT Plus Order System - Server Setup"
echo "============================================"

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and Node.js
echo "🐍 Installing Python 3.9+..."
sudo apt install python3 python3-pip python3-venv -y

echo "📦 Installing Node.js 18+..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install PostgreSQL
echo "🗄️ Installing PostgreSQL..."
sudo apt install postgresql postgresql-contrib -y

# Install Redis
echo "🔴 Installing Redis..."
sudo apt install redis-server -y

# Install Chrome for Selenium
echo "🌐 Installing Google Chrome..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable -y

# Install Supervisor for process management
echo "⚙️ Installing Supervisor..."
sudo apt install supervisor -y

# Create project directories
echo "📁 Creating project directories..."
mkdir -p /home/chatgpt-orders/{frontend,backend,logs,screenshots}

# Setup Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd /home/chatgpt-orders/backend
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies (after you upload requirements.txt)
echo "📦 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found. Please upload it first."
fi

# Setup database
echo "🗄️ Setting up database..."
sudo -u postgres createdb chatgpt_orders
sudo -u postgres psql -c "CREATE USER chatgpt_user WITH PASSWORD 'chatgpt_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE chatgpt_orders TO chatgpt_user;"

# Start services
echo "🚀 Starting services..."
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl start redis
sudo systemctl enable redis

# Create systemd service files
echo "⚙️ Creating service files..."

# Flask app service
sudo tee /etc/systemd/system/chatgpt-api.service > /dev/null <<EOF
[Unit]
Description=ChatGPT Plus Order System API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/chatgpt-orders/backend
Environment=PATH=/home/chatgpt-orders/backend/venv/bin
ExecStart=/home/chatgpt-orders/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Celery worker service
sudo tee /etc/systemd/system/chatgpt-worker.service > /dev/null <<EOF
[Unit]
Description=ChatGPT Celery Worker
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/chatgpt-orders/backend
Environment=PATH=/home/chatgpt-orders/backend/venv/bin
ExecStart=/home/chatgpt-orders/backend/venv/bin/celery -A celery_worker.celery worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Celery beat service
sudo tee /etc/systemd/system/chatgpt-beat.service > /dev/null <<EOF
[Unit]
Description=ChatGPT Celery Beat
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/chatgpt-orders/backend
Environment=PATH=/home/chatgpt-orders/backend/venv/bin
ExecStart=/home/chatgpt-orders/backend/venv/bin/celery -A celery_worker.celery beat --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data /home/chatgpt-orders
sudo chmod +x /home/chatgpt-orders/backend/app.py

# Reload systemd
sudo systemctl daemon-reload

echo "✅ Server setup completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Upload your project files to /home/chatgpt-orders/"
echo "2. Create .env file with your configuration"
echo "3. Run: sudo systemctl start chatgpt-api"
echo "4. Run: sudo systemctl start chatgpt-worker"
echo "5. Run: sudo systemctl start chatgpt-beat"
echo ""
echo "🔍 Check status with:"
echo "sudo systemctl status chatgpt-api"
echo "sudo systemctl status chatgpt-worker"
echo "sudo systemctl status chatgpt-beat"
