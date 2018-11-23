from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from optilab_bi import connection, db
from optilab_bi.api.firebird.sqls.buys_customer import eval_months_buys, \
active_current_previous_month, active_latest_year, active_today_yesterday, \
active_today
from optilab_bi.api.mysql import configuration
from optilab_bi.model import NumberActiveCustomers, CustomerBillingReport

actions = Blueprint('/customers', __name__, url_prefix='/customers')

def build_result(brute_list):
    copy_list = [item for item in brute_list]

    result = []

    for item in brute_list:
        item_result = {
            'cli_codigo': item['cli_codigo'],
            'cli_nome_fan': item['cli_nome_fan'],
            'business_code': item['business_code'],
            'latest_value': None,
            'current_value': None,
        }
        if item['type'] == 'current':
            item_result['current_value'] = item['value']
        else:
            item_result['latest_value'] = item['value']

        for aux in copy_list:
            if item['type'] == 'current':
                if aux['cli_codigo'] == item['cli_codigo'] and \
                aux['business_code'] == item['business_code'] and aux['type'] == 'latest':
                    item_result['latest_value'] = aux['value']
                    
            else:
                if aux['cli_codigo'] == item['cli_codigo'] and \
                aux['business_code'] == item['business_code'] and aux['type'] == 'current':
                    item_result['current_value'] = aux['value']
        
        result.append(item_result)

    result_final = []
    for r in result:
        if r not in result_final:
            result_final.append(r)


    return result_final

def calc_amonts(result_day, result_month, result_lates_year, filters):
    business_codes = []

    result = {
        'current_day': [],
        'latest_day': [],
        'current_month': [],
        'latest_month': [],
        'average_latest_year': []
    }

    for row in result_day:
        obj = {'qtd': row[0], 'emp_code': row[1]}
        if row[2] == int(filters['current_day']):
            result['current_day'].append(obj)
        else:
            result['latest_day'].append(obj)

        if obj['emp_code'] not in business_codes:
            business_codes.append(obj['emp_code'])
            
    for row in result_month:
        obj = {'qtd': row[0], 'emp_code': row[1]}
        if row[2] == int(filters['current_month']):
            result['current_month'].append(obj)
        else:
            result['latest_month'].append(obj)

        if obj['emp_code'] not in business_codes:
            business_codes.append(obj['emp_code'])

    emp_codes = list(set([r[1] for r in result_lates_year]))
    
    for emp_code in emp_codes:
        list_emp = [r[0] for r in result_lates_year if r[1] == emp_code]
        average = sum(list_emp)/len(list_emp)

        obj = {'average': average, 'emp_code': emp_code}
        result['average_latest_year'].append(obj)

        if emp_code not in business_codes:
            business_codes.append(emp_code)
    
    response = []

    for emp_code in business_codes:
        response.append({
            'current_day': next((obj['qtd'] for obj in result['current_day'] if obj['emp_code'] == emp_code), None),
            'latest_day': next((obj['qtd'] for obj in result['latest_day'] if obj['emp_code'] == emp_code), None),
            'current_month': next((obj['qtd'] for obj in result['current_month'] if obj['emp_code'] == emp_code), None),
            'latest_month': next((obj['qtd'] for obj in result['latest_month'] if obj['emp_code'] == emp_code), None),
            'average_latest_year': next((obj['average'] for obj in result['average_latest_year'] if obj['emp_code'] == emp_code), None),
            'business_code': int(emp_code)
        })

    return response
        

def _eval(date):
    session = connection.cursor()
    sql = eval_months_buys()

    list_cfop = configuration.get_config('cfop_vendas')

    current_month = date.get('month')
    current_year = date.get('year')
    
    if int(current_month) == 1:
        latest_month = '12'
        years = current_year + ', {}'.format(int(current_year) - 1)
    else:
        latest_month = str(int(current_month) - 1)
        years = current_year

    sql = sql.format(list_cfop=list_cfop, current_month=current_month, 
                                latest_month=latest_month, years=years)

    session.execute(sql)
    
    results = session.fetchall()
    result_list = []
    for row in results:
        rate = {}

        rate['cli_codigo'] = row[0]
        rate['cli_nome_fan'] = row[1]
        rate['value'] = row[2]
        rate['month'] = row[3]
        rate['year'] = row[4]
        rate['business_code'] = row[5]
        rate['type'] = 'current' if row[4] == int(current_year) and row[3] == int(current_month) else 'latest' 

        result_list.append(rate)
    
    response = build_result(result_list)
    
    for item in response:
        if not item['current_value']:
            item['variation'] = 0
            item['current_value'] = 0        
        elif not item['latest_value']:
            item['variation'] = 0
            item['latest_value'] = 0                    
        else:
            item['variation'] = (item['current_value'] / item['latest_value']) - 1

        customer_billing_report = CustomerBillingReport.query.filter(
            CustomerBillingReport.business_code == item['business_code'],
            CustomerBillingReport.customer_code == item['cli_codigo'],
            CustomerBillingReport.customer_name == item['cli_nome_fan'],
            CustomerBillingReport.month == int(current_month),
            CustomerBillingReport.year == int(current_year)
        ).one_or_none()

        if not customer_billing_report:

            customer_billing_report = CustomerBillingReport()
            customer_billing_report.business_code = item['business_code']
            customer_billing_report.customer_code = item['cli_codigo']
            customer_billing_report.customer_name = item['cli_nome_fan']
            customer_billing_report.month = int(current_month)
            customer_billing_report.year = int(current_year)

        customer_billing_report.current_value = item['current_value']
        customer_billing_report.latest_value = item['latest_value']
        customer_billing_report.variation = item['variation']

        db.session.add(customer_billing_report)
    
    db.session.commit()

    return jsonify(response)


