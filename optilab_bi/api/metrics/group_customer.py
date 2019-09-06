import decimal
from datetime import datetime, timedelta
from calendar import monthrange

from optilab_bi import user_manager, db_metrics

from flask import Blueprint, jsonify, request

actions = Blueprint('/group_customer', __name__, url_prefix='/group_customer')

def consolidate_result(result):
    return_ = []

    for row in result:
        keys = row.keys()
        obj = {}

        for key in keys:
            if isinstance(row[key], decimal.Decimal):
                obj[key] = str(row[key])
            else:
                obj[key] = row[key]
        
        return_.append(obj)

    return return_


@actions.route('/customers', methods=['POST'])
@user_manager.auth_required('user')
def get_customers(auth_data=None):
    params = request.get_json()
    result = {}
    with db_metrics.connect() as con:
        group = params.get('group')
        date = params.get('date')
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
        sql = """
        SELECT 
        c.wallet wallet,
        c.customer_code customer_code,
        c.customer_name customer_name,
        c.group_customer group_customer,
        sum(IF(year(c.date) = {last_year}, c.sold_amount / 2, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_qtd_last_year,
        sum(IF(year(c.date) = {last_year}, c.sold_value, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_value_last_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_amount / 2, 0 )) / {last_month} avg_month_qtd_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_value, 0 )) / {last_month} avg_month_value_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_amount / 2, 0 )) qtd_current_month,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_value, 0 )) value_current_month
        FROM metrics.consolidation c
        WHERE 1 = 1
        AND date BETWEEN '{init_date}' AND '{end_date}'
        AND group_customer = '{group}'
        AND c.product = '' AND c.product_group = ''
        group by customer_code, customer_name, group_customer, wallet
        """.format(
            current_year=current_year,
            last_year=last_year,
            current_month=current_month,
            last_month=last_month,
            current_day=current_day,
            init_date=init_date,
            end_date=end_date,
            group=group,
        )

        result = con.execute(sql)
        result = consolidate_result(result)

    return jsonify(result)


@actions.route('/bills_per_month', methods=['POST'])
@user_manager.auth_required('user')
def get_bills_per_month(auth_data=None):
    params = request.get_json()
    result = {}
    with db_metrics.connect() as con:
        date = params.get('date')
        group_customer = params.get('group_customer')
        period = params.get('period')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        current_year = date.year
        last_year = date.year - 1
        current_month = date.month
        current_day = date.day
        
        if period == 'last_year':
            init_date = date.replace(day=1, month=1, year=last_year).strftime('%Y-%m-%d')
            end_date = date.replace(day=31, month=12, year=last_year).strftime('%Y-%m-%d')
        else:
            init_date = date.replace(day=1, month=1, year=current_year).strftime('%Y-%m-%d')
            end_date = date.replace(day=current_day, month=current_month, year=current_year).strftime('%Y-%m-%d')

        sql = """
        SELECT 
        c.group_customer group_customer,
        DAY(LAST_DAY(c.date)) last_day_month,
        MONTH(c.date) month,
        YEAR(c.date) year,
        sum(c.sold_amount) / 2 month_qtd,
        sum(c.sold_value) month_value
        FROM metrics.consolidation c
        WHERE c.group_customer = '{group_customer}'
        AND c.date BETWEEN '{init_date}' AND '{end_date}'
        AND c.product = '' AND c.product_group = ''
        group by group_customer, last_day_month, month, year;
        """.format(
            group_customer=group_customer,
            init_date=init_date,
            end_date=end_date,
        )

        result = con.execute(sql)
        result = consolidate_result(result)

    return jsonify(result)

@actions.route('/products', methods=['POST'])
@user_manager.auth_required('user')
def products(auth_data=None):
    params = request.get_json()

    with db_metrics.connect() as con:
        group = params.get('group')
        date = params.get('date')
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

        sql = """
        SELECT
        c.product,
        c.product_group,
        sum(IF(year(c.date) = {last_year}, c.sold_amount / 2, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_qtd_last_year,
        sum(IF(year(c.date) = {last_year}, c.sold_value, 0 )) / count(distinct month(IF(year(c.date) = {last_year}, c.date, null))) avg_month_value_last_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_amount / 2, 0 )) / {last_month} avg_month_qtd_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_value, 0 )) / {last_month} avg_month_value_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_amount / 2, 0 )) qtd_current_month,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_value, 0 )) value_current_month
        FROM consolidation c
        WHERE c.group_customer = '{group}'
        AND date BETWEEN '{init_date}' AND '{end_date}'
        AND c.product_group != ''
        group by product, product_group
        """


        # for column in metrics_columns:
        sql_ = sql.format(
            current_year=current_year,
            last_year=last_year,
            current_month=current_month,
            last_month=last_month,
            current_day=current_day,
            group=group,
            init_date=init_date,
            end_date=end_date,
        )

        result = con.execute(sql_)

    return jsonify(consolidate_result(result))