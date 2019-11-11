from ..settings import *  # noqa
from envparse import env

env.read_envfile()

# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['f5bd9901.ngrok.io', '178.124.222.234', '127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASS'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.int('DB_PORT'),
    }
}