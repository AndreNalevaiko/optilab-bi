import decimal
from datetime import datetime, timedelta, date
import dateutil.relativedelta
from calendar import monthrange

from optilab_bi import user_manager, db_metrics

from flask import Blueprint, jsonify, request

actions = Blueprint('/product', __name__, url_prefix='/product')

select_products_by_wallet = """
    SELECT
    c.product,
    c.product_group,
    c.wallet wallet,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.{column_current_values}_amount / 2, 0 )) / {last_month} avg_month_qtd_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.{column_current_values}_value, 0 )) / {last_month} avg_month_value_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.{column_current_values}_amount / 2, 0 )) qtd_current_month,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.{column_current_values}_value, 0 )) value_current_month
    FROM consolidation c
    WHERE date BETWEEN '{init_date}' AND '{end_date}'
    AND wallet in ({wallets})
    AND c.product_group != ''
    group by product, product_group, wallet
    ORDER BY CASE WHEN c.product_group IN ('CRIZAL*', 'TRANSITIONS*') THEN 'WWWW'
              ELSE c.product_group END asc;
    """


select_products_global = """
    SELECT
    c.product,
    c.product_group,
    '0' _wallet,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.{column_current_values}_amount / 2, 0 )) / {last_month} avg_month_qtd_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.{column_current_values}_value, 0 )) / {last_month} avg_month_value_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.{column_current_values}_amount / 2, 0 )) qtd_current_month,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.{column_current_values}_value, 0 )) value_current_month
    FROM consolidation c
    WHERE date BETWEEN '{init_date}' AND '{end_date}'
    AND c.product_group != ''
    group by product, product_group, _wallet
    ORDER BY CASE WHEN c.product_group IN ('CRIZAL*', 'TRANSITIONS*') THEN 'WWWW'
              ELSE c.product_group END asc;
    """

select_products_others_wallet = """
    SELECT
    c.product,
    c.product_group,
    '' _wallet,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.{column_current_values}_amount / 2, 0 )) / {last_month} avg_month_qtd_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.{column_current_values}_value, 0 )) / {last_month} avg_month_value_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.{column_current_values}_amount / 2, 0 )) qtd_current_month,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.{column_current_values}_value, 0 )) value_current_month
    FROM consolidation c
    WHERE date BETWEEN '{init_date}' AND '{end_date}'
    AND wallet not in ({wallets})
    AND c.product_group != ''
    group by product, product_group, _wallet
    ORDER BY CASE WHEN c.product_group IN ('CRIZAL*', 'TRANSITIONS*') THEN 'WWWW'
              ELSE c.product_group END asc;
    """

def consolidate_result(result):
    return_ = []

    for row in result:
        keys = row.keys()
        obj = {}

        for key in keys:
            key_name = key

            # TODO Fix para group by funcionar corretamente
            if key[0] == '_':
                key_name = key.replace('_', '', 1)
                obj[key_name] = str(row[key])

            if isinstance(row[key], decimal.Decimal):
                obj[key] = str(row[key])
            elif isinstance(row[key], date) or isinstance(row[key], datetime):
                obj[key] = str(row[key])
            else:
                obj[key] = row[key]
        
        return_.append(obj)

    return return_


@actions.route('/billings', methods=['POST'])
@user_manager.auth_required('user')
def products(auth_data=None):
    params = request.get_json()

    with db_metrics.connect() as con:
        date = params.get('date')
        wallets = params.get('wallets')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        current_year = date.year
        last_year = date.year - 1
        current_month = date.month
        last_month = date.month - 1
        current_day = date.day

        if current_month == 1:
            last_month = current_month

        column_current_values = 'sold'
        if params.get('date_type', '') == 'created':
            column_current_values = 'accumulated_sold'

        init_date = date.replace(day=1, month=1, year=current_year).strftime('%Y-%m-%d')
        end_date = date.replace(day=current_day, month=current_month, year=current_year).strftime('%Y-%m-%d')

        wallets = ",".join(wallets)

        response = []

        sqls_ = [select_products_by_wallet, select_products_global, select_products_others_wallet]
        for sql_ in sqls_:
            sql = sql_.format(
            current_year=current_year,
            last_year=last_year,
            current_month=current_month,
            last_month=last_month,
            current_day=current_day,
            init_date=init_date,
            end_date=end_date,
            column_current_values=column_current_values,
            wallets=wallets,
            )

            result = con.execute(sql)
            response = response + consolidate_result(result)


    return jsonify(response)


