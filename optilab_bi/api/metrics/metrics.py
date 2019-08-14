import logging
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from optilab_bi.async import metrics

__autor__ = 'Andre'

logger = logging.getLogger(__name__)

actions = Blueprint('/metrics', __name__, url_prefix='/metrics')

@actions.route('/_consolidate', methods=['POST'])
def _consolidate():
    """
    Envia uma ou mais métricas para consolidação.
    """

    data = request.get_json(silent=True) or {}

    logger.info('Consolidando as métricas %s', data)

    # Se não foi informado uma data, será consolidada a data de ontem
    date = datetime.utcnow() - timedelta(days=1)

    if 'date' in data:
        date = datetime.strptime(data['date'], '%Y-%m-%d')
    else:
        date = date.replace(hour=0, minute=0, second=0)

    end_at = date
    if 'end_at' in data:
        end_at = datetime.strptime(data['end_at'], '%Y-%m-%d')

    logger.info('De %s até %s', date, end_at)

    diff = end_at - date

    if diff.days < 0:
        return 'Invalid range of dates', 400

    for i in range(diff.days + 1):
        call_consolidation(None, date)

        date = date + timedelta(days=1)

    return 'OK'


def call_consolidation(metric, date):
    start_datetime = date.strftime('%Y-%m-%d %H:%M:%S')
    end_datetime = date.strftime('%Y-%m-%d %H:%M:%S')

    print('%s  /  %s' % (start_datetime, end_datetime))

    metrics.consolidate_all(start_datetime, end_datetime)