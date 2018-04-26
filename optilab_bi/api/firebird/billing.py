from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from optilab_bi import db2


actions = Blueprint('billing', __name__, url_prefix='/billing')

@actions.route('/', methods=['POST'])
@cross_origin()
def billing():
    # Exemplo POST
    # {
	# 	"period":{
	# 		"date_start": "01/01/2017",
	# 		"date_end": "31/12/2017"	
	# 	}
	# }
    args = request.get_json()

    period = args.get('period')

    if not period:
        return 'Period not found', 404

    date = {
        'start': period['date_start'].split('/'),
        'end': period['date_end'].split('/')
    }

    date_start = '{}/{}/{}'.format(date['start'][1], date['start'][0], date['start'][2])
    date_end = '{}/{}/{}'.format(date['end'][1], date['end'][0], date['end'][2])

    sql = """
        select sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta, nfs.empcodigo
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
        and nfs.nfsit ='N'   and nfp.nfcodigo is not null
        and nfs.fiscodigo1 in ('5.101','5.102','5.116','6.116','6.101','6.102','5.124','5.112')
        group by nfs.empcodigo
    """

    sql = sql.format(date_start, date_end)

    sql = sql.replace('\n', ' ')

    db2.execute(sql)
    
    results = db2.fetchall()
    result_list = []

    for column in results:
        rate = {}

        rate['value'] = column[0]
        rate['business'] = column[1]

        result_list.append(rate)

    return jsonify(result_list)