def group_by_types():
    return """
    select distinct 'ACABADAS', ped.pedcodigo pedido, tpl.tpldescricao, ped.empcodigo empresa, cli.clinomefant, EXTRACT(MONTH from ped.peddtemis) MES,  EXTRACT(YEAR from ped.peddtemis) ANO,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) data_ini,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) hora_ini,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) data_fim,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) hora_fim
    from pedid ped
    left join clien   cli on cli.clicodigo = ped.clicodigo
    left join pdprd   prd on prd.id_pedido = ped.id_pedido
    left join produ   pro on pro.procodigo = prd.procodigo
    left join tplente tpl on tpl.tplcodigo = pro.tplcodigo
    left join pdlente pdl on pdl.id_pedido = ped.id_pedido
    where
    ped.peddtemis between '{data_ini}' and '{data_final}' and ped.peddtsaida <= '{data_final}' AND ped.pedcodigo like '%000'
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) is not null
    and prd.procodigo in (select produ.procodigo from produ where produ.gr1codigo = 2)
    and cli.clifornec = 'N'
    and pdl.tplcodigo_od = pdl.tplcodigo_oe
    UNION ALL
    select distinct 'SURF S/ COL. OU VERNIZ', ped.pedcodigo pedido, tpl.tpldescricao, ped.empcodigo empresa, cli.clinomefant, EXTRACT(MONTH from ped.peddtemis) MES,  EXTRACT(YEAR from ped.peddtemis) ANO,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) data_ini,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) hora_ini,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) data_fim,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) hora_fim
    from pedid ped
    left join clien   cli on cli.clicodigo = ped.clicodigo
    left join pdprd   prd on prd.id_pedido = ped.id_pedido
    left join produ   pro on pro.procodigo = prd.procodigo
    left join tplente tpl on tpl.tplcodigo = pro.tplcodigo
    left join pdlente pdl on pdl.id_pedido = ped.id_pedido
    where
    ped.peddtemis between '{data_ini}' and '{data_final}' and ped.peddtsaida <= '{data_final}' AND ped.pedcodigo like '%000'
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 7) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 33) is null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 32) is null
    and cli.clifornec = 'N' AND tpl.tpldescricao is not null
    and pdl.tplcodigo_od = pdl.tplcodigo_oe
    UNION ALL
    select distinct 'SURF C/ COL OU VERNIZ', ped.pedcodigo pedido, tpl.tpldescricao, ped.empcodigo empresa, cli.clinomefant, EXTRACT(MONTH from ped.peddtemis) MES,  EXTRACT(YEAR from ped.peddtemis) ANO,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) data_ini,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) hora_ini,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) data_fim,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) hora_fim
    from pedid ped
    left join clien   cli on cli.clicodigo = ped.clicodigo
    left join pdprd   prd on prd.id_pedido = ped.id_pedido
    left join produ   pro on pro.procodigo = prd.procodigo
    left join tplente tpl on tpl.tplcodigo = pro.tplcodigo
    left join pdlente pdl on pdl.id_pedido = ped.id_pedido
    where
    ped.peddtemis between '{data_ini}' and '{data_final}' and ped.peddtsaida <= '{data_final}' AND ped.pedcodigo like '%000'
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 7) is not null    
    and ((select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 33/*VERNIZ*/) is not null
    OR (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 32/*COLORAÇÃO*/) is not null)
    AND tpl.tpldescricao is not null and cli.clifornec = 'N'
    and pdl.tplcodigo_od = pdl.tplcodigo_oe
    UNION ALL
    select distinct 'SURF C/ AR', ped.pedcodigo pedido, tpl.tpldescricao, ped.empcodigo empresa, cli.clinomefant, EXTRACT(MONTH from ped.peddtemis) MES,  EXTRACT(YEAR from ped.peddtemis) ANO,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) data_ini,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) hora_ini,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) data_fim,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) hora_fim
    from pedid ped
    left join clien   cli on cli.clicodigo = ped.clicodigo
    left join pdprd   prd on prd.id_pedido = ped.id_pedido
    left join produ   pro on pro.procodigo = prd.procodigo
    left join tplente tpl on tpl.tplcodigo = pro.tplcodigo
    left join pdlente pdl on pdl.id_pedido = ped.id_pedido
    where
    ped.peddtemis between '{data_ini}' and '{data_final}' and ped.peddtsaida <= '{data_final}' AND ped.pedcodigo like '%000'
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 7/*SURF*/) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 19/*AR*/) is not null
    AND tpl.tpldescricao is not null and cli.clifornec = 'N'
    and pdl.tplcodigo_od = pdl.tplcodigo_oe
    UNION ALL
    select distinct 'DIGITAL GERAL', ped.pedcodigo pedido, tpl.tpldescricao, ped.empcodigo empresa, cli.clinomefant, EXTRACT(MONTH from ped.peddtemis) MES,  EXTRACT(YEAR from ped.peddtemis) ANO,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) data_ini,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) hora_ini,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) data_fim,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) hora_fim
    from pedid ped
    left join clien   cli on cli.clicodigo = ped.clicodigo
    left join pdprd   prd on prd.id_pedido = ped.id_pedido
    left join produ   pro on pro.procodigo = prd.procodigo
    left join tplente tpl on tpl.tplcodigo = pro.tplcodigo
    left join pdlente pdl on pdl.id_pedido = ped.id_pedido
    where
    ped.peddtemis between '{data_ini}' and '{data_final}' and ped.peddtsaida <= '{data_final}' AND ped.pedcodigo like '%000'
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) is not null
    and tpl.tplprocesso = 'F' and cli.clifornec = 'N'
    and pdl.tplcodigo_od = pdl.tplcodigo_oe
    UNION ALL
    select distinct 'VARILUX X', ped.pedcodigo pedido, tpl.tpldescricao, ped.empcodigo empresa, cli.clinomefant, EXTRACT(MONTH from ped.peddtemis) MES,  EXTRACT(YEAR from ped.peddtemis) ANO,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) data_ini,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) hora_ini,
    (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) data_fim,
    (select first 1 aphora from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) hora_fim
    from pedid ped
    left join clien   cli on cli.clicodigo = ped.clicodigo
    left join pdprd   prd on prd.id_pedido = ped.id_pedido
    left join produ   pro on pro.procodigo = prd.procodigo
    left join tplente tpl on tpl.tplcodigo = pro.tplcodigo
    left join pdlente pdl on pdl.id_pedido = ped.id_pedido
    where
    ped.peddtemis between '{data_ini}' and '{data_final}' and ped.peddtsaida <= '{data_final}' AND ped.pedcodigo like '%000'
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 1) is not null
    and (select first 1 apdata from acoped where id_pedido = ped.id_pedido and lpcodigo = 10) is not null
    and tpl.tplprocesso = 'F' and cli.clifornec = 'N' and tpl.tpldescricao like '%VARILUX X%'
    and pdl.tplcodigo_od = pdl.tplcodigo_oe
    """


def all():
    return """
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