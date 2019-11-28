from datetime import datetime, timedelta
from calendar import monthrange

from flask import Blueprint, jsonify, request
from optilab_bi import  get_connection, db
from optilab_bi.api.firebird.sqls.buys_customer import eval_months_buys, \
active_current_previous_month, active_latest_year, active_today_yesterday, \
active_today
from optilab_bi.api.mysql import configuration
from optilab_bi.model import NumberActiveCustomers, CustomerBillingReport
from optilab_bi.api.firebird.util import get_same_period_date

actions = Blueprint('/customers', __name__, url_prefix='/customers')

def build_result(brute_list):
    copy_list = [item for item in brute_list]

    result = []
    for item in brute_list:
        item_result = {
            'cli_codigo': item['cli_codigo'],
            'cli_nome_fan': item['cli_nome_fan'],
            'seller': item['seller'],
            'latest_value': None,
            'current_value': None,
            'date': item['date'],
        }

        if item['type'] == 'current':
            item_result['current_value'] = float(str(item['value']))
        else:
            item_result['latest_value'] = float(str(item['value']))

        for aux in copy_list:
            if item['type'] == 'current':
                if aux['cli_codigo'] == item['cli_codigo'] and \
                aux['seller'] == item['seller'] and aux['type'] == 'latest_':
                    item_result['latest_value'] = float(str(aux['value']))
                    
            else:
                if aux['cli_codigo'] == item['cli_codigo'] and \
                aux['seller'] == item['seller'] and aux['type'] == 'current':
                    item_result['current_value'] = float(str(aux['value']))
        
        result.append(item_result)

    result_final = []
    for r in result:
        if r not in result_final:
            result_final.append(r)


    return result_final

def calc_amonts(result_day, result_month, result_lates_year, filters):
    sellers_codes = []

    result = {
        'current_day': [],
        'latest_day': [],
        'current_month': [],
        'latest_month': [],
        'average_latest_year': []
    }

    for row in result_day:
        obj = {'qtd': row[0], 'seller': row[1]}
        if row[2] == int(filters['current_day']):
            result['current_day'].append(obj)
        else:
            result['latest_day'].append(obj)

        if obj['seller'] not in sellers_codes:
            sellers_codes.append(obj['seller'])
            
    for row in result_month:
        obj = {'qtd': row[0], 'seller': row[1]}
        if row[2] == int(filters['current_month']):
            result['current_month'].append(obj)
        else:
            result['latest_month'].append(obj)

        if obj['seller'] not in sellers_codes:
            sellers_codes.append(obj['seller'])

    sellers = list(set([r[1] for r in result_lates_year]))
    
    for seller in sellers:
        list_emp = [r[0] for r in result_lates_year if r[1] == seller]
        average = sum(list_emp)/len(list_emp)

        obj = {'average': average, 'seller': seller}
        result['average_latest_year'].append(obj)

        if seller not in sellers_codes:
            sellers_codes.append(seller)
    
    response = []

    for seller in sellers_codes:
        response.append({
            'current_day': next((obj['qtd'] for obj in result['current_day'] if obj['seller'] == seller), None),
            'latest_day': next((obj['qtd'] for obj in result['latest_day'] if obj['seller'] == seller), None),
            'current_month': next((obj['qtd'] for obj in result['current_month'] if obj['seller'] == seller), None),
            'latest_month': next((obj['qtd'] for obj in result['latest_month'] if obj['seller'] == seller), None),
            'average_latest_year': next((obj['average'] for obj in result['average_latest_year'] if obj['seller'] == seller), None),
            'seller': int(seller)
        })

    return response
        

