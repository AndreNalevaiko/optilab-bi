from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from optilab_bi import db2

actions = Blueprint('abstract_products', __name__, url_prefix='/abstract_products')

@actions.route('/', methods=['POST'])
@cross_origin()
def abstract_products():
    # Exemplo do POST
    # {
    #     "products": [
    #         {
    #         "descriptions": ["VLX", "VARILUX"],
    #         "process": "C",
    #         "label": "VARILUX-TRAD"
    #         },
    #         {
    #         "descriptions": ["VLX", "VARILUX"],
    #         "process": "F",
    #         "label": "VARILUX-DIG"
    #         }
    #     ],
    #     "period":{
    #         "date_start": "01/01/2017",
    #         "date_end": "31/12/2017"	
    #     },
    #     "business_code": 1
    # }

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

    date_start = '{}/{}/{}'.format(date['start'][1], date['start'][0], date['start'][2])
    date_end = '{}/{}/{}'.format(date['end'][1], date['end'][0], date['end'][2])

    for product in products:
        sql = """
            select '{}', tpl.tpldescricao ,sum(nfp.nfpqtdade) as qtdade,
            sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta
            from notas nfs
            left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                                and nfs.empcodigo = nfp.empcodigo
            left join produ    pro on pro.procodigo = nfp.procodigo
            left join marca    mar on pro.marcodigo = mar.marcodigo
            left join grupo2   gr2 on gr2.gr2codigo = pro.gr2codigo
            left join grulente gru on gru.glcodigo  = pro.glcodigo
            left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
            left join grupo4   gr4 on gr4.gr4codigo = pro.gr4codigo
            where  nfs.nfdtemis between '{}' and '{}'  
            and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
            and nfs.fiscodigo1 in ('5.101','5.102','5.116','6.116','6.101','6.102','5.124','5.112')
        """

        sql = sql.format(product['label'], date_start, date_end)

        if business_code:
            sql = sql + ' and nfs.empcodigo = {}'.format(business_code)

        process = " and (tpl.tplprocesso = '{}')".format(product['process'])

        descriptions = ''
        for desc in product['descriptions']:
            if descriptions == '':
                descriptions = "TPL.tpldescricao LIKE '%{}%'".format(desc)
            else:
                descriptions = descriptions + " or TPL.tpldescricao LIKE '%{}%'".format(desc)
        
        sql = sql + ' and ({})'.format(descriptions)
        sql = sql + process

        sql = sql + ' group by tpl.tpldescricao'

        sql = sql.replace('\n', ' ')

        if query == '':
            query = sql
        else:
            query = query + ' UNION ALL ' + sql

    db2.execute(query)
    
    results = db2.fetchall()
    result_list = []

    for column in results:
        rate = {}

        rate['label'] = column[0]
        rate['description'] = column[1]
        rate['amount'] = column[2]
        rate['value'] = column[3]

        result_list.append(rate)

    return jsonify(result_list)