import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
CHARTIT_DIR = os.path.split(os.path.dirname(__file__))[0]
sys.path = [CHARTIT_DIR] + sys.path
PROJECT_ROOT = os.path.dirname(__file__)
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
SECRET_KEY = 'chartit-demo'
MANAGERS = ADMINS
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
CHARTIT_JS_REL_PATH = '/chartit/js/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'projectstatic'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)
INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'syntax_colorize',
    'chartit',
    'chartdemo',
    'pivotdemo',
)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

# All production settings like sensitive passwords go here.
# Remember to exclude this file from version control
try:
    from prod_settings_demo import * # noqa
except ImportError:
    pass
