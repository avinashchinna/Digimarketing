import dj_database_url
from .base import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {}
DATABASES['default'] =  dj_database_url.config()
