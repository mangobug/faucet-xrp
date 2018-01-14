"""
Django settings for xrp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# userprofile module settings
AUTH_PROFILE_MODULE = 'userprofile.userprofile'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7+*03gxajb(&a!ls+(qdpnu+c9#0_h@olt6y=tqimc8onp8*9n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    #external apps
    'south',
    'registration',
    'threadedcomments',
    'django.contrib.comments',
    'sorl.thumbnail',
    'storages',
    'tracking',
    'django-session-idle-timeout',

    #my apps
    'xrp.userprofile',
    'xrp.account',
    'xrp.institute',
    'xrp.course',
    'xrp.quiz',
)

MIDDLEWARE_CLASSES = (
    'tracking.middleware.VisitorTrackingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django-session-idle-timeout.middleware.SessionIdleTimeout',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'xrp.urls'

WSGI_APPLICATION = 'xrp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',#'django.db.backends.mysql',
#        'NAME': 'xrpdatabase', #os.path.join(BASE_DIR, 'xrpdb'),
#	    'USER': 'zain',
#	    'PASSWORD': '123456',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'xrpdatabase',
    }
}

# Parse database configuration from $DATABASE_URL
#import dj_database_url
#DATABASES['default'] =  dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')

MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = '/project_static/'
STATIC_ROOT = 'staticfiles'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATICFILES_DIRS = (
    #os.path.join(os.path.dirname(__file__), 'static'),
    os.path.join(BASE_DIR, 'static'),
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "xrp/templates/"),
)

ACCOUNT_ACTIVATION_DAYS = 7
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST ='smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

LOGIN_URL = '/'

COMMENTS_APP = 'threadedcomments'

SITE_ID = 1

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJNNPHXOC5N3XEOJQ'
AWS_SECRET_ACCESS_KEY = 'Iy5fiRy47s/lmgTAqWPZ1mjhLUUSZ9aJEuwavZgH'
AWS_STORAGE_BUCKET_NAME = 'xrpkids'
AWS_QUERYSTRING_AUTH = False
MEDIA_URL = 'http://%s.s3.amazonaws.com/your-folder/' % AWS_STORAGE_BUCKET_NAME

TRACK_AJAX_REQUESTS = True
TRACK_PAGEVIEWS = True
TRACK_QUERY_STRING = True

SESSION_IDLE_TIMEOUT = 1800
