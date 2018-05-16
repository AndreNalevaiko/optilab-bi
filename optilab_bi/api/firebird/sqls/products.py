def abstract_products():
    return """
    select 'vlx_digitime',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%DIGITIME%')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'vlx_liberty',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs  
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%LIBERTY%')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'vlx_comfort',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%COMFORT%')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'vlx_physio',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and (tpl.tplprocesso = 'F') AND (TPL.tpldescricao LIKE '%PHYSIO%')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'vlx_e',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and (tpl.tplprocesso = 'F') AND (TPL.tpldescricao LIKE '% E %')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%') 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'vlx_x',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and (tpl.tplprocesso = 'F') AND (TPL.tpldescricao LIKE '% X %')
    AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%')
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'vlx_trad',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})
    and (tpl.tplprocesso = 'C') AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%' ) 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'vlx_digital',  sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})
    and (tpl.tplprocesso = 'F') AND (TPL.tpldescricao LIKE '%VLX%' or  TPL.tpldescricao LIKE '%VARILUX%' )
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'kodak_mult_conv',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'M' and tpl.tplprocesso = 'C'
    AND (TPL.tpldescricao LIKE '%KODAK%' ) 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'kodak_mult_dig',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'M' and tpl.tplprocesso = 'F'
    AND (TPL.tpldescricao LIKE '%KODAK%' ) 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'kodak_vs_conv',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'C'
    AND (TPL.tpldescricao LIKE '%KODAK%' ) 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'kodak_vs_digital',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'F'
    AND (TPL.tpldescricao LIKE '%KODAK%' ) 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'itop_mult',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'M'
    AND (TPL.tpldescricao LIKE '%ITOP%' or  TPL.tpldescricao LIKE '%MULTILUX%' ) 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'itop_vs_dig',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'F'
    AND (TPL.tpldescricao LIKE '%ITOP%' or  TPL.tpldescricao LIKE '%MULTILUX%' ) 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'itop_vs_conv',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'C'
    AND (TPL.tpldescricao LIKE '%ITOP%' or  TPL.tpldescricao LIKE '%MULTILUX%' ) 
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'cz_vs_conv',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'C'
    AND (TPL.tpldescricao LIKE '%CRIZAL%' OR TPL.tpldescricao LIKE '%CF UV%' OR TPL.tpldescricao LIKE '%C FORTE UV%'
    or TPL.tpldescricao LIKE '%C/AR PRIME%')
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'cz_vs_dig',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S' and tpl.tplprocesso = 'F'
    AND (TPL.tpldescricao LIKE '%CRIZAL%' OR TPL.tpldescricao LIKE '%CF UV%' OR TPL.tpldescricao LIKE '%C FORTE UV%'
    or TPL.tpldescricao LIKE '%C/AR PRIME%')
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'cz_vlx',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})  AND (TPL.tpldescricao LIKE '%VLX%' OR TPL.tpldescricao LIKE '%VARILUX%')
    AND (TPL.tpldescricao LIKE '%CRIZAL%' OR TPL.tpldescricao LIKE '%CF UV%' OR TPL.tpldescricao LIKE '%C FORTE UV%'
    or TPL.tpldescricao LIKE '%C/AR PRIME%')
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'cz_kodak',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop})  AND (TPL.tpldescricao LIKE '%KODAK%')
    AND (TPL.tpldescricao LIKE '%CRIZAL%' OR TPL.tpldescricao LIKE '%CF UV%' OR TPL.tpldescricao LIKE '%C FORTE UV%'
    or TPL.tpldescricao LIKE '%C/AR PRIME%')
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'trans_vlx',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%VLX%' OR TPL.tpldescricao LIKE '%VARILUX%')
    AND (TPL.tpldescricao LIKE '%TRANS%' or  TPL.tpldescricao LIKE '%NG%'
    or TPL.tpldescricao LIKE '%ACCLI%' or TPL.tpldescricao LIKE '%PHOTO%' ) and pro.gr4codigo <>  1
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'trans_kodak',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%KODAK%')
    AND (TPL.tpldescricao LIKE '%TRANS%' or  TPL.tpldescricao LIKE '%NG%'
    or TPL.tpldescricao LIKE '%ACCLI%' or TPL.tpldescricao LIKE '%PHOTO%' ) and pro.gr4codigo <>  1
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'trans_itop',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) AND (TPL.tpldescricao LIKE '%ITOP%')
    AND (TPL.tpldescricao LIKE '%TRANS%' or  TPL.tpldescricao LIKE '%NG%'
    or TPL.tpldescricao LIKE '%ACCLI%' or TPL.tpldescricao LIKE '%PHOTO%' ) and pro.gr4codigo <>  1
    group by   ANO,  MES,  nfs.empcodigo
    UNION ALL
    select 'trans_vs',sum(nfp.nfpqtdade) as qtdade, sum(nfp.nfpqtdade * nfp.nfpunitliquido) as vr_venda_bruta,
    nfs.empcodigo, EXTRACT(YEAR FROM nfs.nfdtemis) ANO, EXTRACT(MONTH FROM nfs.nfdtemis) MES
    from notas nfs
    left join nfpro    nfp on nfs.nfcodigo  = nfp.nfcodigo
                        and nfs.empcodigo = nfp.empcodigo
    left join produ    pro on pro.procodigo = nfp.procodigo
    left join tplente  tpl on tpl.tplcodigo = pro.tplcodigo
    where   EXTRACT(MONTH FROM nfs.nfdtemis) = {month} and EXTRACT(YEAR FROM nfs.nfdtemis) in ({years})
    and nfs.nfsit ='N'   and nfp.nfcodigo is not null AND tpl.tpldescricao is not null
    and nfs.fiscodigo1 in ({list_cfop}) and tpl.tpltipo = 'S'
    AND (TPL.tpldescricao LIKE '%TRANS%' or  TPL.tpldescricao LIKE '%NG%'
    or TPL.tpldescricao LIKE '%ACCLI%' or TPL.tpldescricao LIKE '%PHOTO%' ) and pro.gr4codigo <>  1
    group by   ANO,  MES,  nfs.empcodigo
    """

