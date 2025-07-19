from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# settings.py
INSTALLED_APPS = [
    # Other installed apps
    'rest_framework',
    'rest_framework.authtoken',
    'djangoapi',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # SQLite database file in the project root
    }
}

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'  # Replace with actual email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'

ALLOWED_HOSTS = ['*']
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Make sure this is before AuthenticationMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Add other middlewares as needed...
]

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # Ensure app directories are scanned for templates
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ROOT_URLCONF = 'djangoapi.urls'
SECRET_KEY = '8*v+uyh19=1sksg5h2op37jxk*bs!1(3bbz8t2&h4xzvkw=k_3j'
