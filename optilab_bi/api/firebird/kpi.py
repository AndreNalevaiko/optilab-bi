from datetime import datetime, timedelta
import calendar
from flask import Blueprint, jsonify, request
from optilab_bi import  get_connection, db
from optilab_bi.api.firebird.sqls.kpi import qtd_pedid, qtd_pecas_pedid, vlr_pedid
from optilab_bi.api.mysql import configuration
from optilab_bi.model import Kpi

actions = Blueprint('/kpi', __name__, url_prefix='/kpi')


def _consolidate_result(qtd_pedid, vlr_pedid, qtd_pecas):
    # business_codes = set([i[1] for i in qtd_pedid] + \ 
    #     [i[1] for i in qtd_pedid] + [i[1] for i in qtd_pedid])

    result = {}

    for row in qtd_pedid:
        if not result.get(row[1]):
            result[row[1]] = {}

        if not result.get(0):
            result[0] = {
                'qtd_pedid': 0,
                'vlr_pedid': 0,
                'qtd_pecas': 0,
                'business_code': 0
            }

        result[row[1]]['qtd_pedid'] = row[0]
        result[row[1]]['business_code'] = int(row[1])

        result[0]['qtd_pedid'] += row[0]

    for row in vlr_pedid:
        if not result.get(row[1]):
            result[row[1]] = {}

        if not result.get(0):
            result[0] = {
                'qtd_pedid': 0,
                'vlr_pedid': 0,
                'qtd_pecas': 0,
                'business_code': 0
            }

        result[row[1]]['vlr_pedid'] = row[0]
        result[row[1]]['business_code'] = int(row[1])

        result[0]['vlr_pedid'] += row[0]

    for row in qtd_pecas:
        if not result.get(row[1]):
            result[row[1]] = {}

        if not result.get(0):
            result[0] = {
                'qtd_pedid': 0,
                'vlr_pedid': 0,
                'qtd_pecas': 0,
                'business_code': 0
            }

        result[row[1]]['qtd_pecas'] = row[0]
        result[row[1]]['business_code'] = int(row[1])

        result[0]['qtd_pecas'] += row[0]

    return result


@actions.route('/_generate', methods=['POST'])
def _generate():
    date = request.get_json()

    if not date:
        date_now = datetime.now() - timedelta(days=1)
        date = {
            'year': date_now.year,
            'month': date_now.month,
            'day': date_now.day,
        }

    connection = get_connection()
    session = connection.cursor()

    date_now = datetime.now().replace(day=int(date['day']), month=int(date['month']), year=int(date['year']))
    
    previous_date = date_now - timedelta(days=1)
    date_fim = date_now - timedelta(days=2)
    date_ini = date_fim.replace(day=1)

    dates_formated = {
        'previous_date': previous_date.strftime('%m/%d/%Y'),
        'date_fim': date_fim.strftime('%m/%d/%Y'),
        'date_ini': date_ini.strftime('%m/%d/%Y'),
    }

    previous_is_valid = True

    if previous_date.isoweekday() in [6,7] or previous_date.month != date_fim.month:
        previous_is_valid = False

    list_cfop = configuration.get_config('cfop_vendas')

    sql_qtd_pedid = qtd_pedid()
    sql_vlr_pedid = vlr_pedid()
    sql_qtd_pecas = qtd_pecas_pedid()

    sql_qtd_pedid = sql_qtd_pedid.format(
        list_cfop=list_cfop,
        data_ini=dates_formated['date_ini'],
        data_fim=dates_formated['date_fim'])

    sql_vlr_pedid = sql_vlr_pedid.format(
        list_cfop=list_cfop,
        data_ini=dates_formated['date_ini'],
        data_fim=dates_formated['date_fim'])

    sql_qtd_pecas = sql_qtd_pecas.format(
        list_cfop=list_cfop,
        data_ini=dates_formated['date_ini'],
        data_fim=dates_formated['date_fim'])

    session.execute(sql_qtd_pedid)
    result_qtd_pedid = session.fetchall()

    session.execute(sql_vlr_pedid)
    result_vlr_pedid = session.fetchall()

    session.execute(sql_qtd_pecas)
    result_qtd_pecas = session.fetchall()

    result_average = _consolidate_result(result_qtd_pedid, result_vlr_pedid, result_qtd_pecas)

    if previous_is_valid:
        sql_qtd_pedid = qtd_pedid()
        sql_vlr_pedid = vlr_pedid()
        sql_qtd_pecas = qtd_pecas_pedid()

        sql_qtd_pedid = sql_qtd_pedid.format(
            list_cfop=list_cfop,
            data_ini=dates_formated['previous_date'],
            data_fim=dates_formated['previous_date'])

        sql_vlr_pedid = sql_vlr_pedid.format(
            list_cfop=list_cfop,
            data_ini=dates_formated['previous_date'],
            data_fim=dates_formated['previous_date'])

        sql_qtd_pecas = sql_qtd_pecas.format(
            list_cfop=list_cfop,
            data_ini=dates_formated['previous_date'],
            data_fim=dates_formated['previous_date'])

        session.execute(sql_qtd_pedid)
        result_qtd_pedid = session.fetchall()

        session.execute(sql_vlr_pedid)
        result_vlr_pedid = session.fetchall()

        session.execute(sql_qtd_pecas)
        result_qtd_pecas = session.fetchall()

        result_previous_date = _consolidate_result(result_qtd_pedid, result_vlr_pedid, result_qtd_pecas)

    for key, average in result_average.items():

        kpi = Kpi.query.filter(
            Kpi.business_code == average['business_code'],
            Kpi.month == date_fim.month,
            Kpi.year == date_fim.year,
        ).one_or_none()

        if not kpi:
            kpi = Kpi()
            kpi.business_code = average['business_code']
            kpi.month = date_fim.month
            kpi.year = date_fim.year
        
        kpi.date = date_now
        kpi.average_billing = average['vlr_pedid'] / date_fim.day
        kpi.average_order_quantity = average['qtd_pedid'] / date_fim.day
        kpi.average_quantity_pieces = average['qtd_pecas'] / date_fim.day
        kpi.average_tm = (average['vlr_pedid'] / date_fim.day) / (average['qtd_pedid'] / date_fim.day)
        
        db.session.add(kpi)

    if previous_is_valid:
        for key, previous_day in result_previous_date.items():

            kpi = Kpi.query.filter(
                Kpi.business_code == previous_day['business_code'],
                Kpi.month == date_fim.month,
                Kpi.year == date_fim.year,
            ).one_or_none()

            if kpi:
                kpi.date = date_now
                kpi.last_day_billing = previous_day['vlr_pedid']
                kpi.last_day_order_quantity = previous_day['qtd_pedid']
                kpi.last_day_quantity_pieces = previous_day['qtd_pecas']
                kpi.last_day_tm = previous_day['vlr_pedid'] / previous_day['qtd_pedid']
            
            db.session.add(kpi)

    db.session.commit()

    connection.close()

    return 'OK', 200