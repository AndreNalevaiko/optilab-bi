from flask import Blueprint
from optilab_bi import connection

actions = Blueprint('rate_service', __name__, url_prefix='/rate_service')

@actions.route('/')
def hello():
    session = connection.cursor()
    sql = """
        select distinct ped.pedcodigo pedido, ped.empcodigo empresa, cli.clinomefant, EXTRACT(MONTH from ped.peddtemis) MES,  EXTRACT(YEAR from ped.peddtemis) ANO,
        (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) data_ini,
        (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) hora_ini,
        (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) data_fim,
        (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) hora_fim
        from pedid ped
        left join clien   cli on cli.clicodigo = ped.clicodigo
        where
        ped.peddtemis between '01/01/2018' and '03/31/2018' AND ped.pedcodigo like '%000'
        and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) is not null
        and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) is not null
        and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 28) is null
        and cli.clifornec = 'N'
    """

    session.execute(sql)
    
    results = session.fetchall()
    result_list = []
    for row in results:
        rate = {}

        rate['order'] = row[0]
        rate['business'] = row[1]
        rate['cli_nome_fan'] = row[2]
        rate['month'] = row[3]
        rate['year'] = row[4]
        rate['start_date'] = row[5]
        rate['start_hour'] = row[6]
        rate['end_date'] = row[7]
        rate['end_hour'] = row[8]

        result_list.append(rate)

    return result_list[0]