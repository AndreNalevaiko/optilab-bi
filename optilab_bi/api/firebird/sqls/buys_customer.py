def eval_months_buys():
    return """
    SELECT tmp.CLICODIGO 
     , tmp.CLINOME 
     , tmp.CidNome
     , sum(tmp.produto) as produto 
     , sum(tmp.servico) as servico 
     , sum(tmp.produto_desconto) as produto_desconto 
     , sum(tmp.servico_desconto) as servico_desconto 
     , sum(tmp.pedvrtotal) as vr_venda_bruta
     , count(distinct(tmp.id_pedido)) as qtdade
     , tmp.num_month as num_month 
     , tmp.num_year as num_year 
     , tmp.empcodigo as emp_code
    from 
        ( 
    SELECT cl.clicodigo 
        , CliNomeFant clinome 
        , cid.cidnome
        , SUM(Coalesce(pr.pdpvrdesctogeral,0) + (Coalesce(pr.pdpunitliquido,0) * Coalesce(pr.pdpqtdade,0))) produto 
        , 0 servico 
        , SUM(Coalesce(pr.pdpvrdesctogeral,0)) produto_desconto 
        , 0 servico_desconto 
        , pd.id_pedido
        , iif( cl.funcodigo = 858, 5, pd.empcodigo ) empcodigo
        , SUM(coalesce(pr.pdpvrcontabil,0)) pedvrtotal
        , count(pr.id_pedido) as qtdade 
        , EXTRACT(MONTH FROM pd.PedDtBaixa) num_month
        , EXTRACT(YEAR FROM pd.PedDtBaixa) num_year
    FROM Pedid pd 
            LEFT JOIN PdPrd pr   ON (pr.id_pedido = pd.id_pedido) 
            LEFT JOIN TbFis fis  ON (pr.FisCodigo = fis.FisCodigo)
            LEFT JOIN Clien cl   ON (pd.CliCodigo = cl.CliCodigo)
            LEFT JOIN EndCli ed  ON (pd.CliCodigo = ed.CliCodigo and pd.EndCodigo = ed.EndCodigo)
            LEFT JOIN Cidade cid ON (ed.CidCodigo = cid.CidCodigo)
            LEFT JOIN UF u       ON (u.ufcodigo = cid.CidUf)
            LEFT JOIN GrupoCli grp ON grp.gclcodigo = cl.gclcodigo 
    WHERE EXTRACT(MONTH FROM pd.PedDtBaixa) IN ({latest_month},{current_month}) and EXTRACT(YEAR FROM pd.PedDtBaixa) in ({years})
    and pd.PedSitPed in ('B', 'F') and PedDtSaida is not null
    and ( (pr.pdplcfinan = 'S' and pd.pedlcfinanc <> 'L') or  (pr.pdplcfinan = 'N') or  (pd.pedlcfinanc = 'L' and pr.pdplcfinan = 'S'))
    and ( (pr.pdplcetq = 'S' and pd.pedlcestoq <> 'L') or (pr.pdplcetq = 'N') or (pr.pdplcetq = 'S' and pd.pedlcestoq = 'L')) 
    and (fis.FisTpNatOp in ('V', 'R', 'REG', 'REB', 'RG', 'RC', 'RB', 'OS', 'SF'))
    GROUP BY 1,2,3,8,9,12,13
    UNION 
    SELECT cl.clicodigo 
        , CliNomeFant clinome 
        , cid.cidnome
        , 0 produto 
        , SUM(Coalesce(ps.pdsvrdesctogeral,0) + (Coalesce(ps.pdsunitliquido,0) * Coalesce(ps.pdsqtdade,0))) servico 
        , 0 produto_desconto 
        , SUM(Coalesce(ps.pdsvrdesctogeral,0)) servico_desconto 
        , pd.id_pedido
        , iif( cl.funcodigo = 858, 5, pd.empcodigo ) empcodigo
        , SUM(coalesce(ps.pdsvrcontabil,0)) pedvrtotal
        , count(ps.id_pedido) as qtdade
        , EXTRACT(MONTH FROM pd.PedDtBaixa) num_month
        , EXTRACT(YEAR FROM pd.PedDtBaixa) num_year
    FROM Pedid pd 
            LEFT JOIN PdSer ps   ON (ps.id_pedido = pd.id_pedido) 
            LEFT JOIN TbFis fis  ON (fis.FisCodigo = ps.FisCodigo) 
            LEFT JOIN Clien cl   ON (pd.CliCodigo = cl.CliCodigo)
            LEFT JOIN EndCli ed  ON (pd.CliCodigo = ed.CliCodigo and pd.EndCodigo = ed.EndCodigo)
            LEFT JOIN Cidade cid ON (ed.CidCodigo = cid.CidCodigo)
            LEFT JOIN UF u       ON (u.ufcodigo = cid.CidUf)
            LEFT JOIN GrupoCli grp ON grp.gclcodigo = cl.gclcodigo 
    WHERE EXTRACT(MONTH FROM pd.PedDtBaixa) IN ({latest_month},{current_month}) and EXTRACT(YEAR FROM pd.PedDtBaixa) in ({years}) 
    and pd.PedSitPed in ('B', 'F') and PedDtSaida is not null
    and ( (ps.pdslcfinan = 'S' and pd.pedlcfinanc <> 'L') or  (ps.pdslcfinan = 'N') or  (pd.pedlcfinanc = 'L' and ps.pdslcfinan = 'S'))
    and ( (ps.pdslcetq = 'S' and pd.pedlcestoq <> 'L') or (ps.pdslcetq = 'N') or (ps.pdslcetq = 'S' and pd.pedlcestoq = 'L')) 
    and (fis.FisTpNatOp in ('V', 'R', 'REG', 'REB', 'RG', 'RC', 'RB', 'OS', 'SF'))
    GROUP BY 1,2,3,8,9,12,13
    ORDER BY 1 
        ) tmp 
    group by 1,2,3,10,11,12
    ORDER BY 1 
    """

