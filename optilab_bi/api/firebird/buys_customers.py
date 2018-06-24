from flask import Blueprint, jsonify, request
from optilab_bi import connection
from optilab_bi.api.firebird.sqls.buys_customer import eval_months_buys, \
active_current_previous_month, active_latest_year, active_today_yesterday
from optilab_bi.api.mysql import configuration

actions = Blueprint('/customers', __name__, url_prefix='/customers')

def build_result(brute_list):
    copy_list = [item for item in brute_list]

    result = []

    for item in brute_list:
        item_result = {
            'cli_codigo': item['cli_codigo'],
            'cli_nome_fan': item['cli_nome_fan'],
            'emp_code': item['emp_code'],
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
                aux['emp_code'] == item['emp_code'] and aux['type'] == 'latest':
                    item_result['latest_value'] = aux['value']
                    
            else:
                if aux['cli_codigo'] == item['cli_codigo'] and \
                aux['emp_code'] == item['emp_code'] and aux['type'] == 'current':
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
    
    response = {}
    for emp_code in business_codes:
        response[str(emp_code)] = {
            'current_day': next((obj['qtd'] for obj in result['current_day'] if obj['emp_code'] == emp_code), None),
            'latest_day': next((obj['qtd'] for obj in result['latest_day'] if obj['emp_code'] == emp_code), None),
            'current_month': next((obj['qtd'] for obj in result['current_month'] if obj['emp_code'] == emp_code), None),
            'latest_month': next((obj['qtd'] for obj in result['latest_month'] if obj['emp_code'] == emp_code), None),
            'average_latest_year': next((obj['average'] for obj in result['average_latest_year'] if obj['emp_code'] == emp_code), None)
        }

    return response
        


@actions.route('/_eval', methods=['POST'])
def _eval():
    session = connection.cursor()
    sql = eval_months_buys()

    args = request.get_json()

    list_cfop = configuration.get_config('cfop_vendas')

    current_month = args.get('month')
    current_year = args.get('year')
    
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
        rate['emp_code'] = row[5]
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

    return jsonify(response)


@actions.route('/_amount', methods=['POST'])
def _amount():
    session = connection.cursor()

    sql_month = active_current_previous_month()
    sql_day = active_today_yesterday()
    sql_latest_year = active_latest_year()

    args = request.get_json()

    list_cfop = configuration.get_config('cfop_vendas')

    current_year = args.get('year')
    latest_year = str(int(current_year) - 1)
    current_month = args.get('month')
    latest_month = str(int(current_month) - 1)
    # TODO melhorar logica para pega o latest day como latest util day
    current_day = args.get('day')
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

    result = calc_amonts(result_day, result_month, result_latest_year, filters)

    return jsonify(result)
    
