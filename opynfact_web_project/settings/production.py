"""
Django settings for opynfact_web_project project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import logging

from . import *
from .zenvar import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!

SECRET_KEY = KEY

DEBUG = False
ALLOWED_HOSTS = [IP_HOST]


# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_REFERRER_POLICY = True


# Application definition

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': DB_NAME, # le nom de notre base de donnees creee precedemment
        'USER': DB_USER, # attention : remplacez par votre nom d'utilisateur
        'PASSWORD': DB_PWD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# AUTH_USER_MODEL = 'account.ZUser'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators



# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


    
# Static files settings
STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),       # 'staticfiles'
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.DEBUG,        # Capture info and above as breadcrumbs
    event_level=logging.INFO  # Send errors as events
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration(), sentry_logging],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

CRONJOBS = [
    ('*/1 * * * *', 'product.cron.my_scheduled_job', '>> /tmp/scheduled_job.log'),
    # ('*/3 * * * *', 'migrate', '>> /tmp/sch_job.log'),
    # ('*/3 * * * *', echo "la tete a toto", '>> /tmp/sch_job2.log'),
    # ('*/10   * * * *', 'django.core.management.call_command', ['initializedatabase 0']),
    ('*/15 * * * *', 'django.core.management.call_command', ['initializedatabase 0'], {}, '>> /tmp/backups_3.log'),
    # ('*/20 * * * *', 'product.management.commands.initializedatabase', ['0'], '> /home/miket2/backups/last_sunday_auth_backup.json'),
]