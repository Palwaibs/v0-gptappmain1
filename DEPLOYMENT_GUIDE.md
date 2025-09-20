# 🚀 Panduan Deploy ChatGPT Plus Order System

## 📋 Prerequisites yang Dibutuhkan

### **1. Akun & Services:**
- ✅ Domain & Hosting (sudah ada)
- 🔑 **ChatGPT Team Account** ($25-30/bulan)
- 💳 **Midtrans Account** (Payment Gateway)
- 📧 **SendGrid Account** (Email Service)
- 🗄️ **PostgreSQL Database** (bisa dari hosting atau cloud)
- 🔴 **Redis Server** (untuk background tasks)

### **2. Technical Requirements:**
- **Frontend**: Node.js 18+, npm
- **Backend**: Python 3.9+, pip
- **Database**: PostgreSQL 14+
- **Cache**: Redis 6+
- **Browser**: Chrome/Chromium (untuk automation)

---

## 🏗️ Setup Step by Step

### **STEP 1: Setup ChatGPT Team Account**

1. **Beli ChatGPT Team:**
   - Kunjungi: https://chatgpt.com/team
   - Subscribe plan Team ($25-30/bulan)
   - Anda akan jadi Admin workspace

2. **Catat Kredensial:**
   \`\`\`
   Email Admin: your-admin@domain.com
   Password: your-secure-password
   Admin URL: https://chatgpt.com/admin?tab=members
   \`\`\`

### **STEP 2: Setup Payment Gateway (Midtrans)**

1. **Daftar Midtrans:**
   - Kunjungi: https://midtrans.com
   - Daftar akun merchant
   - Verifikasi dokumen bisnis

2. **Dapatkan API Keys:**
   \`\`\`
   Server Key: SB-Mid-server-xxx (sandbox) / Mid-server-xxx (production)
   Client Key: SB-Mid-client-xxx (sandbox) / Mid-client-xxx (production)
   \`\`\`

### **STEP 3: Setup Email Service (SendGrid)**

1. **Daftar SendGrid:**
   - Kunjungi: https://sendgrid.com
   - Daftar free account (100 email/hari gratis)

2. **Buat API Key:**
   - Dashboard → Settings → API Keys
   - Create API Key dengan Full Access
   - Catat API Key: `SG.xxx`

### **STEP 4: Setup Database & Redis**

#### **Option A: Cloud Services (Recommended)**
\`\`\`bash
# PostgreSQL (Supabase/Railway/PlanetScale)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis (Upstash/Railway)
REDIS_URL=redis://user:pass@host:6379
\`\`\`

#### **Option B: VPS/Dedicated Server**
\`\`\`bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Install Redis
sudo apt install redis-server

# Create database
sudo -u postgres createdb chatgpt_orders
\`\`\`

---

## 📁 Upload Files ke Hosting

### **1. Upload via FTP/cPanel:**
\`\`\`
public_html/
├── frontend/          # React build files
├── backend/           # Python Flask app
├── .env              # Environment variables
└── requirements.txt   # Python dependencies
\`\`\`

### **2. File Structure di Server:**
\`\`\`
/home/yourdomain/
├── frontend/
│   ├── dist/         # Built React app
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── tasks.py
│   ├── automation/
│   └── utils/
└── .env
\`\`\`

---

## ⚙️ Configuration Files

### **1. Frontend Environment (.env)**
\`\`\`env
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
\`\`\`

### **2. Backend Environment (backend/.env)**
\`\`\`env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/chatgpt_orders

# Flask
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production

# Midtrans Payment
MIDTRANS_SERVER_KEY=your-midtrans-server-key
MIDTRANS_CLIENT_KEY=your-midtrans-client-key
MIDTRANS_IS_PRODUCTION=true

# ChatGPT Admin
CHATGPT_ADMIN_EMAIL=your-admin@domain.com
CHATGPT_ADMIN_PASSWORD=your-admin-password
CHATGPT_ADMIN_URL=https://chatgpt.com/admin?tab=members

# Redis
REDIS_URL=redis://host:6379/0

# Email
SENDGRID_API_KEY=SG.your-sendgrid-api-key
FROM_EMAIL=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com

# Security
WEBHOOK_SECRET=your-webhook-secret
ALLOWED_WEBHOOK_IPS=103.10.128.0/22,103.10.129.0/22

# Chrome/Selenium
SELENIUM_HEADLESS=true
SELENIUM_TIMEOUT=30
\`\`\`

---

## 🚀 Deployment Process

### **1. Build Frontend:**
\`\`\`bash
# Di local computer
cd frontend
npm install
npm run build

# Upload folder 'dist' ke public_html
\`\`\`

### **2. Setup Backend:**
\`\`\`bash
# Di server (SSH/Terminal)
cd backend
pip install -r requirements.txt

# Setup database
python -c "from app import create_app, init_database; app = create_app(); init_database(app)"

# Test backend
python app.py
\`\`\`

### **3. Setup Web Server (Apache/Nginx):**

#### **Apache (.htaccess):**
\`\`\`apache
# Frontend (React Router)
RewriteEngine On
RewriteBase /
RewriteRule ^index\.html$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]

# API Proxy to Backend
RewriteRule ^api/(.*)$ http://localhost:5000/api/$1 [P,L]
\`\`\`

#### **Nginx:**
\`\`\`nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    # Frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
\`\`\`

### **4. Setup Background Tasks (Celery):**
\`\`\`bash
# Install supervisor untuk manage processes
sudo apt install supervisor

# Create config file: /etc/supervisor/conf.d/chatgpt-celery.conf
[program:chatgpt-worker]
command=/path/to/venv/bin/celery -A celery_worker.celery worker --loglevel=info
directory=/path/to/backend
user=www-data
autostart=true
autorestart=true

[program:chatgpt-beat]
command=/path/to/venv/bin/celery -A celery_worker.celery beat --loglevel=info
directory=/path/to/backend
user=www-data
autostart=true
autorestart=true

# Start services
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
\`\`\`

---

## 🔧 Testing & Troubleshooting

### **1. Test Components:**
\`\`\`bash
# Test database connection
python -c "from models import db; print('DB OK' if db else 'DB Error')"

# Test Redis connection
redis-cli ping

# Test email service
python -c "from utils.email_service import get_email_service; print('Email OK')"

# Test payment gateway
python -c "from utils.payment_gateway import get_payment_gateway; print('Payment OK')"
\`\`\`

### **2. Common Issues:**

#### **Database Connection Error:**
\`\`\`bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection string
psql "postgresql://user:pass@host:5432/dbname"
\`\`\`

#### **Redis Connection Error:**
\`\`\`bash
# Check Redis status
sudo systemctl status redis

# Test connection
redis-cli -h host -p 6379 ping
\`\`\`

#### **Selenium/Chrome Issues:**
\`\`\`bash
# Install Chrome on server
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable

# Install ChromeDriver
pip install webdriver-manager
\`\`\`

---

## 📊 Monitoring & Maintenance

### **1. Log Files:**
\`\`\`bash
# Application logs
tail -f /var/log/chatgpt-orders.log

# Celery logs
tail -f /var/log/celery-worker.log

# Web server logs
tail -f /var/log/apache2/error.log
tail -f /var/log/nginx/error.log
\`\`\`

### **2. Database Backup:**
\`\`\`bash
# Daily backup script
#!/bin/bash
pg_dump "postgresql://user:pass@host:5432/chatgpt_orders" > backup_$(date +%Y%m%d).sql

# Add to crontab
0 2 * * * /path/to/backup-script.sh
\`\`\`

### **3. Health Checks:**
- **Frontend**: https://yourdomain.com
- **Backend API**: https://yourdomain.com/api/health
- **Celery Monitor**: Install Flower untuk monitoring

---

## 💰 Cost Estimation

### **Monthly Costs:**
- **ChatGPT Team**: $25-30 (base workspace)
- **ChatGPT Members**: $20/member/month
- **Hosting**: $10-50 (tergantung traffic)
- **Database**: $10-25 (cloud PostgreSQL)
- **Redis**: $5-15 (cloud Redis)
- **SendGrid**: Free (100 emails/day)
- **Midtrans**: 2.9% per transaction

### **Revenue Model:**
- **Jual**: Rp 25,000/member/month
- **Cost**: ~$20/member/month
- **Margin**: Tergantung exchange rate & volume

---

## 🚨 Security Checklist

- ✅ HTTPS/SSL Certificate
- ✅ Environment variables (tidak di public)
- ✅ Database password yang kuat
- ✅ Webhook signature verification
- ✅ Rate limiting pada API
- ✅ Input validation & sanitization
- ✅ Regular security updates

---

## 📞 Support & Maintenance

### **Regular Tasks:**
1. **Monitor logs** untuk error
2. **Backup database** harian
3. **Update dependencies** bulanan
4. **Monitor member count** untuk billing
5. **Check automation** berjalan normal

### **Emergency Contacts:**
- **Midtrans Support**: support@midtrans.com
- **SendGrid Support**: support@sendgrid.com
- **ChatGPT Support**: help.openai.com

---

Apakah ada bagian tertentu yang ingin dijelaskan lebih detail?