def _eval(date):
    connection = get_connection()
    session = connection.cursor()

    sql = eval_months_buys()

    current_month = date.month
    current_year = date.year
    
    date_filter = get_same_period_date(date)

    # sellers = configuration.get_config('sellers')
    sellers = '319,320,321,322,318,323'

    # Ajuste para consolidação do global 
    sql_sellers = sql.format(
        date_ini_current=date_filter['current']['date_ini'],
        date_fim_current=date_filter['current']['date_fim'],
        date_ini_latest=date_filter['latest']['date_ini'],
        date_fim_latest=date_filter['latest']['date_fim'],
        seller_column='tmp.seller', sellers='and cl.funcodigo in ({})'.format(sellers))
    sql_global = sql.format(
        date_ini_current=date_filter['current']['date_ini'],
        date_fim_current=date_filter['current']['date_fim'],
        date_ini_latest=date_filter['latest']['date_ini'],
        date_fim_latest=date_filter['latest']['date_fim'],
        seller_column='0', sellers='')

    session.execute(sql_sellers)
    results = session.fetchall()
    
    session.execute(sql_global)
    results = results + session.fetchall()

    result_list = []

    for row in results:
        rate = {}

        rate['cli_codigo'] = row[0]
        rate['cli_nome_fan'] = row[1]
        rate['value'] = row[7]
        rate['month'] = row[9]
        rate['year'] = row[10]
        rate['seller'] = row[11]
        rate['type'] = row[12]
        rate['date'] = date.date()

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
            CustomerBillingReport.seller == item['seller'],
            CustomerBillingReport.customer_code == item['cli_codigo'],
            CustomerBillingReport.customer_name == item['cli_nome_fan'],
            CustomerBillingReport.date == item['date'],
            CustomerBillingReport.month == int(current_month),
            CustomerBillingReport.year == int(current_year)
        ).one_or_none()

        if not customer_billing_report:

            customer_billing_report = CustomerBillingReport()
            customer_billing_report.seller = item['seller']
            customer_billing_report.customer_code = item['cli_codigo']
            customer_billing_report.customer_name = item['cli_nome_fan']
            customer_billing_report.date = item['date']
            customer_billing_report.month = int(current_month)
            customer_billing_report.year = int(current_year)

        customer_billing_report.current_value = item['current_value']
        customer_billing_report.latest_value = item['latest_value']
        customer_billing_report.variation = item['variation']

        db.session.add(customer_billing_report)
    
    db.session.commit()

    connection.close()

    return jsonify(response)


def _amount(date):
    connection = get_connection()
    session = connection.cursor()

    sql_month = active_current_previous_month()
    sql_day = active_today_yesterday()
    sql_latest_year = active_latest_year()

    list_cfop = configuration.get_config('cfop_vendas')
    # cutting_average = configuration.get_config('cutting_average')
    # sellers = configuration.get_config('sellers')
    sellers = '319,320,321,322,318,323'
    cutting_average = 1000

    current_year = date.get('year')
    latest_year = str(int(current_year) - 1)
    current_month = date.get('month')
    latest_month = str(int(current_month) - 1)
    current_day = date.get('day')
    # TODO melhorar logica para pega o latest day como latest util day
    latest_day = str(int(current_day) - 1)

    if latest_month == '0':
        latest_month = '12'

    if latest_day == '0':
        if latest_month == '12':
            latest_day = str(monthrange(int(latest_year),12)[1])
        else:
            latest_day = str(monthrange(int(current_year), int(latest_month))[1])


    sql_month_emps = sql_month.format(list_cfop=list_cfop, current_year=current_year,\
                            current_month=current_month, current_day=current_day,\
                            seller_column='tmp.seller', cutting_average=cutting_average,\
                            sellers='and cli.funcodigo in ({})'.format(sellers))

    sql_day_emps = sql_day.format(list_cfop=list_cfop, current_day=current_day, \
                            current_month=current_month, current_year=current_year,\
                            seller_column='tmp.seller', cutting_average=cutting_average,\
                            sellers='and cli.funcodigo in ({})'.format(sellers))

    sql_latest_year_emps = sql_latest_year.format(list_cfop=list_cfop, current_year=current_year,\
                            seller_column='tmp.seller', cutting_average=cutting_average,\
                            sellers='and cli.funcodigo in ({})'.format(sellers))

    sql_month_global = sql_month.format(list_cfop=list_cfop, current_year=current_year,\
                            current_month=current_month, current_day=current_day,\
                            seller_column=0, cutting_average=cutting_average,\
                            sellers='')

    sql_day_global = sql_day.format(list_cfop=list_cfop, current_day=current_day, \
                            current_month=current_month, current_year=current_year,\
                            seller_column=0, cutting_average=cutting_average,\
                            sellers='')

    sql_latest_year_global = sql_latest_year.format(list_cfop=list_cfop, current_year=current_year,\
                            seller_column=0, cutting_average=cutting_average, sellers='')

    session.execute(sql_month_emps)
    result_month = session.fetchall()
    session.execute(sql_month_global)
    result_month = result_month + session.fetchall()

    session.execute(sql_day_emps)
    result_day = session.fetchall()
    session.execute(sql_day_global)
    result_day = result_day + session.fetchall()

    session.execute(sql_latest_year_emps)
    result_latest_year = session.fetchall()
    session.execute(sql_latest_year_global)
    result_latest_year = result_latest_year + session.fetchall()

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
            NumberActiveCustomers.seller == amount['seller'],
            NumberActiveCustomers.date == date_record,
        ).one_or_none()

        if not number_active_customers:
            number_active_customers = NumberActiveCustomers()
            number_active_customers.seller = amount['seller']
            number_active_customers.date = date_record
        
        number_active_customers.number_current_day = amount.get('current_day') or 0
        number_active_customers.number_latest_day = amount.get('latest_day') or 0
        number_active_customers.number_current_month = amount.get('current_month') or 0
        number_active_customers.number_latest_month = amount.get('latest_month') or 0
        number_active_customers.average_latest_year = amount.get('average_latest_year') or 0

        db.session.add(number_active_customers)

    db.session.commit()

    connection.close()


