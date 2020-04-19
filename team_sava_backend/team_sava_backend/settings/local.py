from .base import *

"""
Place here environment dedicated settings that is not secret
"""

DOMAIN = "localhost:3000"

CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_IMPORTS = ('custom_auth.tasks',)