def _amount(date):
    session = connection.cursor()

    sql_month = active_current_previous_month()
    sql_day = active_today_yesterday()
    sql_latest_year = active_latest_year()

    list_cfop = configuration.get_config('cfop_vendas')

    current_year = date.get('year')
    latest_year = str(int(current_year) - 1)
    current_month = date.get('month')
    latest_month = str(int(current_month) - 1)
    current_day = date.get('day')
    # TODO melhorar logica para pega o latest day como latest util day
    latest_day = str(int(current_day) - 1)

    sql_month = sql_month.format(list_cfop=list_cfop, current_year=current_year,\
                            current_month=current_month, latest_month=latest_month)

    sql_day = sql_day.format(list_cfop=list_cfop, current_day=current_day, latest_day=latest_day, \
                            current_month=current_month, current_year=current_year)

    sql_latest_year = sql_latest_year.format(list_cfop=list_cfop, latest_year=latest_year)

    session.execute(sql_month)
    result_month = session.fetchall()

    session.execute(sql_day)
    result_day = session.fetchall()

    session.execute(sql_latest_year)
    result_latest_year = session.fetchall()

    filters = {
        'current_year': current_year,
        'latest_year': latest_year,
        'current_month': current_month,
        'latest_month': latest_month,
        'current_day': current_day,
        'latest_day': latest_day,
    }

    amounts = calc_amonts(result_day, result_month, result_latest_year, filters)

    date_record = datetime.now().replace(
        day=int(current_day),
        month=int(current_month),
        year=int(current_year)
    ).date()
    
    for amount in amounts:

        number_active_customers = NumberActiveCustomers.query.filter(
            NumberActiveCustomers.business_code == amount['business_code'],
            NumberActiveCustomers.date == date_record,
        ).one_or_none()

        if not number_active_customers:
            number_active_customers = NumberActiveCustomers()
            number_active_customers.business_code = amount['business_code']
            number_active_customers.date = date_record
        
        number_active_customers.number_current_day = amount.get('current_day') or 0
        number_active_customers.number_latest_day = amount.get('latest_day') or 0
        number_active_customers.number_current_month = amount.get('current_month') or 0
        number_active_customers.number_latest_month = amount.get('latest_month') or 0
        number_active_customers.average_latest_year = amount.get('average_latest_year') or 0

        db.session.add(number_active_customers)

    db.session.commit()


def generate_current_day_amount(date):
    session = connection.cursor()

    sql_day = active_today()

    list_cfop = configuration.get_config('cfop_vendas')

    current_year = date.get('year')
    current_month = date.get('month')
    current_day = date.get('day')

    sql_day = sql_day.format(list_cfop=list_cfop, current_day=current_day, \
                            current_month=current_month, current_year=current_year)

    session.execute(sql_day)
    result_day = session.fetchall()

    result = []

    for row in result_day:
        obj = {
            'qtd': row[0], 
            'business_code': row[1],
        }

        result.append(obj)

    date_record = datetime.now().replace(
        day=int(current_day),
        month=int(current_month),
        year=int(current_year)
    ).date()

    for item in result:
        number_active_customers = NumberActiveCustomers.query.filter(
            NumberActiveCustomers.business_code == item['business_code'],
            NumberActiveCustomers.date == date_record,
        ).one_or_none()

        if number_active_customers:
            number_active_customers.number_current_day = item.get('qtd') or 0

            db.session.add(number_active_customers)

    db.session.commit()    
    
@actions.route('/_generate', methods=['POST'])
def _generate():
    date = request.get_json()

    if not date:
        date_now = datetime.now() - timedelta(days=1)
        date = {
            'year': date_now.year,
            'month': date_now.month,
            'day': date_now.day,
        }

    _amount(date)
    _eval(date)

    return 'OK', 200