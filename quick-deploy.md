# ⚡ Quick Deploy Guide

## 🎯 Langkah Cepat Deploy ke Hosting

### **1. Persiapan Akun (30 menit)**
\`\`\`bash
✅ ChatGPT Team Account ($25/bulan)
✅ Midtrans Account (gratis)
✅ SendGrid Account (gratis)
✅ Domain & Hosting (sudah ada)
\`\`\`

### **2. Upload Files (15 menit)**
\`\`\`bash
# Download semua files dari project ini
# Upload ke hosting via cPanel/FTP:

public_html/
├── index.html, assets/ (frontend)
├── api/ (backend files)
└── .env (configuration)
\`\`\`

### **3. Install Dependencies (20 menit)**
\`\`\`bash
# SSH ke server, jalankan:
cd public_html/api
pip install -r requirements.txt
npm install (untuk frontend)
\`\`\`

### **4. Database Setup (10 menit)**
\`\`\`bash
# Buat database PostgreSQL di cPanel
# Import schema dari migrations/
# Update DATABASE_URL di .env
\`\`\`

### **5. Configuration (.env file)**
\`\`\`env
# Copy dari .env.example dan isi:
DATABASE_URL=postgresql://user:pass@host/db
MIDTRANS_SERVER_KEY=your-key
CHATGPT_ADMIN_EMAIL=your-email
SENDGRID_API_KEY=your-key
\`\`\`

### **6. Test & Launch (15 menit)**
\`\`\`bash
# Test API: yourdomain.com/api/health
# Test frontend: yourdomain.com
# Test order flow: buat test order
\`\`\`

## 🚀 Total Time: ~90 menit

### **Biaya Bulanan:**
- ChatGPT Team: $25-30
- Hosting: $10-50 (existing)
- Database: $0-25 (tergantung hosting)
- Email: $0 (SendGrid free)

### **Revenue Potential:**
- Jual Rp 25k/member/bulan
- Cost ~$20/member/bulan
- Break-even: ~50 members/bulan
