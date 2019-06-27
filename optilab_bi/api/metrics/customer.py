import decimal
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
            if isinstance(row[key], decimal.Decimal):
                obj[key] = str(row[key])
            else:
                obj[key] = row[key]
        
        return_.append(obj)

    return return_


@actions.route('/billings', methods=['POST'])
@user_manager.auth_required('user')
def get_customers(auth_data=None):
    params = request.get_json()
    result = {}
    with db_metrics.connect() as con:
        date = params.get('date')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        current_year = date.year
        last_year = date.year - 1
        current_month = date.month
        last_month = date.month - 1
        current_day = date.day

        if current_month == 1:
            last_month = current_month

        sql = """
        SELECT 
        c.wallet wallet,
        c.customer customer,
        sum(IF(year(c.date) = {last_year}, c.total_qtd, 0 )) / 12 avg_month_qtd_last_year,
        sum(IF(year(c.date) = {last_year}, c.total_value, 0 )) / 12 avg_month_value_last_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.total_qtd, 0 )) / {last_month} avg_month_qtd_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.total_value, 0 )) / {last_month} avg_month_value_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.total_qtd, 0 )) qtd_current_month,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.total_value, 0 )) value_current_month
        FROM metrics.consolidation c
        group by customer, wallet
        """.format(
            current_year=current_year,
            last_year=last_year,
            current_month=current_month,
            last_month=last_month,
            current_day=current_day,
        )

        result = con.execute(sql)
        result = consolidate_result(result)

    return jsonify(result)

@actions.route('/products', methods=['POST'])
@user_manager.auth_required('user')
def products(auth_data=None):
    params = request.get_json()
    result_ = []

    # Fazer get por config
    metrics_columns = [
        'varilux_geral',
        'varilux_trad',
        'varilux_digital',
        'varilux_trans',
        'varilux_digitime',
        'varilux_s',
        'varilux_x'
    ]

    with db_metrics.connect() as con:
        customer = params.get('customer')
        date = params.get('date')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        current_year = date.year
        last_year = date.year - 1
        current_month = date.month
        last_month = date.month - 1
        current_day = date.day

        if current_month == 1:
            last_month = current_month

        sql = """
        SELECT
        '{column}' product,
        sum(IF(year(c.date) = {last_year}, c.{column}_qtd, 0 )) / 12 avg_month_qtd_last_year,
        sum(IF(year(c.date) = {last_year}, c.{column}_value, 0 )) / 12 avg_month_value_last_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.{column}_qtd, 0 )) / {last_month} avg_month_qtd_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.{column}_value, 0 )) / {last_month} avg_month_value_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.{column}_qtd, 0 )) qtd_current_month,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.{column}_value, 0 )) value_current_month
        FROM consolidation c
        WHERE c.customer = '{customer}'
        group by product
        """


        for column in metrics_columns:
            sql_ = sql.format(
                column=column,
                current_year=current_year,
                last_year=last_year,
                current_month=current_month,
                last_month=last_month,
                current_day=current_day,
                customer=customer
            )

            result = con.execute(sql_)
            result_.append(consolidate_result(result)[0])

    return jsonify(result_)