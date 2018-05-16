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

    cfop_configuration = configuration.get_config('cfop_vendas')

    month = period['month']
    year = period['year']

    sql = """
        select sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta, nfs.empcodigo
        from notas nfs
        left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                            and nfs.empcodigo = nfp.empcodigo
        left join produ    pro on pro.procodigo = nfp.procodigo
        left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
        where  EXTRACT(MONTH FROM nfs.nfdtemis) = {} and EXTRACT(YEAR FROM nfs.nfdtemis) = {}  
        and nfs.nfsit ='N'   and nfp.nfcodigo is not null
        and nfs.fiscodigo1 in ({})
        group by nfs.empcodigo
    """

    sql = sql.format(month, year, cfop_configuration)

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