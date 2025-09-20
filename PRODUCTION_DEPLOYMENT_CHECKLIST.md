# Production Deployment Checklist

## ⚠️ CRITICAL: Before Going Live

### 1. Environment Variables Setup
Copy `.env.production` to `.env` and fill in ALL required values:

\`\`\`bash
# REQUIRED - Generate strong secrets
SECRET_KEY=your-super-secure-secret-key-here-change-this
WEBHOOK_SECRET=your-webhook-secret-key

# REQUIRED - Database
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name

# REQUIRED - Tripay Credentials
TRIPAY_API_KEY=your-tripay-api-key
TRIPAY_MERCHANT_CODE=your-merchant-code
TRIPAY_PRIVATE_KEY=your-tripay-private-key
TRIPAY_CALLBACK_URL=https://api.aksesgptmurah.tech/callback/tripay

# REQUIRED - ChatGPT Admin
CHATGPT_ADMIN_EMAIL=your-chatgpt-admin@email.com
CHATGPT_ADMIN_PASSWORD=your-chatgpt-password

# REQUIRED - Email
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@aksesgptmurah.tech
ADMIN_EMAIL=admin@aksesgptmurah.tech
\`\`\`

### 2. Security Checklist
- [ ] Strong SECRET_KEY generated (use `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Database credentials are secure
- [ ] All API keys are from production accounts
- [ ] CORS origins are set to production domains only
- [ ] SSL certificates are installed
- [ ] Webhook secret is configured

### 3. Database Setup
\`\`\`bash
# Create database
mysql -u root -p -e "CREATE DATABASE gptapp_production;"
mysql -u root -p -e "CREATE USER 'gptuser'@'%' IDENTIFIED BY 'SecurePassword123!';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON gptapp_production.* TO 'gptuser'@'%';"

# Run migrations
docker-compose -f docker-compose.production.yml exec backend flask db upgrade
\`\`\`

### 4. Tripay Configuration
- [ ] Tripay account is in production mode
- [ ] Callback URL is set to: `https://api.aksesgptmurah.tech/callback/tripay`
- [ ] Payment methods are configured
- [ ] Test transaction completed successfully

### 5. Email Configuration
- [ ] SendGrid account verified
- [ ] Domain authentication completed
- [ ] Test email sent successfully

### 6. Deployment Commands
\`\`\`bash
# Build and start production services
docker-compose -f docker-compose.production.yml up -d --build

# Check all services are healthy
docker-compose -f docker-compose.production.yml ps

# View logs
docker-compose -f docker-compose.production.yml logs -f backend
\`\`\`

### 7. Post-Deployment Testing
\`\`\`bash
# Health check
curl https://api.aksesgptmurah.tech/health

# Test order creation
curl -X POST https://api.aksesgptmurah.tech/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "test@example.com",
    "full_name": "Test User",
    "phone_number": "08123456789",
    "package_id": "chatgpt_plus_1_month"
  }'

# Test webhook (simulate Tripay callback)
# Use Tripay's webhook testing tool or Postman
\`\`\`

### 8. Monitoring Setup
- [ ] Check application logs: `docker-compose -f docker-compose.production.yml logs -f`
- [ ] Monitor Celery workers: Access Flower at http://your-server:5555
- [ ] Set up log rotation for production logs
- [ ] Configure alerts for critical errors

### 9. Backup Strategy
- [ ] Database backup scheduled
- [ ] Application logs backup
- [ ] Environment files backup (encrypted)

## 🚨 Common Production Issues & Solutions

### Issue: "Environment variable required" errors
**Solution**: Ensure all required variables in `.env.production` are filled

### Issue: Database connection failed
**Solution**: Check DATABASE_URL format and credentials

### Issue: Tripay webhook signature verification failed
**Solution**: Verify TRIPAY_PRIVATE_KEY and callback URL configuration

### Issue: Selenium automation fails
**Solution**: Ensure Chrome and ChromeDriver are properly installed in container

### Issue: High memory usage
**Solution**: Adjust Docker resource limits and Celery concurrency settings

## 📞 Support Contacts
- **Technical Issues**: Check logs first, then contact development team
- **Payment Issues**: Contact Tripay support
- **Email Issues**: Contact SendGrid support
