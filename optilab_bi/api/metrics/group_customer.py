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


@actions.route('/billings', methods=['POST'])
@user_manager.auth_required('user')
def get_billings(auth_data=None):
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
        day_ytd = current_day

        ytd_columns, ytd_dimension, ytd_group_by = '', '', ''

        if current_month == 1:
            last_month = current_month

        # CASO SEJA ANO BISSEXTO NÃO IRÁ BUGAR
        try:
            datetime(year=last_year, month=current_month, day=current_day)
        except:
            day_ytd = current_day

        init_date = date.replace(day=1, month=1, year=last_year).strftime('%Y-%m-%d')
        end_date = date.replace(day=current_day, month=current_month, year=current_year).strftime('%Y-%m-%d')

        column_current_values = 'sold'
        if params.get('date_type', '') == 'created':
            column_current_values = 'accumulated_sold'

        if params.get('view_type', '') == 'ytd':
            ytd_columns = """
            ,SUM(IF(tmp.year = {last_year} AND tmp.month <= {current_month} AND tmp.day <= {day_ytd}, tmp.amount_solded / 2, 0)) ytd_qtd_last_year,
            SUM(IF(tmp.year = {last_year} AND tmp.month <= {current_month} AND tmp.day <= {day_ytd}, tmp.value_solded, 0)) ytd_value_last_year,
            SUM(IF(tmp.year = {current_year} AND tmp.month <= {current_month} AND tmp.day <= {current_day}, tmp.amount_solded / 2, 0)) ytd_qtd_current_year,
            SUM(IF(tmp.year = {current_year} AND tmp.month <= {current_month} AND tmp.day <= {current_day}, tmp.value_solded, 0)) ytd_value_current_year
            """.format(last_year=last_year, current_year=current_year, current_month=current_month, day_ytd=day_ytd, current_day=current_day)
            ytd_dimension = 'DAY(c.date) day,'
            ytd_group_by = ',5'

        custom_where = ''

        # Filtros de Estado, Cidade e bairro
        if params.get('searchFilters') and params['searchFilters'].get('states'):
            custom_where += ' AND c.state in ({})'.format(",".join(["'%s'" % val for val in params['searchFilters'].get('states')]))

        if params.get('searchFilters') and params['searchFilters'].get('cities'):
            custom_where += ' AND c.city in ({})'.format(",".join(["'%s'" % val for val in params['searchFilters'].get('cities')]))

        if params.get('searchFilters') and params['searchFilters'].get('neighborhoods'):
            custom_where += ' AND c.neighborhood in ({})'.format(",".join(["'%s'" % val for val in params['searchFilters'].get('neighborhoods')]))

        sql = """
        SELECT 
        tmp.wallet wallet,
        tmp.group_customer customer,
        tmp.group_customer customer_name,
        tmp.group_customer group_customer,
        AVG(if(tmp.year = {last_year} and tmp.amount_solded > 0, tmp.amount_solded / 2, null)) avg_month_qtd_last_year,
        AVG(if(tmp.year = {last_year} and tmp.value_solded > 0, tmp.value_solded, null)) avg_month_value_last_year,
        AVG(if(tmp.year = {current_year} and tmp.month <= {last_month} and tmp.amount_solded > 0, tmp.amount_solded / 2, null)) avg_month_qtd_current_year,
        AVG(if(tmp.year = {current_year} and tmp.month <= {last_month} and tmp.value_solded > 0, tmp.value_solded, null)) avg_month_value_current_year,
        SUM(IF(tmp.year = {current_year} and tmp.month = {current_month}, tmp.amount_solded / 2, 0)) qtd_current_month,
        SUM(IF(tmp.year = {current_year} and tmp.month = {current_month}, tmp.value_solded, 0)) value_current_month
        {ytd_columns}
        FROM (
            SELECT 
            c.wallet wallet,
            c.group_customer group_customer,
            {ytd_dimension}
            MONTH(c.date) month,
            YEAR(c.date) year,
            SUM(c.{column_current_values}_amount) amount_solded,
            SUM(c.{column_current_values}_value) value_solded
            FROM metrics.consolidation c
            WHERE 1 = 1
            AND date BETWEEN '{init_date}' AND '{end_date}'
            {custom_where}
            AND c.product = '' AND c.product_group = '' and c.group_customer != ''
            group by 1,2,3,4,{ytd_group_by}
        ) as tmp
        GROUP BY 1,2,3,4;
        """.format(
            current_year=current_year,
            last_year=last_year,
            current_month=current_month,
            last_month=last_month,
            init_date=init_date,
            end_date=end_date,
            custom_where=custom_where,
            column_current_values=column_current_values,
            ytd_columns=ytd_columns,
            ytd_dimension=ytd_dimension,
            ytd_group_by=ytd_group_by
        )

        result = con.execute(sql)
        result = consolidate_result(result)

    return jsonify(result)


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

        column_current_values = 'sold'
        if params.get('date_type', '') == 'created':
            column_current_values = 'accumulated_sold'

        sql = """
        SELECT 
        tmp.wallet wallet,
        tmp.customer_code customer_code,
        tmp.customer_name customer_name,
        tmp.group_customer group_customer,
        AVG(if(tmp.year = {last_year} and tmp.amount_solded > 0, tmp.amount_solded / 2, null)) avg_month_qtd_last_year,
        AVG(if(tmp.year = {last_year} and tmp.value_solded > 0, tmp.value_solded, null)) avg_month_value_last_year,
        AVG(if(tmp.year = {current_year} and tmp.month <= {last_month} and tmp.amount_solded > 0, tmp.amount_solded / 2, null)) avg_month_qtd_current_year,
        AVG(if(tmp.year = {current_year} and tmp.month <= {last_month} and tmp.value_solded > 0, tmp.value_solded, null)) avg_month_value_current_year,
        SUM(IF(tmp.year = {current_year} and tmp.month = {current_month}, tmp.amount_solded / 2, 0)) qtd_current_month,
        SUM(IF(tmp.year = {current_year} and tmp.month = {current_month}, tmp.value_solded, 0)) value_current_month
        FROM (
            SELECT 
            c.wallet wallet,
            c.customer_code customer_code,
            c.customer_name customer_name,
            c.group_customer group_customer,
            MONTH(c.date) month,
            YEAR(c.date) year,
            SUM(c.{column_current_values}_amount) amount_solded,
            SUM(c.{column_current_values}_value) value_solded
            FROM metrics.consolidation c
            WHERE 1 = 1
            AND date BETWEEN '{init_date}' AND '{end_date}'
            AND group_customer = '{group}'
            AND c.product = '' AND c.product_group = ''
            group by 1,2,3,4,5,6
        ) as tmp
        GROUP BY 1,2,3,4;
        """.format(
            current_year=current_year,
            last_year=last_year,
            current_month=current_month,
            last_month=last_month,
            init_date=init_date,
            end_date=end_date,
            group=group,
            column_current_values=column_current_values,
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

        column_current_values = 'sold'
        if params.get('date_type', '') == 'created':
            column_current_values = 'accumulated_sold'

        sql = """
        SELECT 
        c.group_customer group_customer,
        DAY(LAST_DAY(c.date)) last_day_month,
        MONTH(c.date) month,
        YEAR(c.date) year,
        sum(c.{column_current_values}_amount) / 2 month_qtd,
        sum(c.{column_current_values}_value) month_value
        FROM metrics.consolidation c
        WHERE c.group_customer = '{group_customer}'
        AND c.date BETWEEN '{init_date}' AND '{end_date}'
        AND c.product = '' AND c.product_group = ''
        group by group_customer, last_day_month, month, year;
        """.format(
            group_customer=group_customer,
            init_date=init_date,
            end_date=end_date,
            column_current_values=column_current_values,
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

        column_current_values = 'sold'
        if params.get('date_type', '') == 'created':
            column_current_values = 'accumulated_sold'

        sql = """
        SELECT 
        tmp.product,
        tmp.product_group,
        AVG(if(tmp.year = {last_year} and tmp.amount_solded > 0, tmp.amount_solded / 2, null)) avg_month_qtd_last_year,
        AVG(if(tmp.year = {last_year} and tmp.value_solded > 0, tmp.value_solded, null)) avg_month_value_last_year,
        AVG(if(tmp.year = {current_year} and tmp.month <= {last_month} and tmp.amount_solded > 0, tmp.amount_solded / 2, null)) avg_month_qtd_current_year,
        AVG(if(tmp.year = {current_year} and tmp.month <= {last_month} and tmp.value_solded > 0, tmp.value_solded, null)) avg_month_value_current_year,
        SUM(IF(tmp.year = {current_year} and tmp.month = {current_month}, tmp.amount_solded / 2, 0)) qtd_current_month,
        SUM(IF(tmp.year = {current_year} and tmp.month = {current_month}, tmp.value_solded, 0)) value_current_month
        FROM (
            SELECT 
            c.product product,
            c.product_group product_group,
            MONTH(c.date) month,
            YEAR(c.date) year,
            SUM(c.{column_current_values}_amount) amount_solded,
            SUM(c.{column_current_values}_value) value_solded
            FROM metrics.consolidation c
            WHERE c.group_customer = '{group}'
            AND date BETWEEN '{init_date}' AND '{end_date}'
            AND c.product_group != ''
            GROUP BY 1,2,3,4
        ) as tmp
        GROUP BY 1,2
        ORDER BY 
            CASE 
            WHEN tmp.product_group IN ('CRIZAL*', 'TRANSITIONS*') THEN 'WWWW'
            WHEN tmp.product_group like '%%VARILUX%%' THEN 'AAA'
            ELSE tmp.product_group END asc;
        """


        sql_ = sql.format(
            current_year=current_year,
            last_year=last_year,
            current_month=current_month,
            last_month=last_month,
            group=group,
            init_date=init_date,
            end_date=end_date,
            column_current_values=column_current_values,
        )

        result = con.execute(sql_)

    return jsonify(consolidate_result(result))