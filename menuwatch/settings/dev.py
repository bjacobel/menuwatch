"""Development settings and globals."""

from os.path import join, normpath

from common import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'menuwatch',
        'USER': 'bjacobel',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## SECRET CONFIGURATION
SECRET_FILE = normpath(join(DJANGO_ROOT, 'settings/secret_key'))
SECRET_KEY = open(SECRET_FILE).read().strip()
########## END SECRET CONFIGURATION


########## MAILGUN CONFIGURATION
MAILGUN_FILE = normpath(join(DJANGO_ROOT, 'settings/mailgun_key'))
MAILGUN_ACCESS_KEY = open(MAILGUN_FILE).read().strip()
########## END MAILGUN CONFIGURATION


########## STRIPE CONFIGURATION
STRIPE_FILE = normpath(join(DJANGO_ROOT, 'settings/stripe_key'))
STRIPE_KEY = open(STRIPE_FILE).read().strip()
########## END STRIPE CONFIGURATION


########## CELERY CONFIGURATION
# See: http://docs.celeryq.org/en/latest/configuration.html#celery-always-eager
CELERY_ALWAYS_EAGER = True
########## END CELERY CONFIGURATION
