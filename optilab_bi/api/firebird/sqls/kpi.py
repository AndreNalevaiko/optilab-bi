
def qtd_pedid():
    return """
    SELECT COUNT(ped.ID_PEDIDO), iif(cli.FUNCODIGO = 321, 5, ped.EMPCODIGO) empcodigo
    FROM PEDID ped
    LEFT JOIN clien cli on cli.CLICODIGO = ped.CLICODIGO
    WHERE 1 = 1
    AND ped.PEDDTEMIS between '{data_ini}' and '{data_fim}'
    AND ped.PEDCODIGO like '%000'
    and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
    GROUP BY empcodigo
    """

def vlr_pedid():
    return """
    SELECT SUM(ped.PEDVRTOTAL), iif(cli.FUNCODIGO = 321, 5, ped.EMPCODIGO) empcodigo
    FROM PEDID ped
    LEFT JOIN clien cli on cli.CLICODIGO = ped.CLICODIGO
    WHERE 1 = 1
    AND ped.PEDDTEMIS between '{data_ini}' and '{data_fim}'
    AND ped.PEDCODIGO like '%000'
    and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
    GROUP BY empcodigo
    """

def qtd_pecas_pedid():
    return """
    SELECT SUM(pdp.PDPQTDADE), iif(cli.FUNCODIGO = 321, 5, ped.EMPCODIGO) empcodigo
    FROM PEDID ped
    LEFT JOIN clien cli on cli.CLICODIGO = ped.CLICODIGO
    LEFT JOIN PDPRD pdp on pdp.ID_PEDIDO = ped.ID_PEDIDO
    LEFT JOIN PRODU pro on pro.PROCODIGO = pdp.PROCODIGO
    WHERE 1 = 1
    AND ped.PEDDTEMIS between '{data_ini}' and '{data_fim}'
    AND PRO.TPLCODIGO is not null
    and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
    GROUP BY empcodigo
    """
