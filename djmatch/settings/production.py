from .base import PIPELINE,dotenv_path
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL_HOST_USER = 'contact.notice.board.18@gmail.com'


DEBUG = False
PIPELINE['PIPELINE_ENABLED'] = True
SITE_URL = "http://djmatch.herokuapp.com"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  os.environ.get("SQL_NAME"),
        'USER': os.environ.get("SQL_USER"),
        'PASSWORD': os.environ.get("SQL_PASSWORD"),
        'HOST': os.environ.get("SQL_HOST"),
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
