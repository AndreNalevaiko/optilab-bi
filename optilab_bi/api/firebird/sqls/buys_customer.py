def eval_months_buys():
    return """
    select nfs.CLICODIGO CLICODIGO, cli.CLINOMEFANT NOMEFANT, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    EXTRACT(MONTH FROM nfs.nfdtemis) num_month, EXTRACT(YEAR FROM nfs.nfdtemis) num_year,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) emp_code
    from notas nfs
    left join clien cli on cli.CLICODIGO = nfs.CLICODIGO 
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                            and nfs.empcodigo = nfp.empcodigo
    where  EXTRACT(MONTH FROM nfs.nfdtemis) IN ({latest_month},{current_month}) 
    and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years}) and nfs.nfsit ='N'
    and nfs.fiscodigo1 in ({list_cfop})
    group by emp_code, num_month, CLICODIGO, NOMEFANT, num_year
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