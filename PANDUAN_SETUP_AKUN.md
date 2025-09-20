# 🔑 Panduan Setup Akun untuk Pemula Banget

## Domain Anda: https://aksesgptmurah.tech/

---

## 🎯 **AKUN APA SAJA YANG DIBUTUHKAN?**

Untuk menjalankan bisnis ChatGPT Plus ini, Anda butuh 3 akun utama:

1. **ChatGPT Team** → Untuk jadi admin dan invite customer
2. **Midtrans** → Untuk terima pembayaran dari customer  
3. **SendGrid** → Untuk kirim email konfirmasi ke customer

Mari kita setup satu per satu dengan detail!

---

## 👑 **LANGKAH 1: SETUP CHATGPT TEAM ACCOUNT**

### **A. Apa itu ChatGPT Team?**
- **Bukan ChatGPT Plus individual** (yang $20/bulan)
- **Tapi ChatGPT Team** (yang $25-30/bulan untuk workspace)
- **Anda jadi Admin**, bisa invite orang lain jadi Member
- **Customer jadi Member**, dapat akses ChatGPT Plus penuh

### **B. Cara Daftar ChatGPT Team:**

**1. Buka Website:**
- **Ketik di browser:** https://chatgpt.com/team
- **Atau Google:** "ChatGPT Team subscription"

**2. Klik "Subscribe to Team"**

