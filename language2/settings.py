# Django settings for language2 project.

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

TEMPLATE_DIRS = (
		TEMPLATE_PATH,
)


STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
STATIC_ROOT = os.path.join(STATIC_PATH, 'static_root')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
                        STATIC_PATH,
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

LOCALE_PATH = os.path.join(PROJECT_PATH, 'locale')
LOCALE_PATHS = (
		        LOCALE_PATH,
)

LOGIN_URL = os.path.join(TEMPLATE_PATH, '/user_login/')

gettext = lambda s: s
LANGUAGES = (
	        ('en', 'English'),
	        ('ru', 'Russian'),
	        ('fr', 'French'),
)

TINYMCE_JS_ROOT = os.path.join(STATIC_URL, "js/tiny_mce")
TINYMCE_JS_URL = os.path.join(TINYMCE_JS_ROOT, "tiny_mce.js")
TINYMCE_DEFAULT_CONFIG = {
                    'theme' : 'advanced',
                    'skin' : 'cirkuit',
                    'theme_advanced_resizing' : True,
                    'width' : '100%',
                    'plugins' : 'autosave',
                    'theme_advanced_resizing_min_height' : '440',
                    'theme_advanced_resizing_use_cookie' : False,
                    'theme_advanced_path' : False,
                    'theme_advanced_buttons1' : 'undo,redo,fontsizeselect,bold,italic,underline,separator,bullist,numlist,outdent,indent,separator,image,link,unlink',
}

BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a']
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style']
BLEACH_ALLOWED_STYLES = ['font-family']
BLEACH_STRIP_TAGS = True
BLEACH_DEFAULT_WIDGET = 'tinymce.models.HTMLField'

MANDRILL_API_KEY = 'bGma5A35VBJarb0i2DY-FA'
EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
import dj_database_url
DATABASES['default'] = dj_database_url.config()


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

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
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'os2w$q-28srwsoqn8fixhd@t0=bc_qhkz*0h&amp;75r2j$!ohg6!c'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
#)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'likes.middleware.SecretBallotUserIpUseragentMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'language2.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'language2.wsgi.application'

#TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'lambada',
    #'debug_toolbar',
    'djrill',
    'tinymce',
    #'sorl.thumbnail',
    #'mce_filebrowser',
    #'django_bleach',
    'bootstrapform',
    'secretballot',
    #'likes',
    'datetimewidget',
)
# !! This is needed for Debug Toolbar to work with Gunicorn.
#DEBUG_TOOLBAR_PATCH_SETTINGS = False
#INTERNAL_IPS = ('127.0.0.1',)
#DEBUG_TOOLBAR_CONFIG = {
#	'SHOW_TEMPLATE_CONTEXT': True,
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


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
