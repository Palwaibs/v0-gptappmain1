#!/usr/bin/env node

/**
 * Script untuk membuat package download
 * Jalankan: node create-zip-package.js
 */

const fs = require('fs');
const path = require('path');

console.log('📦 ChatGPT Plus Order System - Download Package Creator');
console.log('='.repeat(60));

// Daftar file yang harus didownload
const filesToDownload = {
  'Frontend Core': [
    'index.html',
    'package.json',
    'vite.config.ts',
    'tailwind.config.js',
    'tsconfig.json',
    'tsconfig.app.json',
    'tsconfig.node.json',
    'postcss.config.js',
    'eslint.config.js'
  ],
  'React Source': [
    'src/main.tsx',
    'src/App.tsx',
    'src/index.css',
    'src/vite-env.d.ts'
  ],
  'React Components': [
    'src/components/Header.tsx',
    'src/components/Footer.tsx',
    'src/components/PackageCard.tsx',
    'src/components/OrderForm.tsx',
    'src/components/OrderSummary.tsx',
    'src/components/FAQSection.tsx',
    'src/components/TestimonialSection.tsx',
    'src/components/DemoControls.tsx'
  ],
  'React Pages': [
    'src/pages/LandingPage.tsx',
    'src/pages/OrderPage.tsx',
    'src/pages/ConfirmationPage.tsx'
  ],
  'React Services': [
    'src/contexts/OrderContext.tsx',
    'src/services/apiService.ts',
    'src/services/mockApiService.ts'
  ],
  'Backend Core': [
    'backend/app.py',
    'backend/config.py',
    'backend/models.py',
    'backend/tasks.py',
    'backend/celery_worker.py',
    'backend/requirements.txt',
    'backend/Dockerfile'
  ],
  'Backend Utils': [
    'backend/utils/validators.py',
    'backend/utils/payment_gateway.py',
    'backend/utils/email_service.py'
  ],
  'Backend Automation': [
    'backend/automation/chatgpt_inviter.py'
  ],
  'Backend Database': [
    'backend/migrations/env.py'
  ],
  'Configuration': [
    '.env.example',
    'backend/.env.example',
    'docker-compose.yml',
    'backend/docker-compose.yml'
  ],
  'Documentation': [
    'README.md',
    'backend/README.md',
    'DEPLOYMENT_GUIDE.md',
    'PANDUAN_DEPLOY_PEMULA.md',
    'download-files.md'
  ]
};

console.log('\n📋 Files to Download:');
console.log('-'.repeat(40));

let totalFiles = 0;
Object.entries(filesToDownload).forEach(([category, files]) => {
  console.log(`\n${category}:`);
  files.forEach(file => {
    console.log(`  ✓ ${file}`);
    totalFiles++;
  });
});

console.log(`\n📊 Total Files: ${totalFiles}`);

console.log('\n🎯 Domain Target: https://aksesgptmurah.tech/');

console.log('\n📥 Download Instructions:');
console.log('-'.repeat(40));
console.log('1. Download semua file yang tercantum di atas');
console.log('2. Buat folder structure sesuai path');
console.log('3. Upload ke hosting dengan struktur:');
console.log('   public_html/');
console.log('   ├── index.html (frontend)');
console.log('   ├── assets/ (built files)');
console.log('   ├── api/ (backend files)');
console.log('   └── .env (configuration)');

console.log('\n⚙️ Next Steps:');
console.log('-'.repeat(40));
console.log('1. Setup ChatGPT Team account');
console.log('2. Setup Midtrans payment gateway');
console.log('3. Setup SendGrid email service');
console.log('4. Configure .env file');
console.log('5. Upload files to hosting');
console.log('6. Install dependencies');
console.log('7. Test website');

console.log('\n🚀 Ready to deploy to https://aksesgptmurah.tech/');
console.log('📖 Follow PANDUAN_DEPLOY_PEMULA.md for detailed steps');
