from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from optilab_bi import  get_connection
from optilab_bi.api.mysql import configuration


actions = Blueprint('billing', __name__, url_prefix='/billing')

@actions.route('/', methods=['POST'])
@cross_origin()
def billing():
    connection = get_connection()
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
    SELECT sum(tmp.pedvrtotal) as vr_venda_bruta
     , tmp.empcodigo as emp_code
    from 
        ( 
    SELECT iif( cl.funcodigo = 858, 5, pd.empcodigo ) empcodigo
        , SUM(coalesce(pr.pdpvrcontabil,0)) pedvrtotal
    FROM Pedid pd 
            LEFT JOIN PdPrd pr   ON (pr.id_pedido = pd.id_pedido) 
            LEFT JOIN TbFis fis  ON (pr.FisCodigo = fis.FisCodigo)
            LEFT JOIN Clien cl   ON (pd.CliCodigo = cl.CliCodigo)
    WHERE EXTRACT(MONTH FROM pd.PedDtBaixa) = {month} and EXTRACT(YEAR FROM pd.PedDtBaixa) = {year}
    and pd.PedSitPed in ('B', 'F') and PedDtSaida is not null
    and ( (pr.pdplcfinan = 'S' and pd.pedlcfinanc <> 'L') or  (pr.pdplcfinan = 'N') or  (pd.pedlcfinanc = 'L' and pr.pdplcfinan = 'S'))
    and ( (pr.pdplcetq = 'S' and pd.pedlcestoq <> 'L') or (pr.pdplcetq = 'N') or (pr.pdplcetq = 'S' and pd.pedlcestoq = 'L')) 
    and (fis.FisTpNatOp in ('V', 'R', 'REG', 'REB', 'RG', 'RC', 'RB', 'OS', 'SF'))
    GROUP BY 1
    UNION 
    SELECT iif( cl.funcodigo = 858, 5, pd.empcodigo ) empcodigo
        , SUM(coalesce(ps.pdsvrcontabil,0)) pedvrtotal
    FROM Pedid pd 
            LEFT JOIN PdSer ps   ON (ps.id_pedido = pd.id_pedido) 
            LEFT JOIN TbFis fis  ON (fis.FisCodigo = ps.FisCodigo)
            LEFT JOIN Clien cl   ON (pd.CliCodigo = cl.CliCodigo)
    WHERE EXTRACT(MONTH FROM pd.PedDtBaixa) = {month} and EXTRACT(YEAR FROM pd.PedDtBaixa) = {year}
    and pd.PedSitPed in ('B', 'F') and PedDtSaida is not null
    and ( (ps.pdslcfinan = 'S' and pd.pedlcfinanc <> 'L') or  (ps.pdslcfinan = 'N') or  (pd.pedlcfinanc = 'L' and ps.pdslcfinan = 'S'))
    and ( (ps.pdslcetq = 'S' and pd.pedlcestoq <> 'L') or (ps.pdslcetq = 'N') or (ps.pdslcetq = 'S' and pd.pedlcestoq = 'L')) 
    and (fis.FisTpNatOp in ('V', 'R', 'REG', 'REB', 'RG', 'RC', 'RB', 'OS', 'SF'))
    GROUP BY 1
        ) tmp 
    group by 2
    """

    sql = sql.format(month=month, year=year)

    sql = sql.replace('\n', ' ')

    session.execute(sql)
    
    results = session.fetchall()
    result_list = []

    rate_global = {
        'business': 0,
        'value': 0
    }

    for column in results:
        rate = {}

        rate['value'] = float(str(column[0]))
        rate['business'] = column[1]

        rate_global['value'] = float(rate_global['value']) + float(column[0])
        rate_global['value'] = float(str(rate_global['value']))

        result_list.append(rate)
    
    result_list.append(rate_global)

    connection.close()

    return jsonify(result_list)