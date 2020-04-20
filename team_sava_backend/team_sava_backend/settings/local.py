import os
from .base import *


"""
Place here environment dedicated settings that is not secret
"""

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'celery_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'team_sava_backend/logs/views.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
        },
        'errors_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'team_sava_backend/logs/errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'celery.logger': {
            'handlers': ['celery_handler'],
            'level': 'DEBUG',
        },
    },
}

DOMAIN = "http://localhost:3000"

CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_IMPORTS = ('custom_auth.tasks',)
