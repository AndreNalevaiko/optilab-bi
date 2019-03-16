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
     , {seller_column} as seller
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
        , cl.funcodigo seller
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
    WHERE pd.PedDtBaixa between dateadd(-1 month to date '{current_month}-01-{current_year}') 
    and '{current_month}-{current_day}-{current_year}'
    and pd.PedSitPed in ('B', 'F') and PedDtSaida is not null
    and ( (pr.pdplcfinan = 'S' and pd.pedlcfinanc <> 'L') or  (pr.pdplcfinan = 'N') or  (pd.pedlcfinanc = 'L' and pr.pdplcfinan = 'S'))
    and ( (pr.pdplcetq = 'S' and pd.pedlcestoq <> 'L') or (pr.pdplcetq = 'N') or (pr.pdplcetq = 'S' and pd.pedlcestoq = 'L')) 
    and (fis.FisTpNatOp in ('V', 'R', 'REG', 'REB', 'RG', 'RC', 'RB', 'OS', 'SF')) {sellers}
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
        , cl.funcodigo seller
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
    WHERE pd.PedDtBaixa between dateadd(-1 month to date '{current_month}-01-{current_year}') 
    and '{current_month}-{current_day}-{current_year}'
    and pd.PedSitPed in ('B', 'F') and PedDtSaida is not null
    and ( (ps.pdslcfinan = 'S' and pd.pedlcfinanc <> 'L') or  (ps.pdslcfinan = 'N') or  (pd.pedlcfinanc = 'L' and ps.pdslcfinan = 'S'))
    and ( (ps.pdslcetq = 'S' and pd.pedlcestoq <> 'L') or (ps.pdslcetq = 'N') or (ps.pdslcetq = 'S' and pd.pedlcestoq = 'L')) 
    and (fis.FisTpNatOp in ('V', 'R', 'REG', 'REB', 'RG', 'RC', 'RB', 'OS', 'SF')) {sellers}
    GROUP BY 1,2,3,8,9,12,13
    ORDER BY 1 
        ) tmp 
    group by 1,2,3,10,11,12
    ORDER BY 1 
    """

# def active_today():
#     return """
#     /*DIA ATUAL*/
#     select COUNT(distinct ped.CLICODIGO), {seller_column} emp_code
#     from pedid ped
#     left join clien cli on cli.CLICODIGO = ped.CLICODIGO
#     where  1 = 1
#     AND ped.PEDDTEMIS = '{current_month}-{current_day}-{current_year}'
#     and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
#     group by seller
#     """

def active_today():
    return """
    /*DIA ATUAL*/
    SELECT count(distinct tmp.ct_cli), {seller_column} seller FROM (

        select ped.CLICODIGO ct_cli, cli.funcodigo seller,
        EXTRACT(DAY FROM ped.PEDDTEMIS) day_buy,
        SUM(ped.pedvrtotal) ped_vlr
        from pedid ped
        left join clien cli on cli.CLICODIGO = ped.CLICODIGO
        where 
        ped.PEDDTEMIS = '{current_month}-{current_day}-{current_year}'
        and (ped.FISCODIGO1 in ({list_cfop})
        or ped.FISCODIGO2 in ({list_cfop}))
        and ped.pedsitped in ('B','F') {sellers}
        group by ct_cli, seller , day_buy

    )  AS tmp
    WHERE tmp.ped_vlr > {cutting_average}
    group by seller
    """

# def active_today_yesterday():
#     return """
#     /*DIA ATUAL E DIA ANTERIOR*/
#     select COUNT(distinct ped.CLICODIGO), {seller_column} seller, EXTRACT(DAY FROM ped.PEDDTEMIS) day_buy
#     from pedid ped
#     left join clien cli on cli.CLICODIGO = ped.CLICODIGO
#     where 
#     EXTRACT(DAY FROM ped.PEDDTEMIS) IN ({current_day},{latest_day}) AND 
#     EXTRACT(YEAR FROM ped.PEDDTEMIS) = {current_year}  AND
#     EXTRACT(MONTH FROM ped.PEDDTEMIS) = {current_month}
#     and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
#     group by seller, day_buy
#     """

