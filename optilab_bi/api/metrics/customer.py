from datetime import datetime, timedelta
from calendar import monthrange

from optilab_bi import user_manager, db_metrics

from flask import Blueprint, jsonify, request

actions = Blueprint('/customer', __name__, url_prefix='/customer')

def consolidate_result(result):
    return_ = []

    for row in result:
        keys = row.keys()
        obj = {}

        for key in keys:
            obj[key] = row[key]
        
        return_.append(obj)

    return return_


# @user_manager.auth_required('user')
@actions.route('/teste', methods=['POST'])
def get_customers():
    params = request.get_json()
    with db_metrics.connect() as con:
        import ipdb; ipdb.set_trace()
        date = params.get('date')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        date_start = date.replace(year=date.year-1,month=1,day=1).strftime('%Y-%m-%d')
        date_end = date.strftime('%Y-%m-%d')

        sql = """
        SELECT * FROM consolidation
        WHERE date between '%s' and '%s'
        """ % (date_start, date_end)

        result = con.execute('SELECT * FROM consolidation')
        result = consolidate_result(result)

        result_past_year = [r for r in result if r['date'].year == date.year-1]
        result_current_year = [r for r in result if r['date'].year == date.year and r['date'].month != date.month]
        result_current_month = [r for r in result if r['date'].year == date.year and r['date'].month == date.month]



        return 'OK', 200