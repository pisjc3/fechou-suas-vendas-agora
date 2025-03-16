from .base import *
from config.env import env

INSTALLED_APPS = ['whitenoise.runserver_nostatic'] + INSTALLED_APPS


DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
