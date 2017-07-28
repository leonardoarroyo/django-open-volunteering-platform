#!/usr/bin/env python3
import glob
import os
import sys
import django
import threading

from django.conf import settings
from django.core.management import execute_from_command_line


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, (os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))))

# Unfortunately, apps can not be installed via ``modify_settings``
# decorator, because it would miss the database setup.
CUSTOM_INSTALLED_APPS = (
    'ovp.apps.core',
    'ovp.apps.uploads',
    'ovp.apps.users',
    'ovp.apps.projects',
    'ovp.apps.organizations',
    'ovp.apps.search',
    'ovp.apps.faq',
    'ovp.apps.channels',
    'haystack',
    'vinaigrette',
    'django.contrib.admin',
)

ALWAYS_INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

ALWAYS_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'PAGINATE_BY_PARAM': 'page_size',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

gettext = lambda s: s

settings.configure(
    SECRET_KEY="django_tests_secret_key",
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
    MEDIA_ROOT="/tmp",
    DEBUG=False,
    TEMPLATE_DEBUG=False,
    ALLOWED_HOSTS=[],
    INSTALLED_APPS=ALWAYS_INSTALLED_APPS + CUSTOM_INSTALLED_APPS,
    MIDDLEWARE_CLASSES=ALWAYS_MIDDLEWARE_CLASSES,
    ROOT_URLCONF='test.urls',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    LANGUAGES = (
      ('en-us', gettext('English')),
      ('pt-br', gettext('Portuguese')),
    ),
    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    STATIC_URL='/static/',
    # Use a fast hasher to speed up tests.
    PASSWORD_HASHERS=(
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ),
    FIXTURE_DIRS=glob.glob(BASE_DIR + '/' + '*/fixtures/'),
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.abspath(os.path.join(BASE_DIR, '../../templates'))],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    DEFAULT_SEND_EMAIL='sync',
    REST_FRAMEWORK=REST_FRAMEWORK,
    AUTH_PASSWORD_VALIDATORS=AUTH_PASSWORD_VALIDATORS,
    AUTH_USER_MODEL='users.User',
    OVP_CORE={
      'VALID_CONTACT_RECIPIENTS': ['testemail@1.com', 'testemail@2.com']
    },
    HAYSTACK_CONNECTIONS={
    'default': {
      'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
      'PATH': os.path.join('/tmp', 'ovp_test_whoosh_index'),
      },
    },
    HAYSTACK_SIGNAL_PROCESSOR='ovp.apps.search.signals.TiedModelRealtimeSignalProcessor',
)

django.setup()
args = [sys.argv[0], 'test']
test_cases = [
  'ovp.apps.core',
  'ovp.apps.uploads',
  'ovp.apps.users',
  'ovp.apps.organizations',
  'ovp.apps.projects',
  'ovp.apps.search',
  'ovp.apps.faq',
  'ovp.apps.channels',
]

# Allow accessing test options from the command line.
offset = 1
try:
    sys.argv[1]
except IndexError:
    pass
else: #pragma: no cover
    option = sys.argv[1].startswith('-')
    if not option:
        test_cases = sys.argv[1:]

args.extend(test_cases)
# ``verbosity`` can be overwritten from command line.
args.append('--verbosity=2')

execute_from_command_line(args)
