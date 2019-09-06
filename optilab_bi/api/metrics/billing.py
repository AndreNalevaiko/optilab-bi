import decimal
from datetime import datetime, date, timedelta

from optilab_bi import user_manager, db_metrics

from flask import Blueprint, jsonify, request

actions = Blueprint('/billings', __name__, url_prefix='/billings')

def consolidate_result(result):
    return_ = []

    for row in result:
        keys = row.keys()
        obj = {}

        for key in keys:
            if isinstance(row[key], decimal.Decimal):
                obj[key] = str(row[key])
            elif isinstance(row[key], date) or isinstance(row[key], datetime):
                obj[key] = str(row[key])
            else:
                obj[key] = row[key]
        
        return_.append(obj)

    return return_


@actions.route('/', methods=['POST'])
@user_manager.auth_required('user')
def billings(auth_data=None):
    params = request.get_json()
    result = {}
    with db_metrics.connect() as con:
        date = params.get('date')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        wallets = ','.join(params.get('wallets'))

        init_date = date.replace(day=1).strftime('%Y-%m-%d')
        end_date = date.strftime('%Y-%m-%d')

        sql = """
        SELECT wallet, sum(total_value) value
        FROM metrics.consolidation 
        where company = '' and customer_name = '' and product_group = ''
        and date between '{init_date}' AND '{end_date}'
        and wallet in ({wallets})
        group by 1
        UNION ALL
        SELECT '0', sum(total_value) value
        FROM metrics.consolidation 
        where company = '' and customer_name = '' and product_group = ''
        and date between '{init_date}' AND '{end_date}'
        group by 1
        UNION ALL
        SELECT '', sum(total_value) value
        FROM metrics.consolidation 
        where company = '' and customer_name = '' and product_group = ''
        and date between '{init_date}' AND '{end_date}'
        and wallet not in ({wallets})
        group by 1
        order by 1;
        """

        sql = sql.format(
            init_date=init_date,
            end_date=end_date,
            wallets=wallets,
        )

        result = con.execute(sql)
        result = consolidate_result(result)

    return jsonify(result)


@actions.route('/all_year', methods=['POST'])
@user_manager.auth_required('user')
def billings_all_year(auth_data=None):
    params = request.get_json()
    result = {}
    with db_metrics.connect() as con:
        date = params.get('date')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        wallets = ','.join(params.get('wallets'))

        init_date = date.replace(day=1, month=1, year=date.year-1)
        init_date = init_date.strftime('%Y-%m-%d')
        end_date = date.strftime('%Y-%m-%d')

        sql = """
        SELECT tp.wallet wallet, tp.ld dt, sum(tp.value) value FROM (
        SELECT wallet, date dt , LAST_DAY(date) ld, sum(total_value) value
        FROM metrics.consolidation 
        where company = '' and customer_name = '' and product_group = '' and date between '{init_date}' AND '{end_date}'
        and wallet in ({wallets})
        GROUP BY wallet, dt, ld
        UNION ALL
        SELECT '0' wallet, date dt , LAST_DAY(date) ld, sum(total_value) value
        FROM metrics.consolidation 
        where company = '' and customer_name = '' and product_group = '' and date between '{init_date}' AND '{end_date}'
        GROUP BY dt, ld
        UNION ALL
        SELECT '' wallet, date dt , LAST_DAY(date) ld, sum(total_value) value
        FROM metrics.consolidation
        where company = '' and customer_name = '' and product_group = '' and date between '{init_date}' AND '{end_date}'
        and wallet not in ({wallets})
        GROUP BY dt, ld
        ) as tp
        GROUP BY 1,2;
        """

        sql = sql.format(
            init_date=init_date,
            end_date=end_date,
            wallets=wallets,
        )

        result = con.execute(sql)
        result = consolidate_result(result)

    return jsonify(result)