def generate_current_day_amount(date):
    connection = get_connection()
    session = connection.cursor()

    sql_day = active_today()

    list_cfop = configuration.get_config('cfop_vendas')
    # cutting_average = configuration.get_config('cutting_average')
    # sellers = configuration.get_config('sellers')
    sellers = '319,320,321,322,318,323'
    cutting_average = 1000

    current_year = date.get('year')
    current_month = date.get('month')
    current_day = date.get('day')

    sql_day_emps = sql_day.format(list_cfop=list_cfop, current_day=current_day, \
                            current_month=current_month, current_year=current_year,\
                            seller_column='tmp.seller', cutting_average=cutting_average,\
                            sellers='and cli.funcodigo in ({})'.format(sellers))
    sql_day_global = sql_day.format(list_cfop=list_cfop, current_day=current_day, \
                            current_month=current_month, current_year=current_year,\
                            seller_column=0, cutting_average=cutting_average, sellers='')

    session.execute(sql_day_emps)
    result_day = session.fetchall()
    session.execute(sql_day_global)
    result_day = result_day + session.fetchall()

    result = []

    for row in result_day:
        obj = {
            'qtd': row[0], 
            'seller': row[1],
        }

        result.append(obj)

    date_record = datetime.now().replace(
        day=int(current_day),
        month=int(current_month),
        year=int(current_year)
    ).date()

    for item in result:
        number_active_customers = NumberActiveCustomers.query.filter(
            NumberActiveCustomers.seller == item['seller'],
            NumberActiveCustomers.date == date_record,
        ).one_or_none()

        if number_active_customers:
            number_active_customers.number_current_day = item.get('qtd') or 0

            db.session.add(number_active_customers)

    db.session.commit()   

    connection.close() 
    
@actions.route('/_generate', methods=['POST'])
def _generate():
    data = request.get_json()

    if data:
        date = datetime.strptime(data.get('date'), "%Y-%m-%dT%H:%M:%S.%fZ")

    else:
        date = datetime.now() - timedelta(days=1)

    date_amount = {
        'year': date.year,
        'month': date.month,
        'day': date.day,
    }

    _amount(date_amount)
    # _eval(date)

    return 'OK', 200
    
@actions.route('/<clicodigo>/_info', methods=['GET'])
def _clien_infos(clicodigo):
    tables_query = """
    SELECT tab.tbpcodigo, tab.tbpdescricao FROM clitbp ctp
    join tabpreco tab on ctp.tbpcodigo = tab.tbpcodigo
    join clien cli on cli.clicodigo = ctp.clicodigo
    where tab.tbpsituacao = 'A' AND cli.clicodigo = {clicodigo}
    """.format(clicodigo=clicodigo)

    address_query = """
    SELECT ec.ENDENDERECO || ' ' || ec.ENDNR || ' ' || ec.ENDCEP || ' ' || ci.CIDNOME || ' ' || ci.CIDUF
    FROM clien cli
    join ENDCLI ec on ec.clicodigo = cli.clicodigo
    join CIDADE ci on ci.CIDCODIGO = ec.CIDCODIGO
    where cli.clicodigo = {clicodigo}
    """.format(clicodigo=clicodigo)

    address_query = """
    SELECT ec.ENDTPRUA log, ec.ENDENDERECO endereco, ec.ENDNR numero ,ec.ENDCEP cep ,ci.CIDNOME cidade, ci.CIDUF estado
    FROM clien cli
    join ENDCLI ec on ec.clicodigo = cli.clicodigo
    join CIDADE ci on ci.CIDCODIGO = ec.CIDCODIGO
    where cli.clicodigo = {clicodigo}
    """.format(clicodigo=clicodigo)

    connection = get_connection()
    session = connection.cursor()

    session.execute(tables_query)
    result = session.fetchall()

    tables = [{'tab_codigo': res[0], 'tab_desc': res[1]} for res in result]

    session.execute(address_query)
    address = session.fetchall()[0]
    
    address_view = '%s %s, %s - %s %s-%s' % (address[0], address[1], address[2].replace(' ', ''), address[3], address[4], address[5])
    address_search = '%s %s %s %s %s' % (address[1], address[2].replace(' ', ''), address[3], address[4], address[5])

    return jsonify({'tables': tables, 'address': {'view': address_view, 'search': address_search}}), 200


