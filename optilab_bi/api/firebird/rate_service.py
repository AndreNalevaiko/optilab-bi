from datetime import date, timedelta, datetime
import numpy as np

from flask import Blueprint, jsonify, request
from optilab_bi import get_connection
from optilab_bi.api.firebird.sqls.rate_service import group_by_types

actions = Blueprint('rate_service', __name__, url_prefix='/rate_service')

@actions.route('/_generate', methods=['GET'])
def rate_service():
    connection = get_connection()
    session = connection.cursor()

    sql = group_by_types()

    data_ini = request.args.get('data_ini')
    data_final = request.args.get('data_final')
    sql = sql.format(
        data_ini=datetime.strptime(data_ini, '%d/%m/%Y').strftime('%m/%d/%Y'),
        data_final=datetime.strptime(data_final, '%d/%m/%Y').strftime('%m/%d/%Y')
    )

    session.execute(sql)
    
    results = session.fetchall()
    result_list = []

    for row in results:
        rate = {}

        rate['type'] = row[0].replace(' ', '')
        rate['order'] = row[1]
        rate['product'] = row[2]
        rate['business'] = row[3]
        rate['cli_nome_fan'] = row[4]
        rate['month'] = row[5]
        rate['year'] = row[6]

        rate['start_date'] = row[7].replace(hour=row[8].hour, second=row[8].second, minute=row[8].minute)

        rate['end_date'] = row[9].replace(hour=row[10].hour, second=row[10].second, minute=row[10].minute)

        dif_date = (rate['end_date'] - rate['start_date'])

        if dif_date.days > 0:
            rate['hours'] = (dif_date.days * 24) + dif_date.seconds / 60 / 60
        else:
            rate['hours'] = dif_date.seconds / 60 / 60

        # rate['days'] = dif_date.days
        rate['days'] = (row[9] - row[7]).days

        date_ini_ord = row[7].toordinal()
        date_end_ord = row[9].toordinal()
        weekend_days = 0

        for d_ord in range(date_ini_ord, date_end_ord):
            d = date.fromordinal(d_ord)
            if (d.weekday() == 6) or (d.weekday() == 5):
                weekend_days = weekend_days + 1

        rate['working_days'] = rate['days'] - weekend_days
        rate['working_hours'] = (rate['working_days'] * 24) + dif_date.seconds / 60 / 60


        result_list.append(rate)

    connection.close()

    return jsonify(result_list)