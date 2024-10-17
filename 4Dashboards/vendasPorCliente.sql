WITH Fat AS 
     (SELECT a.CODCLI,
            a.codusur codusur,
            a.CODSUPERVISOR,
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
          GROUP BY a.codusur,a.CODCLI,a.CODSUPERVISOR)
-----------------------------------------------------------------------------------------------------------------------
SELECT  f.codcli || ' - ' || SUBSTR(C.CLIENTE,0,23) cliente,
        U.codsupervisor, 
        f.codusur || ' - ' || SUBSTR(U.nome, INSTR(U.nome, ' ') + 1, INSTR(U.nome, ' ', INSTR(U.nome, ' ') + 1) - INSTR(U.nome, ' ') - 1) as RCA,
        F.valor
FROM FAT F
JOIN pontual.pcusuari u on u.codusur = f.codusur
JOIN PONTUAL.PCCLIENT C ON C.CODCLI = F.CODCLI
WHERE f.codusur not in (10,50)
ORDER BY  f.valor desc