@actions.route('/_overdue', methods=['POST'])
def _overdue():
    data = request.get_json()

    date = datetime.strptime(data.get('date'), "%Y-%m-%dT%H:%M:%S.%fZ")

    connection = get_connection()
    session = connection.cursor()

    if data.get('type') == 'group':

        sql = """
        SELECT 
        re.clicodigo,
        cli.clinomefant,
        REPLACE(re.RECNRDOC, '.', '') n_doc,
        iif(char_length(re.RECPARCELA) = 4, 
            substring(re.RECPARCELA from 1 for 2) || '/' || substring(re.RECPARCELA from 3 for 2), re.RECPARCELA) parcela,
        sum(re.RecValorAberto) vlr_aberto,
        min(re.recdtvencto) dt_vcto
        FROM receb re
        JOIN clien cli on cli.clicodigo = re.clicodigo
        where re.recdtvencto < '{date}' and re.RecValorAberto >= 0.01
        and cli.clifornec = 'N'
        and re.StCodigo in ( 'N', 'C', 'P', 'A', 'J' ) and ( re.RecSituacao = 'N')
        and cli.gclcodigo = {gclcodigo}
        GROUP BY 1,2,3,4
        """

        sql = sql.format(gclcodigo=data.get('code'), date=date.strftime('%Y-%m-%d'))

        session.execute(sql)
        result = session.fetchall()

        billings_overdued = []
        for bill in result:
            billings_overdued.append({
                'clicodigo': bill[0],
                'customer_name': bill[1],
                'document_number': bill[2],
                'installment': bill[3],
                'value': bill[4],
                'overdue_date': str(bill[5]),
            })

        return jsonify({'billings_overdued': billings_overdued}), 200

    elif data.get('type') == 'customer':
        sql = """
        SELECT REPLACE(re.RECNRDOC, '.', '') n_doc,
        iif(char_length(re.RECPARCELA) = 4, 
            substring(re.RECPARCELA from 1 for 2) || '/' || substring(re.RECPARCELA from 3 for 2), re.RECPARCELA) parcela,
        sum(re.RecValorAberto) vlr_aberto,
        min(re.recdtvencto) dt_vcto
        FROM receb re
        JOIN clien cli on cli.clicodigo = re.clicodigo
        where re.recdtvencto < '{date}' and re.RecValorAberto >= 0.01
        and cli.clifornec = 'N'
        and re.StCodigo in ( 'N', 'C', 'P', 'A', 'J' ) and ( re.RecSituacao = 'N')
        and cli.clicodigo = {clicodigo}
        GROUP BY 1,2
        """

        sql = sql.format(clicodigo=data.get('code'), date=date.strftime('%Y-%m-%d'))

        session.execute(sql)
        result = session.fetchall()

        billings_overdued = []
        for bill in result:
            billings_overdued.append({
                'document_number': bill[0],
                'installment': bill[1],
                'value': bill[2],
                'overdue_date': str(bill[3]),
            })

        return jsonify({'is_overdue': len(result) > 0, 'billings_overdued': billings_overdued}), 200


@actions.route('/_brokes', methods=['POST'])
def _brokes():
    data = request.get_json()

    date = datetime.strptime(data.get('date'), "%Y-%m-%dT%H:%M:%S.%fZ")

    current_year = date.year
    last_year = date.year - 1
    current_month = date.month
    last_month = date.month - 1
    current_day = date.day

    if current_month == 1:
        last_month = current_month

    init_date = date.replace(day=1, month=1, year=last_year).strftime('%Y-%m-%d')
    end_date = date.replace(day=current_day, month=current_month, year=current_year).strftime('%Y-%m-%d')

    connection = get_connection()
    session = connection.cursor()

    sql = """
    SELECT pedper.pedcodigo ped_perda, pedor.pedcodigo ped_origem, pdr.PDPDESCRICAO
    FROM pedid  pedper -- pedido perda
    RIGHT JOIN pedxped pdx on pdx.id_peddes = pedper.id_pedido
    JOIN pedid pedor on pedor.id_pedido = pdx.id_pedori -- pedido origem
    JOIN pdprd pdr on pdr.ID_PEDIDO = pedper.ID_PEDIDO
    join produ pro on pro.PROCODIGO = pdr.PROCODIGO
    where pedper.fiscodigo1 = '5.927' and pedper.peddtemis between '{init_date}' and '{end_date}'
    and pedor.clicodico = {clicodigo} and pro.TPLCODIGO is not null;
    """

    sql = sql.format(clicodigo=data.get('clicodigo'), init_date=init_date, end_date=end_date)

    session.execute(sql)
    result = session.fetchall()

    return jsonify(result), 200