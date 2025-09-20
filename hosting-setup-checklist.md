# ✅ Checklist Setup Hosting untuk aksesgptmurah.tech

## 🎯 Domain: https://aksesgptmurah.tech/

---

## 📋 PERSIAPAN SEBELUM UPLOAD

### **1. Akun yang Harus Disiapkan:**
- [ ] **ChatGPT Team Account** ($25-30/bulan)
  - Email admin: ________________
  - Password: ________________
  - Team URL: https://chatgpt.com/admin?tab=members

- [ ] **Midtrans Account** (Payment Gateway)
  - Server Key: SB-Mid-server-________________
  - Client Key: SB-Mid-client-________________
  - Merchant ID: ________________

- [ ] **SendGrid Account** (Email Service)
  - API Key: SG.________________
  - Verified Sender: noreply@aksesgptmurah.tech

### **2. Hosting Requirements Check:**
- [ ] **PHP Version**: 8.0+ atau Python 3.9+
- [ ] **Database**: MySQL/PostgreSQL available
- [ ] **SSL Certificate**: Installed for HTTPS
- [ ] **File Manager**: cPanel access
- [ ] **SSH Access**: Available (optional)

---

## 📁 UPLOAD FILES

### **1. Download Project Files:**
- [ ] Frontend files (React components)
- [ ] Backend files (Python Flask)
- [ ] Configuration files (.env.example)
- [ ] Documentation files

### **2. Upload Structure:**
\`\`\`
public_html/
├── index.html              ← Frontend entry
├── assets/                 ← CSS/JS files
├── api/                    ← Backend files
│   ├── app.py
│   ├── requirements.txt
│   └── utils/
├── .env                    ← Configuration
└── .htaccess              ← Web server config
\`\`\`

### **3. File Permissions:**
- [ ] Folders: 755 (rwxr-xr-x)
- [ ] Files: 644 (rw-r--r--)
- [ ] .env: 600 (rw-------)

---

## 🗄️ DATABASE SETUP

### **1. Create Database:**
- [ ] Database Name: `aksesgpt_orders`
- [ ] Username: `aksesgpt_user`
- [ ] Password: ________________
- [ ] Host: `localhost`

### **2. Database URL:**
\`\`\`
mysql://aksesgpt_user:PASSWORD@localhost/aksesgpt_orders
\`\`\`

### **3. Import Schema:**
- [ ] Run migration scripts
- [ ] Create required tables
- [ ] Test database connection

---

## ⚙️ CONFIGURATION

### **1. Create .env File:**
\`\`\`env
# Database
DATABASE_URL=mysql://aksesgpt_user:YOUR_PASSWORD@localhost/aksesgpt_orders

# ChatGPT Admin
CHATGPT_ADMIN_EMAIL=admin@aksesgptmurah.tech
CHATGPT_ADMIN_PASSWORD=YOUR_CHATGPT_PASSWORD
CHATGPT_ADMIN_URL=https://chatgpt.com/admin?tab=members

# Midtrans Payment
MIDTRANS_SERVER_KEY=SB-Mid-server-YOUR_KEY
MIDTRANS_CLIENT_KEY=SB-Mid-client-YOUR_KEY
MIDTRANS_IS_PRODUCTION=false

# SendGrid Email
SENDGRID_API_KEY=SG.YOUR_API_KEY
FROM_EMAIL=noreply@aksesgptmurah.tech
ADMIN_EMAIL=admin@aksesgptmurah.tech

# Security
SECRET_KEY=your-super-secret-key-here
WEBHOOK_SECRET=your-webhook-secret
\`\`\`

### **2. Web Server Configuration:**
- [ ] Create .htaccess for Apache
- [ ] Configure URL rewriting
- [ ] Set security headers

---

## 🔧 DEPENDENCIES INSTALLATION

### **1. Python Packages:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### **2. Required Packages:**
- [ ] Flask (web framework)
- [ ] SQLAlchemy (database)
- [ ] Celery (background tasks)
- [ ] Selenium (automation)
- [ ] SendGrid (email)
- [ ] Midtrans (payment)

### **3. System Requirements:**
- [ ] Chrome browser (for automation)
- [ ] Redis server (for Celery)
- [ ] Python 3.9+

---

## 🧪 TESTING

### **1. Frontend Test:**
- [ ] https://aksesgptmurah.tech/ loads
- [ ] Navigation works
- [ ] Package selection works
- [ ] Order form displays

### **2. Backend API Test:**
- [ ] https://aksesgptmurah.tech/api/health returns OK
- [ ] Database connection works
- [ ] Payment gateway connects
- [ ] Email service works

### **3. Full Flow Test:**
- [ ] Create test order
- [ ] Payment process works
- [ ] Email notifications sent
- [ ] ChatGPT invite automation works

---

## 🚀 GO LIVE

### **1. DNS Configuration:**
- [ ] Domain points to hosting server
- [ ] SSL certificate active
- [ ] WWW redirect configured

### **2. Security Setup:**
- [ ] HTTPS enforced
- [ ] Security headers set
- [ ] File permissions correct
- [ ] .env file protected

### **3. Monitoring Setup:**
- [ ] Error logging enabled
- [ ] Email notifications for errors
- [ ] Payment webhook configured
- [ ] Backup schedule set

---

## 📊 BUSINESS SETUP

### **1. Pricing Configuration:**
- [ ] Package prices set in config
- [ ] Midtrans payment amounts match
- [ ] Profit margins calculated

### **2. Customer Communication:**
- [ ] Email templates ready
- [ ] WhatsApp support number active
- [ ] FAQ content updated
- [ ] Terms of service ready

### **3. Operations:**
- [ ] ChatGPT Team workspace ready
- [ ] Admin account configured
- [ ] Member invitation process tested
- [ ] Customer support process defined

---

## 🎉 LAUNCH CHECKLIST

- [ ] All files uploaded and configured
- [ ] Database connected and working
- [ ] Payment gateway tested
- [ ] Email service functional
- [ ] ChatGPT automation working
- [ ] Website accessible via HTTPS
- [ ] All forms and features working
- [ ] Error handling in place
- [ ] Backup system active
- [ ] Monitoring and alerts set

---

## 📞 SUPPORT CONTACTS

### **Technical Issues:**
- Hosting Support: ________________
- Domain Registrar: ________________

### **Service Providers:**
- Midtrans Support: support@midtrans.com
- SendGrid Support: support@sendgrid.com
- ChatGPT Support: help.openai.com

### **Emergency Contacts:**
- Your Phone: ________________
- Backup Admin: ________________

---

**🎯 Target: Website live di https://aksesgptmurah.tech/ dalam 24 jam!**

Print checklist ini dan centang setiap item yang sudah selesai.
