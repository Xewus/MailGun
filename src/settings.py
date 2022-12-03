import os
import sys
from dotenv import load_dotenv

root_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(root_dir, '.env'))

sys.path.append(root_dir)

SQLITE_DB = os.path.join(root_dir, '../db.sqlite')

FlaskConfig = {
    'ENV': os.environ.get('ENV', 'production'),
    'DEBUG': os.environ.get('DEBUG', False),
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'you-will-never-guess'),
    'MAX_CONTENT_LENGTH': 1024 * 1024,  # 1 MB
    'DATABASE': {
        'name': SQLITE_DB,
        'engine': 'peewee.SqliteDatabase',
    }
}

PAGE_TEMPLATES_DIR = os.path.join(root_dir, 'web/templates')
EMAIL_TEMPLATES_DIR = os.path.join(root_dir, 'email_templates')

UPLOAD_DIR = os.path.join(root_dir, '../upload')
ALLOWED_EXTENSIONS = ('csv',)

GOOGLE_CODE_CONNECTED = [220]
GOOGLE_CODE_LOGINED = [235]

GOOGLE_HOST = os.environ.get('HOST', 'smtp.gmail.com')
GOOGLE_PORT = os.environ.get('PORT', 587)

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
DOCKER_REDIS_NAME = os.environ.get('DOCKER_REDIS_NAME', 'docker_redis')

MAX_CELERY_DELAY = 24 * 3  # Hours
MAX_LENGTH_USERNAME = 128
MAX_LENGTH_EMAIL = 256
MAX_LENGTH_PASSWORD = 256
