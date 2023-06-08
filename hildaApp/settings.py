"""
Django settings for hildaApp project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# read th .env file
environ.Env.read_env()

# environ init
env = environ.Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'data',
    'main',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'corsheaders',
    'rest_framework',
    # 'import_export',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hildaApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hildaApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# The real one
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': env('APPDATA'),
#         'USER': env('USER_DB'),
#         'PASSWORD': env('PASSWORD'),
#         'HOST': env('HOST'),
#         'PORT': env('PORT'),
#         'ATOMIC_REQUEST': env('ATOMIC_REQUEST')
#     },
#     'hilda_data': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': env('DB'),
#         'USER': env('USER_DB'),
#         'PASSWORD': env('PASSWORD'),
#         'HOST': env('HOST'),
#         'PORT': env('PORT'),
#         'ATOMIC_REQUEST': env('ATOMIC_REQUEST')
#     },
# }

# The development one
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3-app',
    },
    'hilda_data': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3-data',
    },
}

DATABASE_ROUTERS = [
    'data.data_router.DataRouter',
]

# Default User model for the app
AUTH_USER_MODEL = 'main.CustomUser'

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PSWD_MODULE="django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{AUTH_PSWD_MODULE}UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{AUTH_PSWD_MODULE}MinimumLengthValidator',
    },
    {
        'NAME': f'{AUTH_PSWD_MODULE}CommonPasswordValidator',
    },
    {
        'NAME': f'{AUTH_PSWD_MODULE}NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# To redirect to home after login django admin
LOGIN_REDIRECT_URL = 'home'

# Group names with special permissions
REGISTER_ENABLED_GROUPS = ['Admin', 'Superboss', 'Manager']
