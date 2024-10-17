WITH FREEZER AS (
    SELECT 
        P.CODPROD
        ,P.DESCRICAO
    FROM
        PONTUAL.PCPRODUT P
    WHERE
        P.CODSEC IN (120426)
        --P.CODPROD IN (18662,18663,18664,18774,18773,18772,18771,18787,18946,18947)
),

SAIDA AS (
    SELECT 
        M.DTMOV
        ,M.CODCLI
        ,M.NUMNOTA
        ,M.CODPROD
        ,M.QT
    FROM
        PONTUAL.PCMOV M
    WHERE
        M.CODPROD IN (SELECT CODPROD FROM FREEZER)     
    AND
        M.QT > 0
    AND
        M.CODOPER = 'SR' -- SR = SAIDA | ER = ENTRADA
),

CLIENTE AS (
    SELECT 
        C.CODCLI
        ,C.CLIENTE
        ,C.fantasia
        ,C.codusur1
        ,C.cgcent
    FROM
        PONTUAL.PCCLIENT C
    WHERE
        C.CODCLI IN (SELECT CODCLI FROM SAIDA)
    AND C.CODCLI IS NOT NULL
)

SELECT 
    S.DTMOV
    ,S.CODCLI
    ,C.CLIENTE
    ,C.fantasia
    ,C.cgcent
    ,S.NUMNOTA
    ,S.CODPROD
    ,F.DESCRICAO
    ,S.QT
FROM
    SAIDA S
    LEFT JOIN FREEZER F ON S.CODPROD = F.CODPROD
    LEFT JOIN CLIENTE C ON S.CODCLI = C.CODCLI
--WHERE
    --C.CODUSUR1 != 164
    --AND C.CLIENTE LIKE '%BARBOSA%'
--AND S.CODCLI = 4473
