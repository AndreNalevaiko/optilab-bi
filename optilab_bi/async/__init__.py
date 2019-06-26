import logging
import os

from celery import Celery

LOGGER = logging.getLogger(__name__)

_config = {
    'BROKER_URL': os.environ['BROKER_URL'],
    'CELERY_RESULT_BACKEND': os.environ['CELERY_RESULT_BACKEND'],
    'CELERY_ACCEPT_CONTENT': ['json'],
    'CELERY_TASK_SERIALIZER': 'json',
    'CELERY_RESULT_SERIALIZER': 'json',
    'CELERY_ROUTES': {
        'metrics.tasks.consolidate_all': {'queue': 'metrics-consolidate'},
    }
}

celery = Celery(__name__)
celery.config_from_object(_config)