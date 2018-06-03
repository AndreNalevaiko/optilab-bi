from datetime import datetime
from flask import Blueprint, jsonify, request, Response, send_file
from flask_cors import cross_origin
import pandas
import io

from optilab_bi import connection, db
from optilab_bi.model.product import ReportProducts
from optilab_bi.api.mysql import configuration, product as product_api
from optilab_bi.api.firebird.sqls.products import sql_all_products
from optilab_bi.api.firebird.util import resolve_abstract_inconsistency
from optilab_bi.helpers import to_dict

actions = Blueprint('report_products', __name__,
                    url_prefix='/report_products')


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
    
    period = args.get('period')
    brands = args.get('brands')

    month = period['month']
    years = period['years']
    is_new_month = datetime.now().day == 1

    list_cfop = configuration.get_config('cfop_vendas')

    sql = sql_all_products()

    sql = sql.format(list_cfop=list_cfop, month=month, years=years)

    sql = sql.replace('\n', ' ')

    session.execute(sql)

    results = session.fetchall()

    list_products = []
    
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

    years_report = [int(y) for y in years.split(',')]
    latest_year = min(years_report)
    current_year = max(years_report)

    list_current = [item for item in list_products if item['year'] == current_year]


    for record in list_current:
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

@actions.route('/_export_csv', methods=['POST'])
@cross_origin()
def export_csv():
    args = request.get_json()

    current_year = args.get('current_year')
    month = args.get('month')
    # current_year = '2018'
    # month = '02'

    result = ReportProducts.query.filter(
        ReportProducts.current_year == current_year,
        ReportProducts.month == month
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

    data_frame.to_excel(writer, sheet_name='ReportProducts')

    writer.save()

    xlsx_data = output.getvalue()

    return send_file(io.BytesIO(xlsx_data),as_attachment=True, attachment_filename='report.xlsx')
