import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is required")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Payment Gateway (Tripay) - All required
    TRIPAY_API_KEY = os.environ.get('TRIPAY_API_KEY')
    TRIPAY_MERCHANT_CODE = os.environ.get('TRIPAY_MERCHANT_CODE')
    TRIPAY_PRIVATE_KEY = os.environ.get('TRIPAY_PRIVATE_KEY')
    
    if not all([TRIPAY_API_KEY, TRIPAY_MERCHANT_CODE, TRIPAY_PRIVATE_KEY]):
        raise ValueError("All Tripay credentials (API_KEY, MERCHANT_CODE, PRIVATE_KEY) are required")
    
    TRIPAY_IS_PRODUCTION = os.environ.get('TRIPAY_IS_PRODUCTION', 'false').lower() == 'true'
    TRIPAY_BASE_URL = os.environ.get('TRIPAY_BASE_URL', 'https://tripay.co.id/api')
    TRIPAY_CALLBACK_URL = os.environ.get('TRIPAY_CALLBACK_URL')
    
    if not TRIPAY_CALLBACK_URL:
        raise ValueError("TRIPAY_CALLBACK_URL environment variable is required")

    # API Configuration
    API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:5000')
    TRIPAY_CALLBACK_PATH = os.environ.get('TRIPAY_CALLBACK_PATH', '/callback/tripay')
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
    
    # CORS Configuration
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000,https://aksesgptmurah.tech').split(',')
    ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS if origin.strip()]  # Clean up whitespace
    
    # ChatGPT Admin Credentials
    CHATGPT_ADMIN_EMAIL = os.environ.get('CHATGPT_ADMIN_EMAIL')
    CHATGPT_ADMIN_PASSWORD = os.environ.get('CHATGPT_ADMIN_PASSWORD')
    # Use admin URL instead of team URL based on interface
    CHATGPT_ADMIN_URL = os.environ.get('CHATGPT_ADMIN_URL') or 'https://chatgpt.com/admin?tab=members'
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Celery Configuration
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True
    
    # Email Configuration
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    FROM_EMAIL = os.environ.get('FROM_EMAIL') or 'noreply@yourdomain.com'
    
    # Email Configuration
    EMAIL_ENABLED = os.environ.get('EMAIL_ENABLED', 'false').lower() == 'true'
    
    # Admin Notifications
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_TELEGRAM_BOT_TOKEN = os.environ.get('ADMIN_TELEGRAM_BOT_TOKEN')
    ADMIN_TELEGRAM_CHAT_ID = os.environ.get('ADMIN_TELEGRAM_CHAT_ID')
    
    # Security
    WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')
    ALLOWED_WEBHOOK_IPS = os.environ.get('ALLOWED_WEBHOOK_IPS', '').split(',')
    
    # Selenium Configuration
    CHROME_BINARY_PATH = os.environ.get('CHROME_BINARY_PATH')
    CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')
    SELENIUM_HEADLESS = os.environ.get('SELENIUM_HEADLESS', 'true').lower() == 'true'
    SELENIUM_TIMEOUT = int(os.environ.get('SELENIUM_TIMEOUT', '30'))
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATE_LIMIT_STORAGE_URL') or 'redis://localhost:6379/1'
    
    # Celery Configuration
    ENABLE_CELERY = os.environ.get('ENABLE_CELERY', 'false').lower() == 'true'
    
    # Package Configuration
    PACKAGES = {
        'chatgpt_plus_1_month': {
            'name': 'Individual Plan',
            'price': 25000,
            'duration': '1 Bulan',
            'description': 'Akses GPT-4 Unlimited dengan email pribadi sebagai Member'
        },
        'team_package': {
            'name': 'Team Plan',
            'price': 95000,
            'duration': '1 Bulan',
            'description': 'Sampai 5 akun tim sebagai Member dengan akses penuh'
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    def __init__(self):
        super().__init__()
        # Ensure critical production settings
        if not os.environ.get('CHATGPT_ADMIN_EMAIL') or not os.environ.get('CHATGPT_ADMIN_PASSWORD'):
            raise ValueError("ChatGPT admin credentials are required in production")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
