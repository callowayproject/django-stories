# Django settings for example project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
import os, sys
APP = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(APP)
sys.path.append(PROJECT_ROOT)
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dev.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g2_39yupn*6j4p*cg2%w643jiq-1n_annua*%i8+rq0dx9p=$n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'stories',
    'categories',
    'editor',
    'reversion',
    'tinymce',
    'mptt',
    'simpleapp',
    'simpleprofile',
)
cleanup = """
tinyMCE.editors['id_body'].onPostProcess.add(
    function(ed, o) {
        if (o.get) {
            o.content = o.content.replace(/"(?=\w|$)/g, "&rdquo;");
            o.content = o.content.replace(/\b"/g, "&ldquo;");
            o.content = o.content.replace(/'(?=\w|$)/g, "&rsquo;");
            o.content = o.content.replace(/\b'/g, "&lsquo;");
            o.content = o.content.replace(/--/g, "&mdash;");
}});
"""
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'relative_urls': False,
    'plugins': "safari,paste,advimage,advlink,preview,fullscreen,media,searchreplace",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,blockquote,|,bullist,numlist,|,link,unlink,|,charmap,image,media,pastetext,pasteword,search,replace,|,code,fullscreen,preview",
    'theme_advanced_buttons2' : "",
    'theme_advanced_buttons3' : "",
    'theme_advanced_statusbar_location' : "bottom",
    'width': "600",
    'height': "600",
}

TINYMCE_ADMIN_FIELDS = {
    'stories.story': ('body',),
}
STORY_SETTINGS = {
    'RELATION_MODELS': ('simpleapp.basicthing','stories.story',),
    'PAGINATION': {
        'PAGINATE': True,
        'P_PER_PAGE': 5,
        'ORPHANS': 1
    },
    'THROW_404': False,
}

AUTH_PROFILE_MODULE = 'simpleprofile.Profile'

try:
    from local_settings import *
except ImportError:
    pass