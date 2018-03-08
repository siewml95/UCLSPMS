import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL_HOST_USER = 'contact.notice.board.18@gmail.com'

DEBUG = True

SITE_URL = "localhost:8000"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_PLUGINS = [
    'django_nose_qunit.QUnitPlugin'
]
NOSE_ARGS = [
    '--with-django-qunit',
    '--nologcapture',
    '--verbosity=0'
]
