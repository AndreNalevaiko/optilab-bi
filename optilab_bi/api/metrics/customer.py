import decimal
from datetime import date, datetime, timedelta

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
                # obj[key] = str(row[key])
                obj[key] = row[key]
            elif isinstance(row[key], date) or isinstance(row[key], datetime):
                obj[key] = str(row[key])
            else:
                obj[key] = row[key]
        
        return_.append(obj)

    return return_

@actions.route('/search', methods=['GET'])
@user_manager.auth_required('user')
def search(auth_data=None):
    params = request.args.to_dict()

    with db_metrics.connect() as con:

        clauses_search = []

        if params.get('customer_code'):
            clauses_search.append(" AND c.customer_code like '{}'".format(params.get('customer_code')))

        if params.get('customer_name'):
            clauses_search.append(" AND c.customer_name like '%%{}%%'".format(params.get('customer_name')))

        if params.get('group_customer'):
            clauses_search.append(" AND c.group_customer like '%%{}%%'".format(params.get('group_customer')))

        sql = """
        SELECT c.wallet wallet, c.customer_code customer_code,c.customer_name customer_name,c.group_customer group_customer
        FROM metrics.consolidation c 
        WHERE 1 = 1
        {}
        AND c.product = '' AND c.product_group = '' and customer_name != ''
        group by wallet, customer_code, customer_name, group_customer;
        """.format(' '.join(clauses_search))

        result = con.execute(sql)
        result = consolidate_result(result)

    return jsonify(result)

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

        init_date = date.replace(day=1, month=1, year=last_year).strftime('%Y-%m-%d')
        end_date = date.replace(day=current_day, month=current_month, year=current_year).strftime('%Y-%m-%d')

        column_current_values = 'sold'
        if params.get('date_type', '') == 'created':
            column_current_values = 'accumulated_sold'

        # Usado para buscar quando é um cliente especifico
        custom_where = ''
        if params.get('customer_code'):
            custom_where = " AND c.customer_code = '%s'" % params.get('customer_code')

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
            {custom_where}
            AND c.product = '' AND c.product_group = '' and customer_name != ''
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
            custom_where=custom_where,
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
        customer_code = params.get('customer_code')
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
        c.customer_code customer_code,
        c.customer_name customer_name,
        c.group_customer group_customer,
        c.wallet wallet,
        DAY(LAST_DAY(c.date)) last_day_month,
        MONTH(c.date) month,
        YEAR(c.date) year,
        sum(c.sold_amount) / 2 month_qtd,
        sum(c.sold_value) month_value
        FROM metrics.consolidation c
        WHERE c.customer_code = '{customer_code}'
        AND c.date BETWEEN '{init_date}' AND '{end_date}'
        AND c.product = '' AND c.product_group = ''
        group by customer_code, customer_name, group_customer, wallet, last_day_month, month, year;
        """.format(
            customer_code=customer_code,
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
        customer_code = params.get('customer_code')
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
            WHERE c.customer_code = '{customer_code}'
            AND date BETWEEN '{init_date}' AND '{end_date}'
            AND c.product_group != ''
            group by 1,2,3,4
        ) as tmp
        GROUP BY 1,2
        ORDER BY 
            CASE 
            WHEN tmp.product_group IN ('CRIZAL*', 'TRANSITIONS*') THEN 'WWWW'
            WHEN tmp.product_group like '%%VARILUX%%' THEN 'AAA'
            ELSE tmp.product_group END asc;
        """


        # for column in metrics_columns:
        sql_ = sql.format(
            current_year=current_year,
            last_year=last_year,
            current_month=current_month,
            last_month=last_month,
            current_day=current_day,
            customer_code=customer_code,
            init_date=init_date,
            end_date=end_date,
            column_current_values=column_current_values,
        )

        result = con.execute(sql_)

    return jsonify(consolidate_result(result))


@actions.route('/products_all_year', methods=['POST'])
@user_manager.auth_required('user')
def products_all_year(auth_data=None):
    params = request.get_json()

    with db_metrics.connect() as con:
        date = params.get('date')
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Params Query
        init_date = date.replace(day=1, year=date.year-1)
        init_date = init_date.strftime('%Y-%m-%d')
        end_date = date.strftime('%Y-%m-%d')
        customer_code = params.get('customer_code')
        type_ = params.get('type')

        columns_values = 'sum(c.sold_amount) qtd, sum(c.sold_value) value'
        if params.get('date_type', '') == 'created':
            columns_values = """if(year(date) = year('{end_date}') and month(date) = month('{end_date}'), 
            sum(c.accumulated_sold_amount), sum(c.sold_amount)) qtd,
            if(year(date) = year('{end_date}') and month(date) = month('{end_date}'), 
            sum(c.accumulated_sold_value), sum(c.sold_value)) value""".format(end_date=end_date)
        
        if type_:
            sql = """
            SELECT tp.product name, tp.ld dt, sum(tp.value) value, sum(tp.qtd) / 2 qtd FROM (
                select c.product, date dt, LAST_DAY(date) ld, {columns_values}
                from consolidation c
                where c.product_group = '{type_}' and product != ''
                and c.customer_code = {customer_code} and date BETWEEN '{init_date}' AND '{end_date}'
                GROUP BY dt, ld, product
            ) as tp
            GROUP BY 1,2;
            """.format(type_=type_, customer_code=customer_code, init_date=init_date, end_date=end_date, columns_values=columns_values)
        else:
            sql = """
            SELECT tp.product_group name, tp.ld dt, sum(tp.value) value, sum(tp.qtd) / 2 qtd FROM (
                select c.product_group, date dt, LAST_DAY(date) ld, {columns_values}
                from consolidation c
                where c.product_group != '' and c.product = ''
                and c.customer_code = {customer_code} and date BETWEEN '{init_date}' AND '{end_date}'
                GROUP BY dt, ld, product_group
            ) as tp
            GROUP BY 1,2
            order by dt asc;
            """.format(customer_code=customer_code, init_date=init_date, end_date=end_date, columns_values=columns_values)

        result = consolidate_result(con.execute(sql))

        response = []

        # Gera um consolidado para facilitar no frontend
        for item in result:
            date_finded = False
            
            for p in response:
                if item['dt'] == p['data']:
                    date_finded = True
                    p['products'].append({'name': item['name'], 'value': item['value'], 'qtd': item['qtd']})
                
            if not date_finded:
                response.append(
                    {
                        'data': item['dt'], 
                        'products': [{'name': item['name'], 'value': item['value'], 'qtd': item['qtd']}]
                    }
                )
        products = []
        products_names = []

        for prod in result:
            # if prod['name'] not in products_names:
            if prod['name'] not in products_names and prod['value'] and prod['qtd']:
                products_names.append(prod['name'])

        for item in response:
            item_data = {'data': item['data']}

            for prod in item['products']:
                if prod['name'] in products_names:
                    number = products_names.index(prod['name']) + 1
                    item_data['product_{number}_name'.format(number=number)] = prod['name']
                    item_data['product_{number}_value'.format(number=number)] = prod['value']
                    item_data['product_{number}_qtd'.format(number=number)] = prod['qtd']
            
            item_data['total_value'] = sum([p['value'] for p in item['products'] if p['value']])
            item_data['total_qtd'] =  sum([p['qtd'] for p in item['products'] if p['qtd']])
            products.append(item_data)


    return jsonify({'products': products, 'products_names': products_names})