**3. Isi Data Workspace:**
\`\`\`
Workspace Name: AKSES GPT MURAH
Team Size: 5-10 members (pilih yang sesuai rencana)
Use Case: Business/Professional
\`\`\`

**4. Isi Data Pembayaran:**
- **Kartu kredit** atau **PayPal**
- **Biaya:** sekitar $25-30/bulan
- **Auto-renewal:** aktif (bisa dimatikan nanti)

**5. Setelah Berhasil:**
- **Anda jadi Admin** workspace
- **Dapat akses** ke https://chatgpt.com/admin
- **Bisa invite member** unlimited

### **C. Catat Informasi Penting:**
\`\`\`
ChatGPT Admin Email: ________________
ChatGPT Admin Password: ________________
Workspace Name: AKSES GPT MURAH
Admin URL: https://chatgpt.com/admin?tab=members
\`\`\`

### **D. Test Admin Panel:**
1. **Login** ke https://chatgpt.com/admin
2. **Klik tab "Members"**
3. **Harus ada tombol "Invite member"**
4. **Test invite** email Anda sendiri sebagai Member

---

## 💳 **LANGKAH 2: SETUP MIDTRANS ACCOUNT**

### **A. Apa itu Midtrans?**
- **Payment gateway Indonesia** (seperti PayPal tapi lokal)
- **Terima pembayaran** via transfer bank, e-wallet, kartu kredit
- **Fee:** 2.9% per transaksi (standar industri)
- **Gratis** untuk daftar dan setup

### **B. Cara Daftar Midtrans:**

**1. Buka Website:**
- **Ketik di browser:** https://midtrans.com
- **Klik "Daftar Sekarang"** atau "Sign Up"

**2. Pilih Jenis Akun:**
- **Pilih "Merchant"** (bukan Developer)
- **Business Type:** Online Business

**3. Isi Data Bisnis:**
\`\`\`
Business Name: Akses GPT Murah
Business Type: Digital Services
Website URL: https://aksesgptmurah.tech
Business Description: Layanan akses ChatGPT Plus dengan harga terjangkau
\`\`\`

**4. Isi Data Pribadi:**
\`\`\`
Nama Lengkap: [Nama Anda]
Email: admin@aksesgptmurah.tech (atau email pribadi)
No HP: [Nomor HP Anda]
Alamat: [Alamat lengkap Anda]
\`\`\`

**5. Upload Dokumen:**
- **KTP** (foto yang jelas)
- **NPWP** (jika ada)
- **Foto selfie** dengan KTP
- **Rekening bank** (untuk pencairan dana)

**6. Tunggu Verifikasi:**
- **Proses:** 1-3 hari kerja
- **Email konfirmasi** akan dikirim
- **Status:** bisa dicek di dashboard

### **C. Setelah Diverifikasi:**

**1. Login ke Dashboard:**
- **Buka:** https://dashboard.midtrans.com
- **Login** dengan email/password Anda

**2. Ambil API Keys:**
- **Klik "Settings"** → **"Access Keys"**
- **Copy dan catat:**
\`\`\`
Server Key: SB-Mid-server-xxxxxxxxxxxxxxxxx
Client Key: SB-Mid-client-xxxxxxxxxxxxxxxxx
\`\`\`

**3. Set Webhook URL:**
- **Klik "Settings"** → **"Configuration"**
- **Payment Notification URL:**
\`\`\`
https://aksesgptmurah.tech/api/payment/webhook
\`\`\`

### **D. Test Sandbox:**
- **Mode Sandbox** untuk testing (gratis)
- **Mode Production** untuk live (bayar fee)
- **Mulai dengan Sandbox** dulu

---

## 📧 **LANGKAH 3: SETUP SENDGRID ACCOUNT**

### **A. Apa itu SendGrid?**
- **Email service** untuk kirim email otomatis
- **Gratis** 100 email per hari (cukup untuk mulai)
- **Reliable** dan trusted oleh banyak perusahaan

### **B. Cara Daftar SendGrid:**

**1. Buka Website:**
- **Ketik di browser:** https://sendgrid.com
- **Klik "Start for Free"**

**2. Isi Data Registrasi:**
\`\`\`
Email: admin@aksesgptmurah.tech
Password: [password kuat]
First Name: [Nama depan Anda]
Last Name: [Nama belakang Anda]
Company: Akses GPT Murah
Website: https://aksesgptmurah.tech
\`\`\`

**3. Verifikasi Email:**
- **Cek inbox** email Anda
- **Klik link** verifikasi dari SendGrid

**4. Setup Account:**
- **I send:** Transactional emails
- **I send about:** 100 emails per month
- **My role:** Developer/Technical

### **C. Buat API Key:**

**1. Login ke Dashboard:**
- **Buka:** https://app.sendgrid.com
- **Login** dengan akun Anda

**2. Buat API Key:**
- **Klik "Settings"** → **"API Keys"**
- **Klik "Create API Key"**
- **Name:** `aksesgpt-api-key`
- **Permissions:** **Full Access**
- **Klik "Create & View"**

**3. Copy API Key:**
\`\`\`
API Key: SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
\`\`\`
**PENTING:** Copy dan simpan baik-baik! Tidak bisa dilihat lagi.

### **D. Verify Sender:**

**1. Setup Sender Identity:**
- **Klik "Settings"** → **"Sender Authentication"**
- **Klik "Verify a Single Sender"**

**2. Isi Data Sender:**
\`\`\`
From Name: Akses GPT Murah
From Email: noreply@aksesgptmurah.tech
Reply To: admin@aksesgptmurah.tech
Company Address: [Alamat Anda]
City: [Kota Anda]
Country: Indonesia
\`\`\`

**3. Verifikasi:**
- **Cek email** noreply@aksesgptmurah.tech
- **Klik link** verifikasi

---

## ⚙️ **LANGKAH 4: UPDATE FILE .ENV**

Sekarang update file `.env` dengan semua API keys:

\`\`\`env
# Database Configuration
DATABASE_URL=mysql://aksesgpt_user:AksesGPT2024!@#@localhost/aksesgpt_orders

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=aksesgpt-super-secret-key-2024

# ChatGPT Admin Credentials - DATA ASLI ANDA!
CHATGPT_ADMIN_EMAIL=admin@aksesgptmurah.tech
CHATGPT_ADMIN_PASSWORD=password-chatgpt-anda
CHATGPT_ADMIN_URL=https://chatgpt.com/admin?tab=members

# Midtrans Payment Gateway - API KEY ASLI!
MIDTRANS_SERVER_KEY=SB-Mid-server-xxxxxxxxxxxxxxxxx
MIDTRANS_CLIENT_KEY=SB-Mid-client-xxxxxxxxxxxxxxxxx
MIDTRANS_IS_PRODUCTION=false

# SendGrid Email Service - API KEY ASLI!
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL=noreply@aksesgptmurah.tech

# Admin Notifications
ADMIN_EMAIL=admin@aksesgptmurah.tech

# Security
WEBHOOK_SECRET=webhook-secret-key-2024
ALLOWED_WEBHOOK_IPS=103.10.128.0/22,103.10.129.0/22

# Chrome/Selenium Configuration
SELENIUM_HEADLESS=true
SELENIUM_TIMEOUT=30
\`\`\`

**Upload file .env yang sudah diupdate ke hosting!**

---

## 🧪 **LANGKAH 5: TEST SEMUA AKUN**

### **A. Test ChatGPT Team:**
1. **Login** https://chatgpt.com/admin
2. **Klik "Invite member"**
3. **Masukkan email** test Anda
4. **Pilih role "Member"**
5. **Klik "Next"**
6. **Cek email** → harus ada undangan

### **B. Test Midtrans:**
1. **Login** dashboard Midtrans
2. **Buat test transaction**
3. **Cek webhook** berfungsi
4. **Test payment** dengan kartu test

### **C. Test SendGrid:**
1. **Login** dashboard SendGrid
2. **Kirim test email**
3. **Cek delivery** berhasil
4. **Cek spam folder** juga

---

## 💰 **LANGKAH 6: HITUNG BIAYA & PROFIT**

### **A. Biaya Bulanan:**
\`\`\`
ChatGPT Team Workspace: $30/bulan
ChatGPT Members: $20 x jumlah member
Midtrans Fee: 2.9% per transaksi
SendGrid: Gratis (100 email/hari)
Hosting: $20/bulan (existing)

Total: $50 + ($20 x jumlah member)
\`\`\`

### **B. Revenue:**
\`\`\`
Harga Jual: Rp 25,000/member/bulan
Break-even: ~50 members
Profit: Tergantung jumlah member
\`\`\`

### **C. Contoh Perhitungan:**
\`\`\`
100 members:
- Revenue: 100 x Rp 25,000 = Rp 2,500,000
- Cost: $50 + (100 x $20) = $2,050 ≈ Rp 32,000,000
- Loss: Rp 29,500,000 (tidak profitable!)

Solusi: Naikkan harga atau cari paket lebih murah
\`\`\`

---

## ✅ **CHECKLIST SETUP AKUN**

- [ ] ChatGPT Team account sudah dibuat
- [ ] Bisa login ke admin panel ChatGPT
- [ ] Test invite member berhasil
- [ ] Midtrans account sudah diverifikasi
- [ ] API Keys Midtrans sudah dicatat
- [ ] Webhook URL sudah diset
- [ ] SendGrid account sudah dibuat
- [ ] API Key SendGrid sudah dicatat
- [ ] Sender email sudah diverifikasi
- [ ] File .env sudah diupdate dengan semua API keys
- [ ] Test semua service berhasil
- [ ] Perhitungan profit sudah dibuat

---

## 🚨 **TROUBLESHOOTING AKUN**

### **ChatGPT Team tidak bisa invite:**
- Pastikan paket Team (bukan Plus individual)
- Cek billing status aktif
- Coba refresh browser

### **Midtrans verifikasi ditolak:**
- Cek dokumen KTP jelas
- Pastikan data sesuai KTP
- Hubungi support Midtrans

### **SendGrid email tidak terkirim:**
- Cek sender sudah diverifikasi
- Cek API key benar
- Cek spam folder

---

## 📞 **SUPPORT CONTACTS**

### **ChatGPT:**
- Help: https://help.openai.com
- Email: support@openai.com

### **Midtrans:**
- Support: support@midtrans.com
- Phone: +62 21 2212 5555

### **SendGrid:**
- Support: support@sendgrid.com
- Docs: https://docs.sendgrid.com

---

**🎉 Setelah semua akun setup, website Anda siap untuk go-live!**

**Next: Test full flow dari order sampai invite berhasil!**
