# Django settings for rm project.
import dj_database_url
import ffs

ROOT = ffs.Path(__file__).parent

import djcelery
djcelery.setup_loader()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('David Miller', 'david@openhealthcare.org.uk'),
)

MANAGERS = ADMINS
DATABASES = {'default': dj_database_url.config(default='sqlite:///rm.sqlite')}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/usr/local/ohc/var/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/usr/local/ohc/var/media/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    str(ROOT / 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$_7x-n3d33#0v$&2wgm%10lr=_ybns354gtqi2=kyitclj65q_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django_jinja2.loaders.filesystem.Loader',
    'django_jinja2.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'rm.context.sett',
)


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # 'django_cas.backends.CASBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_cas.middleware.CASMiddleware',
    'rm.middleware.BasicAuthMiddleware'
)

ROOT_URLCONF = 'rm.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rm.wsgi.application'

TEMPLATE_DIRS = (
    ROOT / 'templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    # 3rd Party

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrapform',
    # 'django_cas',
    'django_extensions',
    'djcelery',
    'sorl.thumbnail',
    'form_utils',
    'rm.gcapp',
    'grappelli',
    'django.contrib.admin',

    'south',
    'terms',
    # Our Apps
    'rm.trials',
    'rm.userprofiles',
    'rm.gcapp',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_USER_MODEL = 'userprofiles.RMUser'

CAS_SERVER_URL = 'http://auth.openhealthcare.org.uk'
CAS_REDIRECT_URL = '/'
CAS_IGNORE_REFERER = True
CAS_AUTO_CREATE_USERS = True
CAS_USE_EXTRA = True
LOGIN_REDIRECT_URL = '/'

# 3rd party app settings
GRAPPELLI_ADMIN_TITLE = 'Randomise.me'
SOUTH_TESTS_MIGRATE = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
TERMS_REPLACE_FIRST_ONLY = False
THUMBNAIL_DEBUG = True

# Our Settings

BASICAUTH = True

# Dummy settings as a reminder
BASICAUTH_PASSWORD = 'notareal password dummy'
BASICAUTH_USERNAME = 'notareal username dummy'
EMAIL_HOST = 'example.com'
EMAIL_HOST_USER = 'notareal username dummy'
EMAIL_HOST_PASSWORD = 'notareal password dummy'
DEFAULT_FROM_EMAIL = 'Randomise Me <www@randomizeme.org>'
CONTACT_EMAIL = 'nospam@example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_DOMAIN = 'http://byta.randomizeme.org'

GC_APP_ID = 'Not a real ID'
GC_APP_SECRET = 'Not a real secret'
GC_ACCESS_TOKEN = 'Not a real token'
GC_MERCHANT_ID = '0BF5SJEGEH'
GC_ENVIRONMENT = 'sandbox'

try:
    from local_settings import *
except:
    pass
