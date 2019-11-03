import decimal
from datetime import date, datetime, timedelta

from optilab_bi import user_manager, db_metrics

from flask import Blueprint, jsonify, request

actions = Blueprint('/filters', __name__, url_prefix='/filters')

def consolidate_result(result):
    return_ = []

    for row in result:
        keys = row.keys()
        obj = {}

        for key in keys:
            if isinstance(row[key], decimal.Decimal):
                # obj[key] = str(row[key])
                obj[key] = row[key]
            elif isinstance(row[key], date) or isinstance(row[key], datetime):
                obj[key] = str(row[key])
            else:
                obj[key] = row[key]
        
        return_.append(obj)

    return return_

@actions.route('', methods=['GET'])
@user_manager.auth_required('user')
def search(auth_data=None):
    with db_metrics.connect() as con:

        sql = """
        SELECT wallet, state, city, neighborhood 
        from consolidation 
        where state != ''
        group by 1,2,3,4;
        """

        result = con.execute(sql)
        result = consolidate_result(result)        

    return jsonify(result)