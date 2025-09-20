# 📥 Download Files untuk Deploy

## 🎯 Files yang Harus Didownload

### **1. Frontend Files (React)**
\`\`\`
src/
├── App.tsx
├── main.tsx
├── index.css
├── vite-env.d.ts
├── components/
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── PackageCard.tsx
│   ├── OrderForm.tsx
│   ├── OrderSummary.tsx
│   ├── FAQSection.tsx
│   ├── TestimonialSection.tsx
│   └── DemoControls.tsx
├── pages/
│   ├── LandingPage.tsx
│   ├── OrderPage.tsx
│   └── ConfirmationPage.tsx
├── contexts/
│   └── OrderContext.tsx
└── services/
    ├── apiService.ts
    └── mockApiService.ts
\`\`\`

### **2. Root Files**
\`\`\`
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── postcss.config.js
├── eslint.config.js
└── .env.example
\`\`\`

### **3. Backend Files (Python)**
\`\`\`
backend/
├── app.py
├── config.py
├── models.py
├── tasks.py
├── celery_worker.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── utils/
│   ├── validators.py
│   ├── payment_gateway.py
│   └── email_service.py
├── automation/
│   └── chatgpt_inviter.py
└── migrations/
    └── env.py
\`\`\`

### **4. Configuration Files**
\`\`\`
├── docker-compose.yml
├── DEPLOYMENT_GUIDE.md
├── PANDUAN_DEPLOY_PEMULA.md
└── README.md
\`\`\`

## 📋 Cara Download

### **Method 1: Individual Download**
1. Klik kanan pada setiap file di file explorer
2. Pilih "Download"
3. Simpan ke folder project Anda

### **Method 2: Copy-Paste**
1. Klik file yang ingin didownload
2. Select All (Ctrl+A) → Copy (Ctrl+C)
3. Paste ke text editor → Save dengan nama file yang sama

### **Method 3: Bulk Download**
Saya akan buatkan ZIP file untuk memudahkan:

## 🗂️ Struktur Folder di Hosting

Setelah download, upload dengan struktur ini:

\`\`\`
public_html/
├── index.html              # Frontend entry point
├── assets/                 # Built CSS/JS files
│   ├── index-xxx.css
│   └── index-xxx.js
├── api/                    # Backend files
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   └── utils/
├── .env                    # Environment variables
├── .htaccess              # Apache configuration
└── uploads/               # For file uploads (create manually)
\`\`\`

## ⚙️ Build Process

### **1. Build Frontend (Di komputer lokal):**
\`\`\`bash
npm install
npm run build
\`\`\`

### **2. Upload hasil build:**
- Upload folder `dist/` ke `public_html/`
- Rename `dist/index.html` jadi `public_html/index.html`
- Upload folder `dist/assets/` ke `public_html/assets/`

### **3. Upload Backend:**
- Upload semua file `backend/` ke `public_html/api/`
- Jangan lupa file `.env` dengan konfigurasi Anda

## 🔧 File Permissions

Set permissions yang benar:
\`\`\`bash
# Folders
chmod 755 public_html/
chmod 755 public_html/api/
chmod 755 public_html/assets/

# Files
chmod 644 public_html/index.html
chmod 644 public_html/api/*.py
chmod 600 public_html/.env  # Secret file
\`\`\`

## ✅ Checklist Download

- [ ] Semua file `src/` (React components)
- [ ] File `index.html`
- [ ] File `package.json`
- [ ] Semua file `backend/` (Python)
- [ ] File `.env.example` (rename jadi `.env`)
- [ ] File `requirements.txt`
- [ ] Panduan deploy (`PANDUAN_DEPLOY_PEMULA.md`)

**Total files: ~30 files**

Setelah download semua, ikuti panduan di `PANDUAN_DEPLOY_PEMULA.md` untuk deploy ke https://aksesgptmurah.tech/
