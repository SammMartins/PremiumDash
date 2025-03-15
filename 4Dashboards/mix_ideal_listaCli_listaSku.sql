WITH DN_LISTA AS (
    SELECT 
        DISTINCT PED.CODCLI,    
        PED.CODUSUR AS COD
    FROM 
        PONTUAL.PCPEDC PED
        JOIN PONTUAL.PCPEDI PEDI ON PEDI.NUMPED = PED.NUMPED
        JOIN PONTUAL.PCPRODUT PROD ON PEDI.CODPROD = PROD.CODPROD
    WHERE 
        PED.DATA BETWEEN TRUNC(SYSDATE, 'MM') AND LAST_DAY(SYSDATE)
        AND PROD.CODFORNEC = 588 -- Danone
        AND PED.CODUSUR = {rca}
        AND PED.DTCANCEL IS NULL
        AND PED.POSICAO IN ('F')
        AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)    
),

CLIENTES AS (
    SELECT
        CLI.CODCLI,
        CLI.CLIENTE,
        CLI.FANTASIA,
        CLI.MUNICCOM
    FROM
        PONTUAL.PCCLIENT CLI
    WHERE
        CLI.CODCLI IN (SELECT CODCLI FROM DN_LISTA)
),

MIX AS (
    SELECT 
        PED.CODCLI,
        PED.CODUSUR AS COD,
        PEDI.CODPROD AS SKU
    FROM 
        PONTUAL.PCPEDC PED
        JOIN PONTUAL.PCPEDI PEDI ON PEDI.NUMPED = PED.NUMPED
        JOIN PONTUAL.PCPRODUT PROD ON PEDI.CODPROD = PROD.CODPROD
    WHERE 
        PED.DATA BETWEEN TRUNC(SYSDATE, 'MM') AND LAST_DAY(SYSDATE)
        AND PROD.CODFORNEC = 588 -- Danone
        AND PED.CODUSUR = {rca}
        AND PED.DTCANCEL IS NULL
        AND PED.POSICAO IN ('F')
        AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
)

SELECT
    DN_LISTA.COD,
    (SELECT SUBSTR(PCUSUARI.NOME, INSTR(PCUSUARI.NOME, ' ') + 1, 
                   INSTR(PCUSUARI.NOME, ' ', INSTR(PCUSUARI.NOME, ' ') + 1) - INSTR(PCUSUARI.NOME, ' ') - 1) 
     FROM PONTUAL.PCUSUARI WHERE PCUSUARI.CODUSUR = DN_LISTA.COD) AS NOME,
    TO_CHAR(CLIENTES.CODCLI) AS CODCLI,
    CLIENTES.CLIENTE,
    NVL(CLIENTES.FANTASIA, CLIENTES.CLIENTE) AS FANTASIA,
    CLIENTES.MUNICCOM,
    MAX(CASE WHEN MIX.SKU = 17528 and MIX.SKU = 18157 and MIX.SKU = 17507 and MIX.SKU = 17506 and MIX.SKU IN (18446,18447) and MIX.SKU = 17462 and MIX.SKU = 17507 and MIX.SKU = 17517 and MIX.SKU = 18035 and MIX.SKU = 17885 and MIX.SKU = 17932 and MIX.SKU = 18079 and MIX.SKU = 18448 THEN 1 ELSE 0 END) AS "MIX POSITIVADO",
    MAX(CASE WHEN MIX.SKU = 17528 THEN 1 ELSE 0 END) AS "17528", -- ACTIVIA 150g AMEIXA 
    MAX(CASE WHEN MIX.SKU = 18157 THEN 1 ELSE 0 END) AS "18157", -- POLPA KIDS MORANGO 
    MAX(CASE WHEN MIX.SKU = 17507 THEN 1 ELSE 0 END) AS "17507", -- DHO P LEVAR MORANGO
    MAX(CASE WHEN MIX.SKU = 17506 THEN 1 ELSE 0 END) AS "17506", -- DANONINHO 80g MORANGO
    MAX(CASE WHEN MIX.SKU IN (18446, 18447) THEN 1 ELSE 0 END) AS "18446 / 18447", -- ACTIVIA 800g AMEIXA E MORANGO
    MAX(CASE WHEN MIX.SKU = 17462 THEN 1 ELSE 0 END) AS "17462", -- DANONINHO MULTI 320g
    MAX(CASE WHEN MIX.SKU = 17507 THEN 1 ELSE 0 END) AS "17507", -- DANONINHO PARA BEBER 100g MORANGO
    MAX(CASE WHEN MIX.SKU = 17517 THEN 1 ELSE 0 END) AS "17517", -- DANONE VD 170G MORANGO
    MAX(CASE WHEN MIX.SKU = 18035 THEN 1 ELSE 0 END) AS "18035", -- DANETTE SOBREMESA CHOC 90g
    MAX(CASE WHEN MIX.SKU = 17885 THEN 1 ELSE 0 END) AS "17885", -- YOPRO UHT CHOCOLATE
    MAX(CASE WHEN MIX.SKU = 17932 THEN 1 ELSE 0 END) AS "17932", -- YOPRO LIQ 250G MORANGO
    MAX(CASE WHEN MIX.SKU = 18079 THEN 1 ELSE 0 END) AS "18079", -- DANONE MORANGO 850g
    MAX(CASE WHEN MIX.SKU = 18448 THEN 1 ELSE 0 END) AS "18448" -- DANONE CORPUS 800g MORANGO
FROM   
    DN_LISTA
JOIN
    CLIENTES ON DN_LISTA.CODCLI = CLIENTES.CODCLI
LEFT JOIN
    MIX ON DN_LISTA.CODCLI = MIX.CODCLI    
WHERE
    DN_LISTA.COD = {rca}
GROUP BY
    DN_LISTA.COD,
    CLIENTES.CODCLI,
    CLIENTES.CLIENTE,
    CLIENTES.FANTASIA,
    CLIENTES.MUNICCOM
ORDER BY
    CLIENTES.CODCLI