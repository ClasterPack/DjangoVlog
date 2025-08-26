import os
from pathlib import Path

from DjangoVlog.config import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.django_secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.debug

ALLOWED_HOSTS = config.allowed_hosts


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.postgres',
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'adminsortable2',
    'app',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "DjangoVlog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoVlog.wsgi.application'
ASGI_APPLICATION = 'DjangoVlog.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.pg_name,
        'USER': config.pg_user,
        'PASSWORD': config.pg_password,
        'HOST': config.pg_host,
        'PORT': config.pg_port,
        'CONN_MAX_AGE': config.pg_max_age,
        'OPTIONS': {
            'connect_timeout': 5,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = config.django_language

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = config.static_url
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'app.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': config.page_size,
}
# Celery
CELERY_BROKER_URL = config.celery_broker
CELERY_RESULT_BACKEND = config.celery_result_backend
CELERY_TASK_ALWAYS_EAGER = config.celery_task_always_eager

# Логирование SQL при POSTGRES_ECHO=1
if config.pg_echo:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {'console': {'class': 'logging.StreamHandler'}},
        'loggers': {'django.db.backends': {'handlers': ['console'], 'level': 'DEBUG'}},
    }

# Django cache (Redis)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config.cache_url,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': config.title,
    'DESCRIPTION': 'Страницы и контент (Page, Video, Audio).',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}