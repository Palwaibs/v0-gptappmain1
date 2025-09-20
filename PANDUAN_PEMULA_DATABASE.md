# 🗄️ Panduan Database Setup untuk Pemula Banget

## Domain Anda: https://aksesgptmurah.tech/

---

## 🎯 **APA ITU DATABASE?**

Database itu seperti **lemari arsip digital** yang menyimpan data:
- **Data customer** (email, nama, nomor HP)
- **Data pesanan** (order ID, paket yang dibeli, status pembayaran)
- **Data undangan** (siapa yang sudah diundang, kapan, berhasil atau tidak)

Tanpa database, website tidak bisa menyimpan data apapun!

---

## 📋 **LANGKAH 1: CEK HOSTING ANDA**

### **A. Login ke cPanel Hosting:**
1. **Buka browser** → ketik alamat cPanel Anda
   - Biasanya: `https://aksesgptmurah.tech:2083`
   - Atau: `https://cpanel.namahosting.com`
   - Atau: `https://aksesgptmurah.tech/cpanel`

2. **Login dengan:**
   - **Username**: username hosting Anda
   - **Password**: password hosting Anda

3. **Setelah login**, Anda akan lihat dashboard cPanel

### **B. Cari Menu Database:**
Di dashboard cPanel, cari icon/menu:
- 📊 **"MySQL Databases"** (paling umum)
- 🗄️ **"PostgreSQL Databases"** (lebih bagus tapi jarang)
- 📋 **"Database"** atau **"Databases"**

**Screenshot yang harus Anda ambil:**
- Dashboard cPanel Anda
- Menu database yang tersedia

---

## 🔧 **LANGKAH 2: BUAT DATABASE (MySQL)**

### **A. Buat Database Baru:**

1. **Klik "MySQL Databases"**

2. **Di bagian "Create New Database":**
   \`\`\`
   New Database: aksesgpt_orders
   \`\`\`
   - **PENTING**: Nama database HARUS `aksesgpt_orders`
   - Jangan pakai spasi atau karakter aneh
   - Klik **"Create Database"**

3. **Akan muncul pesan:** "Added the database aksesgpt_orders"

### **B. Buat User Database:**

1. **Di bagian "MySQL Users" → "Add New User":**
   \`\`\`
   Username: aksesgpt_user
   Password: [buat password kuat, catat baik-baik!]
   Password (Again): [ketik ulang password yang sama]
   \`\`\`

2. **Contoh password kuat:**
   \`\`\`
   AksesGPT2024!@#
   \`\`\`
   - **CATAT PASSWORD INI!** Anda akan butuh nanti

3. **Klik "Create User"**

### **C. Hubungkan User ke Database:**

1. **Di bagian "Add User To Database":**
   - **User**: Pilih `aksesgpt_user`
   - **Database**: Pilih `aksesgpt_orders`
   - **Klik "Add"**

2. **Di halaman privileges:**
   - **Centang "ALL PRIVILEGES"** (atau klik "Check All")
   - **Klik "Make Changes"**

### **D. Catat Informasi Database:**
\`\`\`
Database Name: aksesgpt_orders
Username: aksesgpt_user  
Password: AksesGPT2024!@# (password yang Anda buat)
Host: localhost
\`\`\`

---

## 🔧 **LANGKAH 3: BUAT TABEL DATABASE**

### **A. Masuk ke phpMyAdmin:**

1. **Di cPanel**, cari dan klik **"phpMyAdmin"**

2. **Login otomatis** atau masukkan:
   - **Username**: aksesgpt_user
   - **Password**: password yang tadi dibuat

3. **Pilih database** `aksesgpt_orders` di panel kiri

### **B. Buat Tabel Orders:**

1. **Klik tab "SQL"** di phpMyAdmin

2. **Copy-paste kode ini** ke kotak SQL:

\`\`\`sql
-- Tabel untuk menyimpan data pesanan
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone_number VARCHAR(20),
    package_id VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'pending',
    invitation_status VARCHAR(50) DEFAULT 'pending',
    payment_gateway_ref_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id),
    INDEX idx_customer_email (customer_email),
    INDEX idx_payment_status (payment_status),
    INDEX idx_invitation_status (invitation_status)
);

-- Tabel untuk log undangan
CREATE TABLE invitation_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    attempt_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    screenshot_path VARCHAR(255),
    retry_count INT DEFAULT 0,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id)
);

-- Tabel untuk paket
CREATE TABLE packages (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    duration VARCHAR(50) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert paket default
INSERT INTO packages (id, name, price, duration, description) VALUES
('chatgpt_plus_1_month', 'Individual Plan', 25000, '1 Bulan', 'Akses ChatGPT Plus penuh dengan email pribadi sebagai Member'),
('team_package', 'Team Plan', 95000, '1 Bulan', 'Sampai 5 akun tim sebagai Member dengan akses penuh');
\`\`\`

3. **Klik "Go"** untuk menjalankan

4. **Jika berhasil**, akan muncul pesan hijau: "Query executed successfully"

### **C. Verifikasi Tabel Terbuat:**

1. **Refresh** panel kiri phpMyAdmin
2. **Expand database** `aksesgpt_orders`
3. **Harus ada 3 tabel:**
   - ✅ `orders`
   - ✅ `invitation_logs` 
   - ✅ `packages`

---

## 🔧 **LANGKAH 4: BUAT FILE KONFIGURASI**

### **A. Buat File .env:**

1. **Buka text editor** (Notepad, VS Code, dll)

2. **Copy-paste kode ini:**

\`\`\`env
# Database Configuration - GANTI DENGAN DATA ANDA!
DATABASE_URL=mysql://aksesgpt_user:AksesGPT2024!@#@localhost/aksesgpt_orders

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=aksesgpt-super-secret-key-2024

# ChatGPT Admin Credentials - GANTI DENGAN AKUN ANDA!
CHATGPT_ADMIN_EMAIL=admin@aksesgptmurah.tech
CHATGPT_ADMIN_PASSWORD=password-chatgpt-anda
CHATGPT_ADMIN_URL=https://chatgpt.com/admin?tab=members

# Midtrans Payment Gateway - GANTI DENGAN API KEY ANDA!
MIDTRANS_SERVER_KEY=SB-Mid-server-xxxxxxxxx
MIDTRANS_CLIENT_KEY=SB-Mid-client-xxxxxxxxx
MIDTRANS_IS_PRODUCTION=false

# SendGrid Email Service - GANTI DENGAN API KEY ANDA!
SENDGRID_API_KEY=SG.xxxxxxxxx
FROM_EMAIL=noreply@aksesgptmurah.tech

# Admin Notifications
ADMIN_EMAIL=admin@aksesgptmurah.tech

# Security
WEBHOOK_SECRET=webhook-secret-key-2024
ALLOWED_WEBHOOK_IPS=103.10.128.0/22,103.10.129.0/22

# Chrome/Selenium Configuration
SELENIUM_HEADLESS=true
SELENIUM_TIMEOUT=30

# Rate Limiting
RATE_LIMIT_STORAGE_URL=redis://localhost:6379/1
\`\`\`

3. **PENTING! Ganti semua yang ada "xxxxxxxxx":**
   - `AksesGPT2024!@#` → password database Anda
   - `admin@aksesgptmurah.tech` → email ChatGPT admin Anda
   - `password-chatgpt-anda` → password ChatGPT Anda
   - `SB-Mid-server-xxxxxxxxx` → Server Key Midtrans
   - `SB-Mid-client-xxxxxxxxx` → Client Key Midtrans
   - `SG.xxxxxxxxx` → API Key SendGrid

