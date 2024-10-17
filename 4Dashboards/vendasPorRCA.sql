WITH Fat AS 
     (SELECT distinct(a.codusur) codusur,
             SUM(a.vlatend) Valor
        FROM pontual.PCPEDC a
        JOIN pontual.pcclient c on c.codcli = a.codcli
        WHERE a.DATA BETWEEN TO_DATE('{dtIni}', 'DD/MM/YYYY') AND TO_DATE('{dtFim}', 'DD/MM/YYYY')
          AND a.DTCANCEL IS NULL
          AND a.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
          AND a.CODCOB IN ('7563','CH','C','D','DH')
          AND a.vlbonific = 0
          AND A.NUMPEDRCA IS NOT NULL OR A.NUMPEDRCA = 0 -- GARANTE APENAS PEDIDOS DIGITADOS PELO RCA
          --AND c.TIPOFJ = 'J' 
          GROUP BY a.codusur),
-----------------------------------------------------------------------------------------------------------------------
DN AS (SELECT ped.codusur codusur,
                COUNT(DISTINCT ped.codcli) AS DN
            FROM pontual.PCPEDC ped
                JOIN pontual.PCPEDI pedi on pedi.numped = ped.numped
                JOIN pontual.pcprodut prod on pedi.codprod = prod.codprod
            WHERE ped.DATA BETWEEN TO_DATE('{dtIni}', 'DD/MM/YYYY') AND TO_DATE('{dtFim}', 'DD/MM/YYYY')
                AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
                AND ped.NUMPEDRCA IS NOT NULL OR ped.NUMPEDRCA = 0 -- GARANTE APENAS PEDIDOS DIGITADOS PELO RCA
            GROUP BY ped.codusur),
-----------------------------------------------------------------------------------------------------------------------
BASE AS (SELECT c.CODUSUR1, COUNT(DISTINCT(c.CODCLI)) BASE
         FROM pontual.pcclient c
         JOIN pontual.pcusuari u on c.CODUSUR1 = u.CODUSUR
         WHERE u.nome LIKE 'PMU%'
         GROUP BY c.CODUSUR1
         ORDER BY c.CODUSUR1)
-----------------------------------------------------------------------------------------------------------------------
SELECT U.codsupervisor, 
       (CASE WHEN U.codsupervisor = 2 THEN 'MARCELO'
             WHEN U.codsupervisor = 8 THEN 'VILMAR JR'
             WHEN U.codsupervisor = 9 THEN 'JOSEAN'
             ELSE 'DESCONHECIDO' END) AS SUPERVISOR,
        f.codusur || ' - ' || 
       SUBSTR(U.nome, INSTR(U.nome, ' ') + 1, INSTR(U.nome, ' ', INSTR(U.nome, ' ') + 1) - INSTR(U.nome, ' ') - 1) AS RCA,
       NVL(f.valor,0) VALOR, 
       NVL(D.DN,0) DN, 
       b.base
FROM FAT F
JOIN DN D on d.codusur = f.codusur
JOIN pontual.pcusuari u on u.codusur = f.codusur
JOIN BASE B on b.CODUSUR1= f.codusur
WHERE f.codusur not in (10,50)
ORDER BY  f.valor desc