from flask import Blueprint, jsonify, request
from optilab_bi import connection
from optilab_bi.api.firebird.sqls.buys_customer import eval_months_buys
from optilab_bi.api.mysql import configuration

actions = Blueprint('/customers', __name__, url_prefix='/customers')

def build_result(brute_list):
    copy_list = [item for item in brute_list]

    result = []
    print('teste')

    for item in brute_list:
        item_result = {
            'cli_codigo': item['cli_codigo'],
            'cli_nome_fan': item['cli_nome_fan'],
            'latest_value': None,
            'current_value': None,
        }
        import ipdb; ipdb.set_trace()
        if item['type'] == 'current':
            item_result['current_value'] = item['value']
        else:
            item_result['latest_value'] = item['value']

        for aux in copy_list:
            if item['type'] == 'current':
                if aux['cli_codigo'] == item['cli_codigo'] and \
                aux['emp_code'] == item['emp_code'] and aux['type'] == 'latest':
                    import ipdb; ipdb.set_trace()
                    item_result['latest_value'] = aux['value']
                    
            else:
                if aux['cli_codigo'] == item['cli_codigo'] and \
                aux['emp_code'] == item['emp_code'] and aux['type'] == 'current':
                    import ipdb; ipdb.set_trace()
                    item_result['current_value'] = aux['value']
        
        result.append(item_result)

    import ipdb; ipdb.set_trace()

    result_teste = []
    for r in result:
        if r not in result_teste:
            result_teste.append(r)

    import ipdb; ipdb.set_trace()

    return result

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
        rate['type'] = 'current ' if row[4] == current_year and row[3] == current_month else 'latest' 

        result_list.append(rate)

    teste = build_result(result_list)

    list_current = [item for item in result_list if item['year'] == current_year and item['month'] == current_year]

    if int(current_month) == 1:
        list_latest = [item for item in result_list if item['year'] == str(int(current_year - 1)) and item['month'] == latest_month]
    else:
        list_latest = [item for item in result_list if item['year'] == current_year and item['month'] == latest_month]

    

    return jsonify(result_list)