def active_today():
    return """
    /*DIA ATUAL*/
    select COUNT(distinct ped.CLICODIGO), iif( cli.funcodigo = 858, 5, ped.empcodigo ) emp_code
    from pedid ped
    left join clien cli on cli.CLICODIGO = ped.CLICODIGO
    where  1 = 1
    AND ped.PEDDTEMIS = '{current_month}-{current_day}-{current_year}'
    and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
    group by emp_code
    order by emp_code asc
    """

def active_today_yesterday():
    return """
    /*DIA ATUAL E DIA ANTERIOR*/
    select COUNT(distinct ped.CLICODIGO), iif( cli.funcodigo = 858, 5, ped.empcodigo ) emp_code, EXTRACT(DAY FROM ped.PEDDTEMIS) day_buy
    from pedid ped
    left join clien cli on cli.CLICODIGO = ped.CLICODIGO
    where 
    EXTRACT(DAY FROM ped.PEDDTEMIS) IN ({current_day},{latest_day}) AND 
    EXTRACT(YEAR FROM ped.PEDDTEMIS) = {current_year}  AND
    EXTRACT(MONTH FROM ped.PEDDTEMIS) = {current_month}
    and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
    group by emp_code, day_buy
    order by day_buy asc, emp_code asc
    """

def active_current_previous_month():
    return """
    /*MES ATUAL E MES ANTERIOR*/
    select COUNT(distinct ped.CLICODIGO), iif( cli.funcodigo = 858, 5, ped.empcodigo ) emp_code, EXTRACT(MONTH FROM ped.PEDDTEMIS) num_month
    from pedid ped
    left join clien cli on cli.CLICODIGO = ped.CLICODIGO
    where 
    EXTRACT(YEAR FROM ped.PEDDTEMIS) = {current_year}  AND
    EXTRACT(MONTH FROM ped.PEDDTEMIS) in ({current_month}, {latest_month})
    and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
    group by emp_code, num_month
    order by num_month asc, emp_code asc
    """

def active_latest_year():
    return """
    /*MEDIA ANO ANTERIOR - TEM QUE CALCULAR NO BACKEND*/
    select COUNT(distinct ped.CLICODIGO), iif( cli.funcodigo = 858, 5, ped.empcodigo ) emp_code, EXTRACT(MONTH FROM ped.PEDDTEMIS) num_month
    from pedid ped
    left join clien cli on cli.CLICODIGO = ped.CLICODIGO
    where 
    EXTRACT(YEAR FROM ped.PEDDTEMIS) = {latest_year}
    and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
    group by emp_code, num_month
    order by num_month asc, emp_code asc
    """