4. **Save file** dengan nama `.env` (dengan titik di depan!)

---

## 🧪 **LANGKAH 5: TEST DATABASE**

### **A. Test Koneksi Database:**

1. **Di phpMyAdmin**, klik tab **"SQL"**

2. **Jalankan query test:**
\`\`\`sql
-- Test insert data
INSERT INTO orders (order_id, customer_email, package_id, amount) 
VALUES ('TEST001', 'test@example.com', 'chatgpt_plus_1_month', 25000);

-- Test select data
SELECT * FROM orders WHERE order_id = 'TEST001';

-- Hapus data test
DELETE FROM orders WHERE order_id = 'TEST001';
\`\`\`

3. **Jika berhasil**, berarti database sudah siap!

### **B. Test Database URL:**

Pastikan format DATABASE_URL benar:
\`\`\`
mysql://username:password@host/database_name
\`\`\`

**Contoh yang benar:**
\`\`\`
mysql://aksesgpt_user:AksesGPT2024!@#@localhost/aksesgpt_orders
\`\`\`

**Yang SALAH:**
\`\`\`
mysql://aksesgpt_user@localhost/aksesgpt_orders  ❌ (tidak ada password)
mysql://aksesgpt_user:password@/aksesgpt_orders  ❌ (tidak ada host)
\`\`\`

---

## 🚨 **TROUBLESHOOTING DATABASE**

### **Error: "Access denied for user"**
**Solusi:**
1. Cek username dan password di .env
2. Pastikan user sudah ditambahkan ke database
3. Pastikan user punya ALL PRIVILEGES

### **Error: "Unknown database"**
**Solusi:**
1. Cek nama database di .env (harus `aksesgpt_orders`)
2. Pastikan database sudah dibuat di cPanel

### **Error: "Table doesn't exist"**
**Solusi:**
1. Jalankan ulang SQL untuk buat tabel
2. Cek di phpMyAdmin apakah tabel ada

### **Error: "Connection refused"**
**Solusi:**
1. Cek host di DATABASE_URL (biasanya `localhost`)
2. Hubungi support hosting jika masih error

---

## ✅ **CHECKLIST DATABASE SETUP**

- [ ] Login cPanel berhasil
- [ ] Database `aksesgpt_orders` sudah dibuat
- [ ] User `aksesgpt_user` sudah dibuat
- [ ] User sudah ditambahkan ke database dengan ALL PRIVILEGES
- [ ] 3 tabel sudah dibuat (orders, invitation_logs, packages)
- [ ] File .env sudah dibuat dengan DATABASE_URL yang benar
- [ ] Test query berhasil dijalankan
- [ ] Semua password dan API key sudah dicatat

---

## 📞 **BANTUAN JIKA STUCK**

### **Screenshot yang Perlu Anda Ambil Jika Error:**
1. Dashboard cPanel Anda
2. Menu MySQL Databases
3. Daftar database yang sudah dibuat
4. Error message (jika ada)
5. Isi file .env Anda (tutup password!)

### **Info yang Perlu Anda Siapkan:**
- Nama hosting provider Anda
- Paket hosting yang digunakan
- Versi PHP/MySQL di hosting
- Control panel yang digunakan (cPanel/Plesk/dll)

**Jika masih bingung, kirim screenshot ke saya dan saya akan bantu troubleshoot!**

---

**🎉 Setelah database setup selesai, lanjut ke upload files dan konfigurasi website!**
