from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# settings.py
INSTALLED_APPS = [
    # Other installed apps
    'rest_framework',
    'rest_framework.authtoken',
    'djangoapi',
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