def active_today_yesterday():
    return """
    /*DIA ATUAL E DIA ANTERIOR*/
    SELECT count(distinct tmp.ct_cli), {seller_column} seller, tmp.day_buy day_buy FROM (

        select  ped.CLICODIGO ct_cli, cli.funcodigo seller,
        EXTRACT(DAY FROM ped.PEDDTEMIS) day_buy,
        SUM(ped.pedvrtotal) ped_vlr
        from pedid ped
        left join clien cli on cli.CLICODIGO = ped.CLICODIGO
        where 
        ped.PEDDTEMIS between dateadd(-1 day to date'{current_month}-{current_day}-{current_year}')
        and dateadd(-1 month to date'{current_month}-{current_day}-{current_year}')
        and (ped.FISCODIGO1 in ({list_cfop})
        or ped.FISCODIGO2 in ({list_cfop}))
        and ped.pedsitped in ('B','F') {sellers}
        group by ct_cli, seller , day_buy

    )  AS tmp
    WHERE tmp.ped_vlr > {cutting_average}
    group by seller, day_buy
    """

# def active_current_previous_month():
#     return """
#     /*MES ATUAL E MES ANTERIOR*/
#     select COUNT(distinct ped.CLICODIGO), {seller_column} seller, EXTRACT(MONTH FROM ped.PEDDTEMIS) num_month
#     from pedid ped
#     left join clien cli on cli.CLICODIGO = ped.CLICODIGO
#     where 
#     EXTRACT(YEAR FROM ped.PEDDTEMIS) = {current_year}  AND
#     EXTRACT(MONTH FROM ped.PEDDTEMIS) in ({current_month}, {latest_month})
#     and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
#     group by seller, num_month
#     """

def active_current_previous_month():
    return """
    /*MES ATUAL E MES ANTERIOR*/
    SELECT count(distinct tmp.ct_cli), {seller_column} seller, tmp.num_month num_month FROM (

        select  ped.CLICODIGO ct_cli, cli.funcodigo seller,
        EXTRACT(MONTH FROM ped.PEDDTEMIS) num_month,
        SUM(ped.pedvrtotal) ped_vlr
        from pedid ped
        left join clien cli on cli.CLICODIGO = ped.CLICODIGO
        where 
        ped.PEDDTEMIS between dateadd(-1 month to date'{current_month}-01-{current_year}')
        and '{current_month}-{current_day}-{current_year}'
        and (ped.FISCODIGO1 in ({list_cfop})
        or ped.FISCODIGO2 in ({list_cfop}))
        and ped.pedsitped in ('B','F') {sellers}
        group by ct_cli, seller , num_month

    )  AS tmp
    WHERE tmp.ped_vlr > {cutting_average}
    group by seller, num_month
    """

# def active_latest_year():
#     return """
#     /*MEDIA ANO ANTERIOR - TEM QUE CALCULAR NO BACKEND*/
#     select COUNT(distinct ped.CLICODIGO), {seller_column} seller, EXTRACT(MONTH FROM ped.PEDDTEMIS) num_month
#     from pedid ped
#     left join clien cli on cli.CLICODIGO = ped.CLICODIGO
#     where 
#     EXTRACT(YEAR FROM ped.PEDDTEMIS) = {latest_year}
#     and (ped.FISCODIGO1 in ({list_cfop}) or ped.FISCODIGO2 in ({list_cfop}))
#     group by seller
#     """

def active_latest_year():
    return """
    /*MEDIA ANO ANTERIOR - TEM QUE CALCULAR NO BACKEND*/

    SELECT count(distinct tmp.ct_cli), {seller_column} seller, tmp.num_month num_month FROM (

        select  ped.CLICODIGO ct_cli, cli.funcodigo seller,
        EXTRACT(MONTH FROM ped.peddtbaixa) num_month,
        SUM(ped.pedvrtotal) ped_vlr
        from pedid ped
        left join clien cli on cli.CLICODIGO = ped.CLICODIGO
        where
        ped.peddtbaixa between dateadd(-1 year to date '01-01-{current_year}')
        and dateadd(-1 day to date '01-01-{current_year}')
        and (ped.FISCODIGO1 in ({list_cfop})
        or ped.FISCODIGO2 in ({list_cfop}))
        and ped.pedsitped in ('B','F') {sellers}
        group by ct_cli, seller , num_month

    )  AS tmp
    WHERE tmp.ped_vlr > {cutting_average}
    group by seller, num_month

    """