def eval_months_buys():
    return """
    select nfs.CLICODIGO CLICODIGO, cli.CLINOMEFANT NOMEFANT, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    EXTRACT(MONTH FROM nfs.nfdtemis) num_month, EXTRACT(YEAR FROM nfs.nfdtemis) num_year,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) emp_code
    from notas nfs
    left join clien cli on cli.CLICODIGO = nfs.CLICODIGO 
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                            and nfs.empcodigo = nfp.empcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) IN ({latest_month},{current_month}) 
    and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years}) and nfs.nfsit ='N'
    and nfs.fiscodigo1 in ({list_cfop})
    group by emp_code, num_month, CLICODIGO, NOMEFANT, num_year
    """

# TODO alterar para medir os ativos pelos pedidos
def active_today_yesterday():
    return """
    /*DIA ATUAL E DIA ANTERIOR*/
    select COUNT(distinct nfs.CLICODIGO), iif( cli.funcodigo = 858, 5, nfs.empcodigo ) emp_code, EXTRACT(DAY FROM nfs.nfdtemis) day_buy
    from notas nfs
    left join clien cli on cli.CLICODIGO = nfs.CLICODIGO
    where nfs.NFDTEMIS in ('02/02/2018', '02/01/2018')
    and nfs.nfsit ='N'
    and nfs.fiscodigo1 in ('5.101','5.102','5.116','6.116','6.101','6.102','5.124','5.112')
    group by emp_code, day_buy
    order by day_buy asc, emp_code asc
    """

def active_current_previous_month():
    return """
    /*MES ATUAL E MES ANTERIOR*/
    select COUNT(distinct nfs.CLICODIGO), iif( cli.funcodigo = 858, 5, nfs.empcodigo ) emp_code, EXTRACT(MONTH FROM nfs.nfdtemis) num_month
    from notas nfs
    left join clien cli on cli.CLICODIGO = nfs.CLICODIGO
    where   EXTRACT(MONTH FROM nfs.nfdtemis) IN ('02','03') and EXTRACT(YEAR FROM nfs.nfdtemis) in ('2018')
    and nfs.nfsit ='N'
    and nfs.fiscodigo1 in ('5.101','5.102','5.116','6.116','6.101','6.102','5.124','5.112')
    group by emp_code, num_month
    order by num_month asc, emp_code asc
    """

def activer_latest_year():
    return """
    /*MEDIA ANO ANTERIOR - TEM QUE CALCULAR NO BACKEND*/
    select COUNT(distinct nfs.CLICODIGO), iif( cli.funcodigo = 858, 5, nfs.empcodigo ) emp_code, EXTRACT(MONTH FROM nfs.nfdtemis) num_month
    from notas nfs
    left join clien cli on cli.CLICODIGO = nfs.CLICODIGO
    where EXTRACT(YEAR FROM nfs.nfdtemis) = '2018'
    and nfs.nfsit ='N'
    and nfs.fiscodigo1 in ('5.101','5.102','5.116','6.116','6.101','6.102','5.124','5.112')
    group by emp_code, num_month
    order by num_month asc, emp_code asc
    """