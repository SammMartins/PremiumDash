-- INADIMPLÊNCIA POR SUPERVISOR
SELECT  (SELECT X.codsupervisor FROM PONTUAL.PCUSUARI X WHERE X.CODUSUR = B.CODUSUR1) SUP,
        B.codusur1 RCA,
        
        SUBSTR(USUR.NOME,
        INSTR(USUR.NOME, ' ') + 1,
        INSTR(USUR.NOME, ' ', INSTR(USUR.NOME, ' ') + 1) - INSTR(USUR.NOME, ' ') - 1) AS NOME,

        A.CODCLI || ' ' || SUBSTR(B.CLIENTE,0,20) CLIENTE, 
        (CASE WHEN 
            (SELECT DISTINCT(X.CODCLI) 
                FROM PONTUAL.PCPEDI X 
                WHERE X.CODCLI = A.CODCLI 
                AND TO_NUMBER(TO_CHAR(X.DATA, 'WW')) = TO_NUMBER(TO_CHAR(SYSDATE, 'WW'))
                AND TO_NUMBER(TO_CHAR(X.DATA, 'YY')) = TO_NUMBER(TO_CHAR(SYSDATE, 'YY'))
                AND X.POSICAO IN ('B','P') ) IS NOT NULL THEN 'SIM'
         ELSE 'NÃO' END
        ) AS "PED. SISTEMA",
        A.valor Título,
        ROUND((A.valor * 0.00333) * ROUND(SYSDATE - A.dtvenc, 0)) AS "JUROS APROXIMADOS", 
        ROUND(A.valor + ((A.valor * 0.00333) * ROUND(SYSDATE - A.dtvenc, 0))) Total,
        (CASE WHEN A.codcob LIKE 'SERA' THEN 'SERASA'
              WHEN A.codcob LIKE 'CHD1' THEN 'CHEQUE'
              WHEN A.codcob LIKE '7563' THEN 'BOLETO'
              ELSE 'OUTROS' END) AS "COB.", 
        ROUND(SYSDATE - A.dtvenc, 0) AS "DIAS VENCIMENTO", 
        A.dtemissao EMISSAO,
        A.dtvenc VENCIMENTO
       
FROM pontual.pcprest A
JOIN pontual.pcclient B ON A.codcli = B.codcli
JOIN pontual.pcusuari USUR ON USUR.CODUSUR = B.CODUSUR1
WHERE A.dtvenc BETWEEN SYSDATE - 732 AND SYSDATE - 1
AND A.vpago IS NULL
AND (A.codusur NOT IN (10) AND B.codusur1 NOT IN (10))
AND A.CODCLI NOT IN (3480, 15286, 15492, 11185, 7724, 2325) -- CLIENTES A DESCONSIDERAR POR SEREM FUNCIONÁRIOS OU CÓDIGOS INTERNOS
AND A.codcob IN ('7563','SERA','C','CHD1')

ORDER BY "DIAS VENCIMENTO" DESC, TÍTULO DESC