import decimal
from datetime import datetime, timedelta
from calendar import monthrange

from optilab_bi import user_manager, db_metrics

from flask import Blueprint, jsonify, request

actions = Blueprint('/product', __name__, url_prefix='/product')

select_products_by_wallet = """
    SELECT
    c.product,
    c.product_group,
    c.wallet wallet,
    sum(IF(year(c.date) = {last_year}, c.sold_amount, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_qtd_last_year,
    sum(IF(year(c.date) = {last_year}, c.sold_value, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_value_last_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_amount, 0 )) / {last_month} avg_month_qtd_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_value, 0 )) / {last_month} avg_month_value_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_amount, 0 )) qtd_current_month,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_value, 0 )) value_current_month
    FROM consolidation c
    WHERE date BETWEEN '{init_date}' AND '{end_date}'
    AND c.product_group != ''
    group by product, product_group, wallet
    """


select_products_global = """
    SELECT
    c.product,
    c.product_group,
    'Global' _wallet,
    sum(IF(year(c.date) = {last_year}, c.sold_amount, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_qtd_last_year,
    sum(IF(year(c.date) = {last_year}, c.sold_value, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_value_last_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_amount, 0 )) / {last_month} avg_month_qtd_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_value, 0 )) / {last_month} avg_month_value_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_amount, 0 )) qtd_current_month,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_value, 0 )) value_current_month
    FROM consolidation c
    WHERE date BETWEEN '{init_date}' AND '{end_date}'
    AND c.product_group != ''
    group by product, product_group, _wallet
    """

select_products_others_wallet = """
    SELECT
    c.product,
    c.product_group,
    'Others' _wallet,
    sum(IF(year(c.date) = {last_year}, c.sold_amount, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_qtd_last_year,
    sum(IF(year(c.date) = {last_year}, c.sold_value, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_value_last_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_amount, 0 )) / {last_month} avg_month_qtd_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_value, 0 )) / {last_month} avg_month_value_current_year,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_amount, 0 )) qtd_current_month,
    sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_value, 0 )) value_current_month
    FROM consolidation c
    WHERE date BETWEEN '{init_date}' AND '{end_date}'
    AND wallet not in ({wallets})
    AND c.product_group != ''
    group by product, product_group, _wallet
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

            if isinstance(row[key], decimal.Decimal):
                obj[key_name] = str(row[key])
            else:
                obj[key_name] = row[key]
        
        return_.append(obj)

    return return_

@actions.route('/billings', methods=['POST'])
@user_manager.auth_required('user')
def products(auth_data=None):
    params = request.get_json()

    with db_metrics.connect() as con:
        customer = params.get('customer')
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

        init_date = date.replace(day=1, month=1, year=last_year).strftime('%Y-%m-%d')
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
            customer=customer,
            init_date=init_date,
            end_date=end_date,
            wallets=wallets
            )

            result = con.execute(sql)
            response = response + consolidate_result(result)


    return jsonify(response)