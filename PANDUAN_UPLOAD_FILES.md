# 📁 Panduan Upload Files untuk Pemula Banget

## Domain Anda: https://aksesgptmurah.tech/

---

## 🎯 **APA YANG AKAN KITA UPLOAD?**

Website ini terdiri dari 2 bagian:
- **Frontend** (tampilan website) → file HTML, CSS, JavaScript
- **Backend** (server/API) → file Python untuk proses data

---

## 📥 **LANGKAH 1: DOWNLOAD SEMUA FILES**

### **A. Files Frontend (React):**

**1. File Utama:**
- `index.html` → Halaman utama website
- `package.json` → Daftar library yang dibutuhkan

**2. Folder src/ (Source Code):**
- `src/App.tsx` → Aplikasi utama
- `src/main.tsx` → Entry point
- `src/index.css` → Style CSS

**3. Components (Komponen Website):**
- `src/components/Header.tsx` → Header website
- `src/components/Footer.tsx` → Footer website  
- `src/components/PackageCard.tsx` → Kartu paket harga
- `src/components/OrderForm.tsx` → Form pemesanan
- `src/components/OrderSummary.tsx` → Ringkasan pesanan
- `src/components/FAQSection.tsx` → Bagian FAQ
- `src/components/TestimonialSection.tsx` → Testimoni
- `src/components/DemoControls.tsx` → Kontrol demo

**4. Pages (Halaman Website):**
- `src/pages/LandingPage.tsx` → Halaman utama
- `src/pages/OrderPage.tsx` → Halaman pemesanan
- `src/pages/ConfirmationPage.tsx` → Halaman konfirmasi

**5. Services (Layanan):**
- `src/contexts/OrderContext.tsx` → Manajemen data pesanan
- `src/services/apiService.ts` → Komunikasi dengan server
- `src/services/mockApiService.ts` → Demo API

### **B. Files Backend (Python):**

**1. File Utama:**
- `backend/app.py` → Server utama
- `backend/config.py` → Konfigurasi
- `backend/models.py` → Model database
- `backend/requirements.txt` → Library Python yang dibutuhkan

**2. Utils (Utilitas):**
- `backend/utils/validators.py` → Validasi data
- `backend/utils/payment_gateway.py` → Integrasi Midtrans
- `backend/utils/email_service.py` → Kirim email

**3. Automation:**
- `backend/automation/chatgpt_inviter.py` → Otomasi invite ChatGPT

### **C. Files Konfigurasi:**
- `.env` → File konfigurasi (yang sudah Anda buat)
- `vite.config.ts` → Konfigurasi build
- `tailwind.config.js` → Konfigurasi CSS

---

## 📂 **LANGKAH 2: CARA DOWNLOAD FILES**

### **Method 1: Download Satu-Satu**
1. **Klik kanan** pada file di panel kiri
2. **Pilih "Download"**
3. **File tersimpan** di folder Downloads komputer

### **Method 2: Copy-Paste**
1. **Klik file** yang ingin didownload
2. **Ctrl+A** (Select All) → **Ctrl+C** (Copy)
3. **Buka Notepad/Text Editor**
4. **Ctrl+V** (Paste) → **Save** dengan nama file yang sama

**PENTING:** Pastikan ekstensi file benar (.tsx, .py, .js, dll)

---

## 🏗️ **LANGKAH 3: BUILD FRONTEND**

### **A. Install Node.js (Jika Belum Ada):**
1. **Download Node.js** dari https://nodejs.org
2. **Install** dengan setting default
3. **Buka Command Prompt/Terminal**
4. **Test:** ketik `node --version` (harus muncul versi)

