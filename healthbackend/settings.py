import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-only-key-change-in-production')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_filters',
    'graphql_jwt',
    'graphene_django',
    'channels',
    'django_rest_passwordreset',
    'anymail',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

_cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if _cors_origins:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_origins.split(',') if o.strip()]
else:
    CORS_ALLOW_ALL_ORIGINS = True  # Development only

ROOT_URLCONF = 'healthbackend.urls'
ASGI_APPLICATION = 'healthbackend.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'project_templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'core.User'

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

GRAPHENE = {
    'SCHEMA': 'core.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_ALLOW_ARGUMENT': True,
}

_redis_url = os.environ.get('REDIS_URL', '')
if _redis_url:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [_redis_url]},
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

APPEND_SLASH = False

USE_TZ = True
TIME_ZONE = 'Africa/Nairobi'

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'
)

_mailtrap_token = os.environ.get('MAILTRAP_API_TOKEN', '')
if _mailtrap_token:
    ANYMAIL = {"MAILTRAP_API_TOKEN": _mailtrap_token}

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@smarthealth.com')

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:8081')
BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:8000')

# Production security hardening (only active when DEBUG=False)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Django REST Password Reset Configuration
DJANGO_REST_PASSWORDRESET = {
    'TOKEN_EXPIRY_TIME': 30,  # in minutes
    'EMAIL_SUBJECT': 'Password Reset Request - Smart Expert Mental Health Support',
    'EMAIL_HTML_PATH': 'email/user_reset_password.html',
    'EMAIL_PLAINTEXT_PATH': 'email/user_reset_password.txt',
    'EMAIL_FROM_EMAIL': os.environ.get('DEFAULT_FROM_EMAIL', 'hello@demomailtrap.co'),
    'EMAIL_REPLY_TO_EMAIL': os.environ.get('DEFAULT_FROM_EMAIL', 'hello@demomailtrap.co'),
    'PASSWORD_RESET_TOKEN_USUARIO_PATH': 'api/password_reset/token/',
    'GOOGLE_RECAPTCHA_SECRET_KEY': None,
    'PASSWORD_RESET_EMAIL_SUBJECT': 'Password Reset Request - Smart Expert Mental Health Support',
    'PASSWORD_RESET_EMAIL_HTML_PATH': 'email/user_reset_password.html',
    'PASSWORD_RESET_EMAIL_PLAINTEXT_PATH': 'email/user_reset_password.txt',
    'PASSWORD_RESET_EMAIL_FROM_EMAIL': os.environ.get('DEFAULT_FROM_EMAIL', 'hello@demomailtrap.co'),
    'PASSWORD_RESET_EMAIL_REPLY_TO_EMAIL': os.environ.get('DEFAULT_FROM_EMAIL', 'hello@demomailtrap.co'),
    'PASSWORD_RESET_EMAIL_TOKEN_GENERATOR_CLASS': 'django_rest_passwordreset.tokens.RandomNumberTokenGenerator',
    'PASSWORD_RESET_EMAIL_SALT': None,
}
