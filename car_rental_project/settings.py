"""
Django settings for car_rental_project project.
Modified for Render deployment.
"""

from pathlib import Path
import os
import dj_database_url # Optionnel mais recommandé pour Render

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
# En production, ne jamais laisser la clé en dur. 
# Render pourra lire la variable d'environnement 'SECRET_KEY'
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-=m#hqro=7#%#h2q!_q2q3q9#-81xh@z_j4z(s6@1=do_m0=#_o')

# DEBUG est True en local, mais devient False sur Render
DEBUG = 'RENDER' not in os.environ

# Autorise localhost et l'URL de ton futur site Render
ALLOWED_HOSTS = ['*'] # Tu pourras restreindre à ['ton-app.onrender.com'] plus tard

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'car_rental',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # AJOUTÉ ICI pour les fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'car_rental_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'car_rental_project.wsgi.application'

# Database
# Utilise SQLite en local, mais prêt pour une DB externe sur Render si besoin
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Tunis'
USE_I18N = True
USE_TZ = True

# Static & Media Configuration
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# Dossier où Django va rassembler tous les fichiers statiques pour la prod
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Optimisation WhiteNoise (compression des fichiers CSS/JS)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# AUTHENTICATION CONFIGURATION
LOGIN_URL = 'login' 
LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/'

# Email (Console pour le dev)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'