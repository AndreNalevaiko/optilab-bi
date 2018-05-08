from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from optilab_bi import connection
from optilab_bi.api.mysql import configuration, product as product_api

actions = Blueprint('abstract_products', __name__,
                    url_prefix='/abstract_products')


@actions.route('/', methods=['POST'])
@cross_origin()
def abstract_products():
    session = connection.cursor()

    query = ''
    args = request.get_json()

    products = product_api.get_products_abstract()
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

    cfop_configuration = configuration.get_config('cfop_vendas')

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
            and nfs.fiscodigo1 in ({})
        """

        sql = sql.format(product.label, date_start, date_end, month, cfop_configuration)

        if business_code:
            sql = sql + ' and nfs.empcodigo = {}'.format(business_code)

        if product.process:
            process = " and (tpl.tplprocesso = '{}')".format(product.process)
        else:
            process = ''

        str_like_or = ''
        str_like_and = ''

        if product.like_or:
            for desc in product.like_or.split(','):
                if str_like_or == '':
                    str_like_or = "TPL.tpldescricao LIKE '%{}%'".format(desc)
                else:
                    str_like_or = str_like_or + \
                        " or TPL.tpldescricao LIKE '%{}%'".format(desc)

        if product.like_and:
            for desc in product.like_and.split(','):
                if str_like_and == '':
                    str_like_and = "TPL.tpldescricao LIKE '%{}%'".format(desc)
                else:
                    str_like_and = str_like_and + \
                        " and TPL.tpldescricao LIKE '%{}%'".format(desc)


        if str_like_or:
            sql = sql + ' and ({})'.format(str_like_or)
        
        if str_like_and:
            sql = sql + ' and ({})'.format(str_like_or)

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

    products = product_api.get_products_abstract()
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

    cfop_configuration = configuration.get_config('cfop_vendas')

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
            and nfs.fiscodigo1 in ({})
        """

        sql = sql.format(product.label, date_start, date_end, month, cfop_configuration)

        if business_code:
            sql = sql + ' and nfs.empcodigo = {}'.format(business_code)
        
        if product.process:
            process = " and (tpl.tplprocesso = '{}')".format(product.process)
        else:
            process = ''

        str_like_or = ''
        str_like_and = ''

        if product.like_or:
            for desc in product.like_or.split(','):
                if str_like_or == '':
                    str_like_or = "TPL.tpldescricao LIKE '%{}%'".format(desc)
                else:
                    str_like_or = str_like_or + \
                        " or TPL.tpldescricao LIKE '%{}%'".format(desc)
        if product.like_and:
            for desc in product.like_and.split(','):
                if str_like_and == '':
                    str_like_and = "TPL.tpldescricao LIKE '%{}%'".format(desc)
                else:
                    str_like_and = str_like_and + \
                        " and TPL.tpldescricao LIKE '%{}%'".format(desc)


        if str_like_or:
            sql = sql + ' and ({})'.format(str_like_or)
        
        if str_like_and:
            sql = sql + ' and ({})'.format(str_like_or)

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
