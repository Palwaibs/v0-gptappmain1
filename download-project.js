#!/usr/bin/env node

/**
 * Project Download Script
 * Run with: node download-project.js
 */

const fs = require('fs');
const path = require('path');

console.log('📦 ChatGPT Plus Order System - Project Files');
console.log('='.repeat(50));

const projectStructure = {
  'Frontend Files': [
    'package.json',
    'vite.config.ts',
    'tailwind.config.js',
    'tsconfig.json',
    'tsconfig.app.json',
    'tsconfig.node.json',
    'postcss.config.js',
    'index.html',
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
  'Pages': [
    'src/pages/LandingPage.tsx',
    'src/pages/OrderPage.tsx',
    'src/pages/ConfirmationPage.tsx'
  ],
  'Services & Context': [
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
  'Automation': [
    'backend/automation/chatgpt_inviter.py'
  ],
  'Database': [
    'backend/migrations/env.py',
    'supabase/migrations/20250911152213_autumn_trail.sql'
  ],
  'Configuration': [
    '.env.example',
    'backend/.env.example',
    'docker-compose.yml',
    'backend/docker-compose.yml',
    'eslint.config.js'
  ],
  'Documentation': [
    'README.md',
    'backend/README.md'
  ]
};

console.log('\n📁 Project Structure:');
console.log('-'.repeat(30));

Object.entries(projectStructure).forEach(([category, files]) => {
  console.log(`\n${category}:`);
  files.forEach(file => {
    console.log(`  ├── ${file}`);
  });
});

console.log('\n🚀 Quick Start Commands:');
console.log('-'.repeat(30));
console.log('Frontend:');
console.log('  npm install');
console.log('  npm run dev');
console.log('');
console.log('Backend:');
console.log('  cd backend');
console.log('  pip install -r requirements.txt');
console.log('  python app.py');
console.log('');
console.log('Docker:');
console.log('  docker-compose up -d');

console.log('\n✅ Ready to download!');
