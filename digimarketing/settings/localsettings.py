# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # DO NOT MODIFY ENGINE
        'NAME': 'postgres', # DATABASE NAME
        'USER': 'avinash', # USERNAME  
        'PASSWORD': 'postgres', # PASSWORD
        'HOST': 'localhost',    # HOST
        'PORT': '5432',     # PORT
    }
}
