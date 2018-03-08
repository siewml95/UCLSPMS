import os
from dotenv import load_dotenv
from .base import *


dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

if os.environ.get('DJANGO_PRODUCTION') == True or os.environ.get('DJANGO_PRODUCTION') == 'True':
      from .production import *
else :
      from .development import *
