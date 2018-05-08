from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from optilab_bi import connection
from optilab_bi.api.mysql import configuration


actions = Blueprint('billing', __name__, url_prefix='/billing')

@actions.route('/', methods=['POST'])
@cross_origin()
def billing():
    session = connection.cursor()
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

    cfop_configuration = configuration.get_config('cfop_vendas')

    sql = """
        select sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta, nfs.empcodigo
        from notas nfs
        left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                            and nfs.empcodigo = nfp.empcodigo
        left join produ    pro on pro.procodigo = nfp.procodigo
        left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
        where  nfs.nfdtemis between '{}' and '{}'  
        and nfs.nfsit ='N'   and nfp.nfcodigo is not null
        and nfs.fiscodigo1 in ({})
        group by nfs.empcodigo
    """

    sql = sql.format(date_start, date_end, cfop_configuration)

    sql = sql.replace('\n', ' ')

    session.execute(sql)
    
    results = session.fetchall()
    result_list = []

    for column in results:
        rate = {}

        rate['value'] = column[0]
        rate['business'] = column[1]

        result_list.append(rate)

    return jsonify(result_list)