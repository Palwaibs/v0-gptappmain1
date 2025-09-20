# 🚀 Panduan Deploy ChatGPT Plus Order System untuk Pemula

## Domain Anda: https://aksesgptmurah.tech/

---

## 📋 PERSIAPAN AWAL (Yang Harus Anda Siapkan)

### **1. Akun-Akun yang Dibutuhkan:**

#### **A. ChatGPT Team Account (WAJIB)**
- **Website**: https://chatgpt.com/team
- **Biaya**: $25-30/bulan
- **Fungsi**: Sebagai admin untuk invite customer
- **Cara Daftar**:
  1. Buka https://chatgpt.com/team
  2. Klik "Subscribe to Team"
  3. Isi data dan bayar
  4. Anda akan jadi admin workspace
- **Yang Dicatat**: Email & password admin

#### **B. Midtrans Account (Payment Gateway)**
- **Website**: https://midtrans.com
- **Biaya**: Gratis (fee 2.9% per transaksi)
- **Fungsi**: Terima pembayaran dari customer
- **Cara Daftar**:
  1. Buka https://midtrans.com
  2. Klik "Daftar Sekarang"
  3. Isi form bisnis
  4. Upload dokumen (KTP, NPWP, dll)
  5. Tunggu verifikasi (1-3 hari)
- **Yang Dicatat**: Server Key & Client Key

#### **C. SendGrid Account (Email Service)**
- **Website**: https://sendgrid.com
- **Biaya**: Gratis (100 email/hari)
- **Fungsi**: Kirim email konfirmasi ke customer
- **Cara Daftar**:
  1. Buka https://sendgrid.com
  2. Klik "Start for Free"
  3. Verifikasi email
  4. Buat API Key di dashboard
- **Yang Dicatat**: API Key

---

## 🗄️ SETUP DATABASE & HOSTING

### **1. Cek Hosting Anda**
Login ke **cPanel** hosting Anda dan pastikan ada:
- ✅ **PHP 8.0+** atau **Python 3.9+**
- ✅ **MySQL/PostgreSQL Database**
- ✅ **File Manager**
- ✅ **SSH Access** (optional tapi sangat membantu)

### **2. Buat Database**
1. **Login cPanel** → **MySQL Databases**
2. **Create Database**: `aksesgpt_orders`
3. **Create User**: `aksesgpt_user`
4. **Password**: Buat password kuat
5. **Add User to Database** → **All Privileges**
6. **Catat**: Database name, username, password

---

## 📁 DOWNLOAD & UPLOAD FILES

### **1. Download Project Files**
Saya akan buatkan file ZIP untuk Anda:

**Frontend Files (React):**
- `package.json`
- `index.html`
- `src/` folder (semua components)
- `public/` folder

**Backend Files (Python):**
- `backend/app.py`
- `backend/requirements.txt`
- `backend/models.py`
- `backend/config.py`
- Semua folder `backend/`