@actions.route('/pillars/all_year', methods=['POST'])
@user_manager.auth_required('user')
def pillars_all_year(auth_data=None):
    params = request.get_json()
    result = {}
    with db_metrics.connect() as con:
        date = params.get('date')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        wallets = ','.join(params.get('wallets'))

        init_date = date.replace(day=1, month=1, year=date.year-1)
        init_date = init_date.strftime('%Y-%m-%d')
        end_date = date.strftime('%Y-%m-%d')

        column_current_values = 'sold'
        if params.get('date_type', '') == 'created':
            column_current_values = 'accumulated_sold'

        sql = """
        SELECT tp.wallet wallet, tp.product_group product_group, tp.ld dt, sum(tp.value) value FROM (
        SELECT wallet, product_group, date dt , LAST_DAY(date) ld, sum({column_current_values}_value) value
        FROM metrics.consolidation 
        where product_group != '' and date between '{init_date}' AND '{end_date}'
        and wallet in ({wallets})
        GROUP BY wallet, dt, ld, product_group
        UNION ALL
        SELECT '0' wallet, product_group, date dt , LAST_DAY(date) ld, sum({column_current_values}_value) value
        FROM metrics.consolidation 
        where product_group != '' and date between '{init_date}' AND '{end_date}'
        GROUP BY dt, ld, product_group
        UNION ALL
        SELECT '' wallet, product_group, date dt , LAST_DAY(date) ld, sum({column_current_values}_value) value
        FROM metrics.consolidation
        where product_group != '' and date between '{init_date}' AND '{end_date}'
        and wallet not in ({wallets})
        GROUP BY dt, ld, product_group
        ) as tp
        GROUP BY 1,2,3
        ORDER BY CASE WHEN tp.product_group IN ('CRIZAL*', 'TRANSITIONS*') THEN 'WWWW'
              ELSE tp.product_group END asc;
        """

        sql = sql.format(
            init_date=init_date,
            end_date=end_date,
            column_current_values=column_current_values,
            wallets=wallets,
        )

        result = con.execute(sql)
        result = consolidate_result(result)

        response = []
        wallets = []

        # Gera um consolidado para facilitar no frontend
        for item in result:
            product_finded = False
            
            if item['wallet'] in wallets:
                index = wallets.index(item['wallet'])

                for p in response[index]['products']:
                    if item['product_group'] == p['name']:
                        product_finded = True
                        p['periods'].append({'dt': item['dt'], 'value': item['value']})
                    
                if not product_finded:
                    response[index]['products'].append(
                        {
                            'name': item['product_group'], 
                            'periods': [{'dt': item['dt'], 'value': item['value']}]
                        }
                    )
            else:
                wallets.append(item['wallet'])
                response.append({'wallet': item['wallet'], 'products': []})

    return jsonify(response)


@actions.route('/bills_per_month', methods=['POST'])
@user_manager.auth_required('user')
def get_bills_per_month(auth_data=None):
    params = request.get_json()
    result = {}
    with db_metrics.connect() as con:
        date = params.get('date')
        wallet = params.get('wallet')
        product_group = params.get('product_group')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        last_month = date - dateutil.relativedelta.relativedelta(months=1)

        if date.year != last_month.year:
            init_date = date.replace(day=1, month=1, year=date.year-1).strftime('%Y-%m-%d')
        else:
            init_date = date.replace(day=1, month=1).strftime('%Y-%m-%d')

        end_date = date.strftime('%Y-%m-%d')

        sql = """
        SELECT 
        c.product_group product_group,
        c.product product_name,
        c.wallet wallet,
        DAY(LAST_DAY(c.date)) last_day_month,
        MONTH(c.date) month,
        YEAR(c.date) year,
        sum(c.sold_amount) / 2 month_qtd,
        sum(c.sold_value) month_value
        FROM metrics.consolidation c
        WHERE c.product_group = '{product_group}'
        AND c.date BETWEEN '{init_date}' AND LAST_DAY('{end_date}')
        AND wallet = {wallet}
        group by product_group, product_name, wallet, last_day_month, month, year;
        """.format(
            product_group=product_group,
            wallet=wallet,
            init_date=init_date,
            end_date=end_date,
        )

        result = con.execute(sql)
        result = consolidate_result(result)

    return jsonify(result)