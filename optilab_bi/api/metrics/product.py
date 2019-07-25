import decimal
from datetime import datetime, timedelta
from calendar import monthrange

from optilab_bi import user_manager, db_metrics

from flask import Blueprint, jsonify, request

actions = Blueprint('/product', __name__, url_prefix='/product')

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
def products(auth_data=None):
    params = request.get_json()

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

        init_date = date.replace(day=1, month=1, year=last_year).strftime('%Y-%m-%d')
        end_date = date.replace(day=current_day, month=current_month, year=current_year).strftime('%Y-%m-%d')

        sql = """
        SELECT
        c.product,
        c.product_group,
        c.wallet,
        sum(IF(year(c.date) = {last_year}, c.sold_amount, 0 )) / 12 avg_month_qtd_last_year,
        sum(IF(year(c.date) = {last_year}, c.sold_value, 0 )) / 12 avg_month_value_last_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_amount, 0 )) / {last_month} avg_month_qtd_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) <= {last_month}, c.sold_value, 0 )) / {last_month} avg_month_value_current_year,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_amount, 0 )) qtd_current_month,
        sum(IF(year(c.date) = {current_year} and month(c.date) = {current_month} and day(c.date) <= {current_day}, c.sold_value, 0 )) value_current_month
        FROM consolidation c
        WHERE date BETWEEN '{init_date}' AND '{end_date}'
        group by product, product_group, wallet
        """


        # for column in metrics_columns:
        sql_ = sql.format(
            current_year=current_year,
            last_year=last_year,
            current_month=current_month,
            last_month=last_month,
            current_day=current_day,
            customer=customer,
            init_date=init_date,
            end_date=end_date,
        )

        result = con.execute(sql_)

    return jsonify(consolidate_result(result))