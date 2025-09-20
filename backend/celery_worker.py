#!/usr/bin/env python3
"""
Celery worker entry point
Run with: celery -A celery_worker.celery worker --loglevel=info
"""

import os
from app import create_app
from tasks import make_celery

# Create Flask app
flask_app = create_app(os.environ.get('FLASK_ENV', 'development'))

# Create Celery instance
celery = make_celery(flask_app)

if __name__ == '__main__':
    celery.start()
