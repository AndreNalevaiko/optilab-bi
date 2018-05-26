def sql_all_products():
    return """
    select 'Transitions', 'Geral_Transitions',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})
    AND (TPL.tpldescricao LIKE '%TRANS%' or  TPL.tpldescricao LIKE '%NG%'
    or TPL.tpldescricao LIKE '%ACCLI%' or TPL.tpldescricao LIKE '%PHOTO%' ) and pro.gr4codigo <>  1
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Transitions', 'Trans Varilux', sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%VLX%' OR TPL.tpldescricao LIKE '%VARILUX%')
    AND (TPL.tpldescricao LIKE '%TRANS%' or  TPL.tpldescricao LIKE '%NG%'
    or TPL.tpldescricao LIKE '%ACCLI%' or TPL.tpldescricao LIKE '%PHOTO%' ) and pro.gr4codigo <>  1
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Transitions', 'Trans_Kodak',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%KODAK%')
    AND (TPL.tpldescricao LIKE '%TRANS%' or  TPL.tpldescricao LIKE '%NG%'
    or TPL.tpldescricao LIKE '%ACCLI%' or TPL.tpldescricao LIKE '%PHOTO%' ) and pro.gr4codigo <>  1
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Transitions', 'Trans_Itop',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%ITOP%')
    AND (TPL.tpldescricao LIKE '%TRANS%' or  TPL.tpldescricao LIKE '%NG%'
    or TPL.tpldescricao LIKE '%ACCLI%' or TPL.tpldescricao LIKE '%PHOTO%' ) and pro.gr4codigo <>  1
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Transitions', 'Trans_Vs',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S'
    AND (TPL.tpldescricao LIKE '%TRANS%' or  TPL.tpldescricao LIKE '%NG%'
    or TPL.tpldescricao LIKE '%ACCLI%' or TPL.tpldescricao LIKE '%PHOTO%' ) and pro.gr4codigo <>  1
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Geral_Varilux', sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Varilux_Digitime',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%DIGITIME%')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Varilux_Liberty',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs  
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%LIBERTY%')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Varilux_Comfort',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%COMFORT%')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Varilux_Physio',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and (tpl.tplprocesso = 'F') AND (TPL.tpldescricao LIKE '%PHYSIO%')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Varilux_E',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and (tpl.tplprocesso = 'F') AND (TPL.tpldescricao LIKE '% E %')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Varilux_X',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and (tpl.tplprocesso = 'F') AND (TPL.tpldescricao LIKE '% X %')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%')
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Varilux_S',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and (tpl.tplprocesso = 'F') AND (TPL.tpldescricao LIKE '% S %')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%')
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Varilux_Trad',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})
    and (tpl.tplprocesso = 'C') AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Varilux', 'Varilux_Digital',  sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})
    and (tpl.tplprocesso = 'F') AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%' )
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Kodak', 'Geral_Kodak',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'M' and tpl.tplprocesso = 'C'
    AND (TPL.tpldescricao LIKE '%KODAK%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Kodak', 'Kodak_Mult_Conv',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'M' and tpl.tplprocesso = 'C'
    AND (TPL.tpldescricao LIKE '%KODAK%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Kodak', 'Kodak_Mult_Dig',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'M' and tpl.tplprocesso = 'F'
    AND (TPL.tpldescricao LIKE '%KODAK%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Kodak', 'Kodak_Vs_Conv',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'C'
    AND (TPL.tpldescricao LIKE '%KODAK%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Kodak', 'Kodak_Vs_Digital',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'F'
    AND (TPL.tpldescricao LIKE '%KODAK%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Itop', 'Geral_Itop',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})
    AND (TPL.tpldescricao LIKE '%ITOP%' or  TPL.tpldescricao LIKE '%MULTILUX%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Itop', 'Itop_Mult',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'M'
    AND (TPL.tpldescricao LIKE '%ITOP%' or  TPL.tpldescricao LIKE '%MULTILUX%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Itop', 'Itop_Vs_Dig',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'F'
    AND (TPL.tpldescricao LIKE '%ITOP%' or  TPL.tpldescricao LIKE '%MULTILUX%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Itop', 'Itop_Vs_Conv',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'C'
    AND (TPL.tpldescricao LIKE '%ITOP%' or  TPL.tpldescricao LIKE '%MULTILUX%' ) 
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Crizal', 'Geral_Crizal',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})
    AND (TPL.tpldescricao LIKE '%CRIZAL%' OR TPL.tpldescricao LIKE '%CF UV%' OR TPL.tpldescricao LIKE '%C FORTE UV%'
    or TPL.tpldescricao LIKE '%C/AR PRIME%')
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Crizal', 'Crizal_Vs_Conv',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'C'
    AND (TPL.tpldescricao LIKE '%CRIZAL%' OR TPL.tpldescricao LIKE '%CF UV%' OR TPL.tpldescricao LIKE '%C FORTE UV%'
    or TPL.tpldescricao LIKE '%C/AR PRIME%')
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Crizal', 'Crizalç_Vs_Dig',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'F'
    AND (TPL.tpldescricao LIKE '%CRIZAL%' OR TPL.tpldescricao LIKE '%CF UV%' OR TPL.tpldescricao LIKE '%C FORTE UV%'
    or TPL.tpldescricao LIKE '%C/AR PRIME%')
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Crizal', 'Crizal_Varilux',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})  AND (TPL.tpldescricao LIKE '%VLX%' OR TPL.tpldescricao LIKE '%VARILUX%')
    AND (TPL.tpldescricao LIKE '%CRIZAL%' OR TPL.tpldescricao LIKE '%CF UV%' OR TPL.tpldescricao LIKE '%C FORTE UV%'
    or TPL.tpldescricao LIKE '%C/AR PRIME%')
    group by   ANO,  MES,  business_code
    UNION ALL
    select 'Crizal', 'Crizal_Kodak',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    iif( cli.funcodigo = 858, 5, nfs.empcodigo ) business_code, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    left join clien    cli on cli.clicodigo = nfs.clicodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})  AND (TPL.tpldescricao LIKE '%KODAK%')
    AND (TPL.tpldescricao LIKE '%CRIZAL%' OR TPL.tpldescricao LIKE '%CF UV%' OR TPL.tpldescricao LIKE '%C FORTE UV%'
    or TPL.tpldescricao LIKE '%C/AR PRIME%')
    group by   ANO,  MES,  business_code
    """