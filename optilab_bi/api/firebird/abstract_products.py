from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from optilab_bi import connection

actions = Blueprint('abstract_products', __name__,
                    url_prefix='/abstract_products')


@actions.route('/', methods=['POST'])
@cross_origin()
def abstract_products():
    session = connection.cursor()

    query = ''
    args = request.get_json()

    products = args.get('products')
    period = args.get('period')
    business_code = args.get('business_code')

    if not products or not period:
        return 'Product or period not found', 404

    date = {
        'start': period['date_start'].split('/'),
        'end': period['date_end'].split('/')
    }

    date_start = '{}/{}/{}'.format(date['start']
                                   [1], date['start'][0], date['start'][2])
    date_end = '{}/{}/{}'.format(date['end']
                                 [1], date['end'][0], date['end'][2])
    month = date['start'][1]

    for product in products:
        sql = """
            select '{}', tpl.tpldescricao ,sum(nfp.nfpqtdade) as qtdade,
            sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
            nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO
            from notas nfs
            left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                                and nfs.empcodigo = nfp.empcodigo
            left join produ    pro on pro.procodigo = nfp.procodigo
            left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
            where  nfs.nfdtemis between '{}' and '{}' and EXTRACT(MONTH FROM nfs.nfdtemis) = {}
            and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
            and nfs.fiscodigo1 in ('5.101','5.102','5.116','6.116','6.101','6.102','5.124','5.112')
        """

        sql = sql.format(product['label'], date_start, date_end, month)

        if business_code:
            sql = sql + ' and nfs.empcodigo = {}'.format(business_code)

        if product.get('process'):
            process = " and (tpl.tplprocesso = '{}')".format(product['process'])
        else:
            process = ''

        descriptions = ''
        for desc in product['descriptions']:
            if descriptions == '':
                descriptions = "TPL.tpldescricao LIKE '%{}%'".format(desc)
            else:
                descriptions = descriptions + \
                    " or TPL.tpldescricao LIKE '%{}%'".format(desc)

        sql = sql + ' and ({})'.format(descriptions)
        sql = sql + process

        sql = sql + ' group by tpl.tpldescricao, nfs.empcodigo, ANO'

        sql = sql.replace('\n', ' ')

        if query == '':
            query = sql
        else:
            query = query + ' UNION ALL ' + sql

    session.execute(query)

    results = session.fetchall()

    if business_code:
        response = []
    else:
        response = {}

    for column in results:
        business = str(column[4])

        product = {}

        product['label'] = column[0]
        product['description'] = column[1]
        product['amount'] = column[2]
        product['value'] = column[3]
        if business_code:
            response.append(product)
        else:
            if response.get(business):
                response[business].append(product)
            else:
                response[business] = [product]

    return jsonify(response)


@actions.route('/brands', methods=['POST'])
@cross_origin()
def abstract_brands():
    session = connection.cursor()

    query = ''
    args = request.get_json()

    products = args.get('products')
    period = args.get('period')
    business_code = args.get('business_code')

    if not products or not period:
        return 'Product or period not found', 404

    date = {
        'start': period['date_start'].split('/'),
        'end': period['date_end'].split('/')
    }

    date_start = '{}/{}/{}'.format(date['start']
                                   [1], date['start'][0], date['start'][2])
    date_end = '{}/{}/{}'.format(date['end']
                                 [1], date['end'][0], date['end'][2])
    month = date['start'][1]

    for product in products:
        sql = """
            select '{}', sum(nfp.nfpqtdade) as qtdade, 
            sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
            nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO
            from notas nfs
            left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                                and nfs.empcodigo = nfp.empcodigo
            left join produ    pro on pro.procodigo = nfp.procodigo
            left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
            where  nfs.nfdtemis between '{}' and '{}'  and EXTRACT(MONTH FROM nfs.nfdtemis) = {}
            and nfs.nfsit ='N' and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
            and nfs.fiscodigo1 in ('5.101','5.102','5.116','6.116','6.101','6.102','5.124','5.112')
        """

        sql = sql.format(product['label'], date_start, date_end, month)

        if business_code:
            sql = sql + ' and nfs.empcodigo = {}'.format(business_code)
        
        if product.get('process'):
            process = " and (tpl.tplprocesso = '{}')".format(product['process'])
        else:
            process = ''

        descriptions = ''
        for desc in product['descriptions']:
            if descriptions == '':
                descriptions = "TPL.tpldescricao LIKE '%{}%'".format(desc)
            else:
                descriptions = descriptions + \
                    " or TPL.tpldescricao LIKE '%{}%'".format(desc)

        sql = sql + ' and ({})'.format(descriptions)
        sql = sql + process

        sql = sql + ' group by nfs.empcodigo, ANO '

        sql = sql.replace('\n', ' ')

        if query == '':
            query = sql
        else:
            query = query + ' UNION ALL ' + sql

    session.execute(query)

    results = session.fetchall()

    list_products = []

    for column in results:
        product = {}
        product['label'] = column[0]
        product['amount'] = column[1]
        product['value'] = column[2]
        product['business_code'] = column[3]
        product['year'] = column[4]

        list_products.append(product)

    companies = list(set([p['business_code'] for p in list_products]))
    labels = list(set([p['label'] for p in list_products]))
    years = list(set([p['year'] for p in list_products]))

    response = {}

    for company in companies:
        if not response.get(company):
            response[company] = {}

        for label in labels:
            if not response[company].get(label):
                response[company][label] = {}
            
            for year in years:
                if not response[company][label].get(year):
                    response[company][label][year] = []
                
                response[company][label][year] = [p for p in list_products if p['year'] == year and p['business_code'] == company and p['label'] == label]
                
       

    return jsonify(response)
