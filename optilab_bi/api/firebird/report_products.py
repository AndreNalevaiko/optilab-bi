from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, Response, send_file
from flask_cors import cross_origin
import pandas
import io, copy

from optilab_bi import connection, db
from optilab_bi.model.product import ReportProducts
from optilab_bi.api.mysql import configuration, product as product_api
from optilab_bi.api.firebird.sqls.products import sql_all_products_pt_1, sql_all_products_pt_2,  sql_all_products_pt_3
from optilab_bi.api.firebird.util import resolve_abstract_inconsistency
from optilab_bi.helpers import to_dict

actions = Blueprint('report_products', __name__,
                    url_prefix='/report_products')


def append_in_list_global(global_list, original_product):
    product = copy.deepcopy(original_product)
    index = None
    for idx, prod in enumerate(global_list):
        if prod['brand'] == product['brand'] and prod['label'] == product['label'] \
            and prod['month'] == product['month'] and prod['year'] == product['year']:
            index = idx
    
    if index:
        global_list[index]['amount'] += product['amount']
        global_list[index]['value'] += product['value']
    else:
        product['business_code'] = 0
        global_list.append(product)

    return global_list

def return_latest(list_products, brand, label, business_code, year):
    result = [record for record in list_products if record['year'] == year and 
        record['brand'] == brand and record['label'] == label and record['business_code'] == business_code]
    if len(result):
        result = result[0]
    else:
        result = {'amount': 0,'value': 0}
    return result


@actions.route('/_generate', methods=['POST'])
@cross_origin()
def report_products():
    session = connection.cursor()

    query = ''

    args = request.get_json()
    
    if args:
        period = args.get('period')

        month = period['month']
        years = period['years']

    else:
        date_now = datetime.now() - timedelta(days=1)

        month = str(date_now.month)
        years = '{},{}'.format(str(date_now.year), str(date_now.year - 1))

    list_cfop = configuration.get_config('cfop_vendas')

    sql_pt_1 = sql_all_products_pt_1()
    sql_pt_1 = sql_pt_1.format(list_cfop=list_cfop, month=month, years=years)
    sql_pt_1 = sql_pt_1.replace('\n', ' ')

    session.execute(sql_pt_1)
    result_pt_1 = session.fetchall()

    sql_pt_2 = sql_all_products_pt_2()
    sql_pt_2 = sql_pt_2.format(list_cfop=list_cfop, month=month, years=years)
    sql_pt_2 = sql_pt_2.replace('\n', ' ')

    session.execute(sql_pt_2)
    result_pt_2 = session.fetchall()

    sql_pt_3 = sql_all_products_pt_3()
    sql_pt_3 = sql_pt_3.format(list_cfop=list_cfop, month=month, years=years)
    sql_pt_3 = sql_pt_3.replace('\n', ' ')

    session.execute(sql_pt_3)
    result_pt_3 = session.fetchall()
    
    results = result_pt_1 + result_pt_2 + result_pt_3

    list_products = []

    list_products_global = []
    
    for column in results:
        product = {}
        product['brand'] = column[0].replace(' ', '')
        product['label'] = column[1].replace(' ', '').replace('_', ' ')
        product['amount'] = int(column[2])
        product['value'] = column[3]
        product['business_code'] = column[4]
        product['year'] = int(column[5])
        product['month'] = int(column[6])

        list_products.append(product)
        list_products_global = append_in_list_global(list_products_global, product)

    # Concatena o array com as empresas e o global
    list_products = list_products + list_products_global

    years_report = [int(y) for y in years.split(',')]
    latest_year = min(years_report)
    current_year = max(years_report)

    list_current = [item for item in list_products if item['year'] == current_year]


    for record in list_current:
        select = "SELECT * FROM report_products where brand = '{}' and label = '{}' and business_code = {} and month = {} and year = {}".format(
            record['brand'],record['label'],record['business_code'],record['month'],current_year
        )
        try:
            report_products = ReportProducts.query.filter(
                ReportProducts.brand == record['brand'],
                ReportProducts.label == record['label'],
                ReportProducts.business_code == record['business_code'],
                ReportProducts.month == record['month'],
                ReportProducts.current_year == current_year
            ).one_or_none()

        except Exception:
            print("Registro duplicado para ({})".format(select))
            # Deleta o registro duplicado
            report_product_duplicated = ReportProducts.query.filter(
                ReportProducts.brand == record['brand'],
                ReportProducts.label == record['label'],
                ReportProducts.business_code == record['business_code'],
                ReportProducts.month == record['month'],
                ReportProducts.current_year == current_year
            ).first()

            db.session.delete(report_product_duplicated)

            report_products = ReportProducts.query.filter(
                ReportProducts.brand == record['brand'],
                ReportProducts.label == record['label'],
                ReportProducts.business_code == record['business_code'],
                ReportProducts.month == record['month'],
                ReportProducts.current_year == current_year
            ).one_or_none()

        if not report_products:
            report_products = ReportProducts()

            report_products.brand = record['brand']
            report_products.label = record['label']
            report_products.business_code = record['business_code']
            report_products.status = 'OPENED'
            report_products.current_year = current_year
            report_products.latest_year = latest_year
            report_products.month = record['month']

        report_products.qtd_current_year = record['amount']
        report_products.value_current_year = record['value']

        latest = return_latest(list_products, record['brand'], record['label'], record['business_code'], latest_year) 
        report_products.qtd_latest_year = latest['amount']
        report_products.value_latest_year = latest['value']

        db.session.add(report_products)

    db.session.commit()

    results = ReportProducts.query.filter(
        ReportProducts.current_year == current_year,
        ReportProducts.month == month
    ).all()

    results = [to_dict(report) for report in results]

    return jsonify(results)

@actions.route('/_export_xlsx', methods=['GET'])
@cross_origin()
def export_xlsx():
    current_year = request.args.get('year')
    month = request.args.get('month')
    emp_code = request.args.get('emp_code')

    if not current_year or not month or not emp_code:
        return 'bad request', 400

    result = ReportProducts.query.filter(
        ReportProducts.current_year == current_year,
        ReportProducts.month == month,
        ReportProducts.business_code == emp_code
    ).all()

    data = {
        'marca': [],
        'lente': [],
        'empresa': [],
        'mes': [],
        'ano_atual': [],
        'ano_anterior': [],
        'qtd_ano_atual': [],
        'valor_ano_atual': [],
        'qtd_ano_anterior': [],
        'valor_ano_anterior': []
    }

    for report in result:
        data['marca'].append(report.brand)
        data['lente'].append(report.label)
        data['empresa'].append(report.business_code)
        data['mes'].append(report.month)
        data['ano_atual'].append(report.current_year)
        data['ano_anterior'].append(report.latest_year)
        data['qtd_ano_atual'].append(report.qtd_current_year)
        data['valor_ano_atual'].append(report.value_current_year)
        data['qtd_ano_anterior'].append(report.qtd_latest_year)
        data['valor_ano_anterior'].append(report.value_latest_year)

    data_frame = pandas.DataFrame(data=data)

    output = io.BytesIO()

    writer = pandas.ExcelWriter(output, engine='xlsxwriter')

    data_frame.to_excel(writer, sheet_name='Planilha1')

    writer.save()

    xlsx_data = output.getvalue()

    filename = 'report_products_{}_{}.xlsx'.format(month, current_year)

    return send_file(io.BytesIO(xlsx_data), as_attachment=True, attachment_filename=filename)
