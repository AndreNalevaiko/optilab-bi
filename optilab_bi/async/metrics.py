import logging

from . import celery

__autor__ = 'Andre'

LOGGER = logging.getLogger(__name__)

def consolidate_all(start_datetime, end_datetime):
    """
    Consolida uma métrica referente a data específica.
    """
    task = celery.signature('metrics.tasks.consolidate_all', args=[start_datetime, end_datetime])

    LOGGER.info('Enviando a tarefa %s', task)

    result = task.delay()

    LOGGER.info('Tarefa enviada: %s %s', task.task, result.id)