### **2. Upload ke Hosting**
1. **Login cPanel** → **File Manager**
2. **Navigate** ke `public_html/`
3. **Upload** file ZIP project
4. **Extract** file ZIP
5. **Structure** harus seperti ini:
\`\`\`
public_html/
├── index.html          (Frontend)
├── assets/             (CSS, JS files)
├── api/                (Backend files)
│   ├── app.py
│   ├── requirements.txt
│   └── ...
└── .env                (Configuration)
\`\`\`

---

## ⚙️ KONFIGURASI ENVIRONMENT

### **1. Buat File .env**
Di folder `public_html/`, buat file `.env`:

\`\`\`env
# Database Configuration
DATABASE_URL=mysql://aksesgpt_user:your_password@localhost/aksesgpt_orders

# ChatGPT Admin (Ganti dengan akun Anda)
CHATGPT_ADMIN_EMAIL=admin@aksesgptmurah.tech
CHATGPT_ADMIN_PASSWORD=your_chatgpt_password
CHATGPT_ADMIN_URL=https://chatgpt.com/admin?tab=members

# Midtrans Payment (Ganti dengan API key Anda)
MIDTRANS_SERVER_KEY=SB-Mid-server-xxx
MIDTRANS_CLIENT_KEY=SB-Mid-client-xxx
MIDTRANS_IS_PRODUCTION=false

# SendGrid Email (Ganti dengan API key Anda)
SENDGRID_API_KEY=SG.xxx
FROM_EMAIL=noreply@aksesgptmurah.tech

# Admin Notifications
ADMIN_EMAIL=admin@aksesgptmurah.tech

# Security
SECRET_KEY=your-super-secret-key-here
WEBHOOK_SECRET=your-webhook-secret

# Redis (Jika hosting support)
REDIS_URL=redis://localhost:6379/0
\`\`\`

### **2. Ganti Semua "xxx" dengan Data Asli Anda!**

---

## 🔧 INSTALL DEPENDENCIES

### **Jika Hosting Support SSH:**
\`\`\`bash
# Login SSH
ssh username@aksesgptmurah.tech

# Navigate ke folder
cd public_html/api

# Install Python packages
pip install -r requirements.txt

# Install Node.js packages (untuk frontend)
cd ../
npm install
npm run build
\`\`\`

### **Jika Hosting Tidak Support SSH:**
- Hubungi support hosting
- Minta install packages dari `requirements.txt`
- Atau gunakan shared hosting yang support Python

---

## 🌐 SETUP WEB SERVER

### **1. Apache (.htaccess)**
Buat file `.htaccess` di `public_html/`:

\`\`\`apache
# Frontend (React Router)
RewriteEngine On
RewriteBase /

# Handle React Router
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} !^/api/
RewriteRule . /index.html [L]

# API Routes to Backend
RewriteRule ^api/(.*)$ /api/app.py/$1 [L,QSA]

# Security Headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
\`\`\`

### **2. Nginx (Jika pakai VPS)**
\`\`\`nginx
server {
    listen 80;
    server_name aksesgptmurah.tech www.aksesgptmurah.tech;
    root /var/www/html;
    index index.html;

    # Frontend
    location / {
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

---

## 🧪 TESTING

### **1. Test Frontend**
- Buka: https://aksesgptmurah.tech/
- Harus muncul landing page
- Test navigasi ke /order

### **2. Test Backend API**
- Buka: https://aksesgptmurah.tech/api/health
- Harus return: `{"status": "healthy"}`

### **3. Test Database**
- Cek apakah tabel terbuat
- Test insert data

### **4. Test Payment**
- Buat test order
- Cek Midtrans dashboard

---

## 🚨 TROUBLESHOOTING UMUM

### **Error: "Module not found"**
- Install dependencies belum lengkap
- Cek `requirements.txt`

### **Error: "Database connection failed"**
- Cek DATABASE_URL di .env
- Pastikan database user punya akses

### **Error: "Permission denied"**
- Set file permissions:
  - Folders: 755
  - Files: 644
  - .env: 600

### **Error: "API not working"**
- Cek .htaccess rules
- Pastikan Python path benar

---

## 📞 SUPPORT & MAINTENANCE

### **Monitoring Harian:**
1. Cek email error reports
2. Monitor Midtrans transactions
3. Cek ChatGPT invite success rate

### **Backup Rutin:**
1. Database backup mingguan
2. File backup bulanan
3. Config backup setiap update

### **Update Berkala:**
1. Update dependencies
2. Security patches
3. Feature improvements

---

## 💰 ESTIMASI BIAYA & REVENUE

### **Biaya Bulanan:**
- ChatGPT Team: $30
- Hosting: $20 (existing)
- Member cost: $20 x jumlah member
- Total: $50 + ($20 x member count)

### **Revenue:**
- Jual Rp 25k/member/bulan
- Break-even: ~50 members
- Profit: Tergantung jumlah member

---

## ✅ CHECKLIST DEPLOY

- [ ] ChatGPT Team account ready
- [ ] Midtrans account verified
- [ ] SendGrid API key ready
- [ ] Database created
- [ ] Files uploaded
- [ ] .env configured
- [ ] Dependencies installed
- [ ] Web server configured
- [ ] Frontend accessible
- [ ] API endpoints working
- [ ] Payment flow tested
- [ ] Email notifications working
- [ ] ChatGPT automation tested

---

**🎉 Selamat! Website Anda siap digunakan di https://aksesgptmurah.tech/**

Jika ada error atau butuh bantuan, screenshot error dan kirim ke saya!