### **B. Build Project:**
1. **Buka Command Prompt**
2. **Navigate** ke folder project:
   \`\`\`cmd
   cd C:\Users\YourName\Downloads\chatgpt-project
   \`\`\`

3. **Install dependencies:**
   \`\`\`cmd
   npm install
   \`\`\`

4. **Build untuk production:**
   \`\`\`cmd
   npm run build
   \`\`\`

5. **Akan terbuat folder `dist/`** berisi file siap upload

---

## 📤 **LANGKAH 4: UPLOAD KE HOSTING**

### **A. Login ke cPanel:**
1. **Buka browser** → alamat cPanel Anda
2. **Login** dengan username/password hosting

### **B. Buka File Manager:**
1. **Cari dan klik "File Manager"** di cPanel
2. **Navigate** ke folder `public_html/`
3. **Ini adalah root website** Anda

### **C. Upload Frontend (Hasil Build):**

**1. Upload file dari folder `dist/`:**
- `index.html` → upload ke `public_html/`
- Folder `assets/` → upload ke `public_html/assets/`

**2. Struktur yang benar:**
\`\`\`
public_html/
├── index.html          ← File utama website
├── assets/             ← CSS, JS, gambar
│   ├── index-abc123.css
│   ├── index-xyz789.js
│   └── ...
\`\`\`

### **D. Upload Backend:**

**1. Buat folder API:**
- **Di public_html/**, klik **"Create Folder"**
- **Nama folder:** `api`

**2. Upload files backend ke folder `api/`:**
- `app.py`
- `config.py`
- `models.py`
- `requirements.txt`
- Folder `utils/` (dengan semua isinya)
- Folder `automation/` (dengan semua isinya)

**3. Struktur yang benar:**
\`\`\`
public_html/
├── index.html
├── assets/
├── api/                ← Backend files
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   ├── utils/
│   │   ├── validators.py
│   │   ├── payment_gateway.py
│   │   └── email_service.py
│   └── automation/
│       └── chatgpt_inviter.py
\`\`\`

### **E. Upload File .env:**
- **Upload file `.env`** ke `public_html/`
- **Set permission** file .env ke **600** (klik kanan → Permissions)

---

## ⚙️ **LANGKAH 5: KONFIGURASI WEB SERVER**

### **A. Buat File .htaccess:**

1. **Di File Manager**, klik **"Create File"**
2. **Nama file:** `.htaccess`
3. **Edit file** dan paste kode ini:

\`\`\`apache
# Enable rewrite engine
RewriteEngine On

# Handle React Router (Frontend)
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

# HTTPS Redirect
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
\`\`\`

4. **Save file**

### **B. Set File Permissions:**

**Folders (755):**
- `public_html/` → 755
- `public_html/api/` → 755
- `public_html/assets/` → 755

**Files (644):**
- `index.html` → 644
- `app.py` → 644
- Semua file .py → 644

**Secret Files (600):**
- `.env` → 600

**Cara set permission:**
1. **Klik kanan file/folder**
2. **Pilih "Permissions"**
3. **Set angka** sesuai di atas
4. **Klik "Change Permissions"**

---

## 🐍 **LANGKAH 6: INSTALL PYTHON DEPENDENCIES**

### **A. Via SSH (Jika Tersedia):**

1. **Login SSH** ke hosting
2. **Navigate** ke folder API:
   \`\`\`bash
   cd public_html/api
   \`\`\`

3. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

### **B. Via cPanel Python App (Jika Ada):**

1. **Cari "Python App"** di cPanel
2. **Create New App**
3. **Set path** ke `/public_html/api`
4. **Install** dari requirements.txt

### **C. Hubungi Support Hosting:**

Jika tidak ada SSH atau Python App:
1. **Buka tiket support** hosting
2. **Minta install** packages dari requirements.txt
3. **Berikan file** requirements.txt

---

## 🧪 **LANGKAH 7: TEST WEBSITE**

### **A. Test Frontend:**
1. **Buka browser**
2. **Ketik:** https://aksesgptmurah.tech/
3. **Harus muncul** landing page website
4. **Test navigasi** ke halaman order

### **B. Test Backend API:**
1. **Buka:** https://aksesgptmurah.tech/api/health
2. **Harus return:** `{"status": "healthy"}`
3. **Jika error**, cek log error di cPanel

### **C. Test Database:**
1. **Buka:** https://aksesgptmurah.tech/api/packages
2. **Harus return** daftar paket
3. **Jika error**, cek koneksi database

---

## 🚨 **TROUBLESHOOTING UPLOAD**

### **Error: "Internal Server Error"**
**Solusi:**
1. Cek file .htaccess (mungkin ada typo)
2. Cek permission files (harus 644)
3. Cek error log di cPanel

### **Error: "Module not found"**
**Solusi:**
1. Install Python dependencies belum lengkap
2. Hubungi support hosting untuk install

### **Error: "Database connection failed"**
**Solusi:**
1. Cek file .env (DATABASE_URL harus benar)
2. Test koneksi database di phpMyAdmin

### **Frontend tidak muncul:**
**Solusi:**
1. Pastikan index.html ada di public_html/
2. Cek folder assets/ sudah terupload
3. Clear cache browser

---

## ✅ **CHECKLIST UPLOAD**

- [ ] Semua files frontend sudah didownload
- [ ] Semua files backend sudah didownload
- [ ] Node.js sudah terinstall
- [ ] Project sudah di-build (`npm run build`)
- [ ] File index.html sudah diupload ke public_html/
- [ ] Folder assets/ sudah diupload
- [ ] Folder api/ sudah dibuat dan diisi
- [ ] File .env sudah diupload dengan permission 600
- [ ] File .htaccess sudah dibuat
- [ ] File permissions sudah diset dengan benar
- [ ] Python dependencies sudah diinstall
- [ ] Test frontend berhasil (website muncul)
- [ ] Test backend berhasil (API response OK)
- [ ] Test database berhasil (packages muncul)

---

## 📞 **BANTUAN JIKA STUCK**

### **Screenshot yang Perlu Jika Error:**
1. File Manager cPanel (struktur folder)
2. Error message di browser
3. Error log di cPanel
4. Isi file .htaccess
5. Permission files

### **Info yang Perlu:**
- Nama hosting provider
- Versi PHP di hosting
- Support Python atau tidak
- Control panel yang digunakan

**Kirim screenshot dan info ke saya jika ada masalah!**

---

**🎉 Setelah upload selesai, lanjut ke setup akun Midtrans, SendGrid, dan ChatGPT!**
