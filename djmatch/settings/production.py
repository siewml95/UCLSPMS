from .base import PIPELINE
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL_HOST_USER = 'contact.notice.board.18@gmail.com'


DEBUG = False
PIPELINE['PIPELINE_ENABLED'] = True
SITE_URL = "http://djmatch.herokuapp.com"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}
