# from datetime import datetime
# from flask import Blueprint, jsonify, request
# from flask_cors import cross_origin

# from optilab_bi import  get_connection
# from optilab_bi.api.mysql import configuration


# actions = Blueprint('billing', __name__, url_prefix='/billing')

# @actions.route('/all_year', methods=['POST'])
# @cross_origin()
# def billing_all_year():
#     params = request.get_json()

#     date = params.get('date')
#     date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

#     init_date = date.replace(day=1, month=1).strftime('%Y-%m-%d')
#     end_date = date.strftime('%Y-%m-%d')

#     connection = get_connection()
#     session = connection.cursor()

#     sql = """
#     SELECT wallet, LAST_DAY(date) dt , sum(sold_value) 
#     FROM metrics.consolidation 
#     where product = '' and product_group = '' and date between '{init_date}' AND '{end_date}'
#     GROUP BY wallet, dt
#     UNION ALL
#     SELECT 'Global' wallet, LAST_DAY(date) dt , sum(sold_value) 
#     FROM metrics.consolidation 
#     where product = '' and product_group = '' and date between '{init_date}' AND '{end_date}'
#     GROUP BY wallet, dt;
#     """

#     sql = sql.format(
#         init_date=init_date,
#         end_date=end_date,
#     )

#     sql = sql.replace('\n', ' ')

#     session.execute(sql)
    
#     results = session.fetchall()
#     result_list = []

#     for column in results:
#         rate = {}

#         rate['value'] = float(str(column[2]))
#         rate['wallet'] = column[0]
#         rate['date'] = column[1]

#         result_list.append(rate)

#     connection.close()

#     return jsonify(result_list)


# @actions.route('/', methods=['POST'])
# @cross_origin()
# def billing():
#     params = request.get_json()

#     date = params.get('date')
#     date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

#     init_date = date.replace(day=1, month=1).strftime('%Y-%m-%d')
#     end_date = date.strftime('%Y-%m-%d')

#     connection = get_connection()
#     session = connection.cursor()

#     sql = """
#     SELECT tmp.wallet as wallet, sum(tmp.pedvrtotal) as vr_venda_bruta
#     from 
#         ( 
#     SELECT cl.FUNCODIGO wallet
#         , SUM(coalesce(pr.pdpvrcontabil,0)) pedvrtotal
#     FROM Pedid pd 
#             LEFT JOIN PdPrd pr   ON (pr.id_pedido = pd.id_pedido) 
#             LEFT JOIN TbFis fis  ON (pr.FisCodigo = fis.FisCodigo)
#             LEFT JOIN Clien cl   ON (pd.CliCodigo = cl.CliCodigo)
#     WHERE pd.PedDtBaixa between '{init_date}' AND '{end_date}'
#     and pd.PedSitPed in ('B', 'F') and PedDtSaida is not null
#     and ( (pr.pdplcfinan = 'S' and pd.pedlcfinanc <> 'L') or  (pr.pdplcfinan = 'N') or  (pd.pedlcfinanc = 'L' and pr.pdplcfinan = 'S'))
#     and ( (pr.pdplcetq = 'S' and pd.pedlcestoq <> 'L') or (pr.pdplcetq = 'N') or (pr.pdplcetq = 'S' and pd.pedlcestoq = 'L')) 
#     and (fis.FisTpNatOp in ('V', 'R', 'REG', 'REB', 'RG', 'RC', 'RB', 'OS', 'SF'))
#     GROUP BY 1
#     UNION 
#     SELECT cl.FUNCODIGO wallet
#         , SUM(coalesce(ps.pdsvrcontabil,0)) pedvrtotal
#     FROM Pedid pd 
#             LEFT JOIN PdSer ps   ON (ps.id_pedido = pd.id_pedido) 
#             LEFT JOIN TbFis fis  ON (fis.FisCodigo = ps.FisCodigo)
#             LEFT JOIN Clien cl   ON (pd.CliCodigo = cl.CliCodigo)
#     WHERE pd.PedDtBaixa between '{init_date}' AND '{end_date}'
#     and pd.PedSitPed in ('B', 'F') and PedDtSaida is not null
#     and ( (ps.pdslcfinan = 'S' and pd.pedlcfinanc <> 'L') or  (ps.pdslcfinan = 'N') or  (pd.pedlcfinanc = 'L' and ps.pdslcfinan = 'S'))
#     and ( (ps.pdslcetq = 'S' and pd.pedlcestoq <> 'L') or (ps.pdslcetq = 'N') or (ps.pdslcetq = 'S' and pd.pedlcestoq = 'L')) 
#     and (fis.FisTpNatOp in ('V', 'R', 'REG', 'REB', 'RG', 'RC', 'RB', 'OS', 'SF'))
#     GROUP BY 1
#         ) tmp 
#     group by 1
#     """

#     sql = sql.format(
#         init_date=init_date,
#         end_date=end_date,
#     )

#     sql = sql.replace('\n', ' ')

#     session.execute(sql)
    
#     results = session.fetchall()
#     result_list = []

#     rate_global = {
#         'wallet': 0,
#         'value': 0
#     }

#     for column in results:
#         rate = {}

#         rate['value'] = float(str(column[1]))
#         rate['wallet'] = column[0]

#         rate_global['value'] = float(rate_global['value']) + float(column[1])
#         rate_global['value'] = float(str(rate_global['value']))

#         result_list.append(rate)
    
#     result_list.append(rate_global)

#     connection.close()

#     return jsonify(result_list)