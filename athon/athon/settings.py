"""
Django settings for athon project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import pkg_resources
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0%2p6@m&wxw--sims@rzq6pdg6q1e0&z2s83knwhbzoum#$w9m'

SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/fantazzi-emails'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'jovannovkovic86@gmail.com'
EMAIL_HOST_PASSWORD = 'asterix86'
DEFAULT_FROM_EMAIL = 'Athon'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'taggit',

    'imagestore',
    'sorl.thumbnail',
    'tagging',
    'athon',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'athon.urls'

WSGI_APPLICATION = 'athon.wsgi.application'

ACCOUNT_ACTIVATION_DAYS = 7

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': os.environ.get('DB_NAME', "athon"),
        'USER': os.environ.get('DB_USER', "athon"),
        'PASSWORD': os.environ.get('DB_PASSWD', "athon123"),
        'HOST': os.environ.get('DB_HOST', "localhost"),
        'PORT': int(os.environ.get('DB_PORT', 5432)),
        # just in case, add the test database stuff here also
        'TEST_CHARSET': "utf8",
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Enable Connection Pooling
DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
DEFAULT_MEDIA_PATH = "media"
MEDIA_ROOT = os.path.join(BASE_DIR, DEFAULT_MEDIA_PATH)
MEDIA_URL = '/%s/' % DEFAULT_MEDIA_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = "static"
# STATIC_ROOT = os.path.join(BASE_DIR, STATIC_FOLDER)
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/%s/' % STATIC_FOLDER

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'drf_toolbox.serializers.ModelSerializer',
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/min',
        'user': '180/min'
    },
    'MAX_PAGINATE_BY': 10000,
}

#
# SWAGGER_SETTINGS = {
# "exclude_namespaces": ["swagger_excluded"],
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

