# Checklist Tes Integrasi Frontend-Backend

## 1. Tes Koneksi API

### Backend Health Check
\`\`\`bash
curl https://api.aksesgptmurah.tech/health
curl https://api.aksesgptmurah.tech/healthz
\`\`\`
**Expected Response:**
\`\`\`json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000",
  "version": "1.0.0",
  "environment": "production"
}
\`\`\`

### Frontend API Connection
1. Buka browser developer tools (F12)
2. Akses https://aksesgptmurah.tech
3. Cek Console untuk error CORS atau network
4. Pastikan tidak ada error "blocked by CORS policy"

## 2. Tes Order Creation

### Manual Test via cURL
\`\`\`bash
curl -X POST https://api.aksesgptmurah.tech/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "test@example.com",
    "package_id": "chatgpt_plus_1_month",
    "full_name": "Test User",
    "phone_number": "+6281234567890",
    "payment_method": "QRIS"
  }'
\`\`\`

**Expected Response:**
\`\`\`json
{
  "success": true,
  "order_id": "INV-1234567890",
  "reference": "T123456789",
  "checkout_url": "https://tripay.co.id/checkout/...",
  "qr_string": "...",
  "payment_method": "QRIS",
  "amount": 25000,
  "status": "pending_payment"
}
\`\`\`

### Frontend Order Test
1. Akses https://aksesgptmurah.tech
2. Pilih paket Individual Plan
3. Isi form dengan data valid
4. Klik "Lanjutkan Pembayaran"
5. Pastikan redirect ke halaman konfirmasi
6. Cek URL mengandung `?order_id=...`

## 3. Tes Order Status

### Manual Test via cURL
\`\`\`bash
curl https://api.aksesgptmurah.tech/api/orders/INV-1234567890/status
\`\`\`

**Expected Response:**
\`\`\`json
{
  "order_id": "INV-1234567890",
  "payment_status": "pending",
  "invitation_status": "pending",
  "message": "Menunggu pembayaran. Silakan selesaikan pembayaran sesuai instruksi."
}
\`\`\`

### Frontend Status Polling
1. Dari halaman konfirmasi, buka Network tab di developer tools
2. Pastikan ada request polling ke `/api/orders/{id}/status` setiap 5 detik
3. Pastikan status update otomatis tanpa refresh halaman

## 4. Tes Webhook Tripay

### Simulasi Webhook
\`\`\`bash
curl -X POST https://api.aksesgptmurah.tech/callback/tripay \
  -H "Content-Type: application/json" \
  -d '{
    "merchant_ref": "INV-1234567890",
    "reference": "T123456789",
    "status": "PAID",
    "total_amount": 25000,
    "signature": "calculated_hmac_signature"
  }'
\`\`\`

**Expected Response:**
\`\`\`json
{
  "success": true
}
\`\`\`

## 5. Tes CORS

### Preflight Request Test
\`\`\`bash
curl -X OPTIONS https://api.aksesgptmurah.tech/api/orders \
  -H "Origin: https://aksesgptmurah.tech" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type"
\`\`\`

**Expected Headers:**
- `Access-Control-Allow-Origin: https://aksesgptmurah.tech`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization, Accept`

## 6. Tes Error Handling

### Invalid Package ID
\`\`\`bash
curl -X POST https://api.aksesgptmurah.tech/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "test@example.com",
    "package_id": "invalid_package",
    "full_name": "Test User"
  }'
\`\`\`

**Expected Response:** HTTP 400 dengan error message

### Invalid Order ID
\`\`\`bash
curl https://api.aksesgptmurah.tech/api/orders/INVALID-ID/status
\`\`\`

**Expected Response:** HTTP 404 dengan error message

## 7. Tes Rate Limiting

### Rapid Requests
Kirim 15 request dalam 1 menit ke `/api/orders`

**Expected:** Request ke-11 dan seterusnya mendapat HTTP 429

## 8. Tes Environment Variables

### Backend Environment Check
\`\`\`bash
# SSH ke server
echo $VITE_API_URL  # Should be empty (backend doesn't need this)
echo $ALLOWED_ORIGINS  # Should contain frontend domain
echo $TRIPAY_API_KEY  # Should be set (don't log the value)
\`\`\`

### Frontend Environment Check
\`\`\`javascript
// In browser console
console.log(process.env.NEXT_PUBLIC_API_URL)
// Should output: https://api.aksesgptmurah.tech
\`\`\`

## 9. Checklist Deployment

- [ ] Backend health endpoint accessible
- [ ] Frontend can reach backend API
- [ ] CORS properly configured
- [ ] Order creation works end-to-end
- [ ] Order status polling works
- [ ] Webhook endpoint accessible
- [ ] Error handling works properly
- [ ] Rate limiting active
- [ ] Environment variables set correctly
- [ ] SSL certificates valid for both domains

## 10. Common Issues & Solutions

### CORS Error
**Problem:** "blocked by CORS policy"
**Solution:** Check `ALLOWED_ORIGINS` in backend config

### 404 on API Calls
**Problem:** Frontend getting 404 on API calls
**Solution:** Verify `NEXT_PUBLIC_API_URL` in frontend .env

### Webhook Not Working
**Problem:** Tripay webhook returns error
**Solution:** Check `TRIPAY_CALLBACK_URL` and signature verification

### Order Status Not Updating
**Problem:** Status stuck on "pending"
**Solution:** Check webhook endpoint and database connection
