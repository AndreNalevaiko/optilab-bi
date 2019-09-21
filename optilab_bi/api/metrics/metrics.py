import logging, calendar
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from optilab_bi.async import metrics
from optilab_bi import db_metrics

__autor__ = 'Andre'

logger = logging.getLogger(__name__)

actions = Blueprint('/metrics', __name__, url_prefix='/metrics')


def clean_consolidations_period(init_date, end_date):
    if not init_date or not end_date:
        return

    with db_metrics.connect() as con:
        
        sql = """
        DELETE FROM consolidation WHERE date(date) between '{init_date}' and '{end_date}'
        """.format(init_date=init_date, end_date=end_date)

        result = con.execute(sql)
    
    return 'OK'

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

    last_day_of_month = calendar.monthrange(date.year, date.month)[1]

    if not 'end_at' in data and date.day in (15, last_day_of_month):
        # Se não é um range e é dia 15 ou o ultimo dia do mes reconsolida o mes inteiro
        clean_consolidations_period(date.strftime('%Y-%m-01') , date.strftime('%Y-%m-{}'.format(last_day_of_month)))

        if date.day == 15:
            end_at = date.replace(day=15)
        else:
            end_at = date.replace(day=last_day_of_month)

        date = date.replace(day=1)
    
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