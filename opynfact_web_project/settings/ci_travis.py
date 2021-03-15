from . import *

SECRET_KEY = "tete_a_toto"
DEBUG = False
ALLOWED_HOSTS = []


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

STATIC_ROOT = os.path.join(PROJECT_DIR, "staticfiles")

# STATICFILES_DIRS = (
#     os.path.join(PROJECT_DIR, 'staticfiles'),       #'static'
# )
