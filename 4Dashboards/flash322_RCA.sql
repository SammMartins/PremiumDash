-- CTE's: (Cada uma delas obtem valores das vendas por supervisor em diferentes seções de produtos)
WITH SUPPLF --IOGURTE DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10040,10042,120239) -- PLF
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR
    ORDER By FAT DESC),
    
       ---------------------------------------------------------------
       
SUPACT --ACTIVIA DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10040) -- ACTIVIA
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),
    
       ---------------------------------------------------------------
       
SUPDHO --DANONINHO DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10042) -- DANONINHO
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),
    
       ---------------------------------------------------------------
       
SUPGRA --GRANADA DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (120239) -- GRANADA
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),
    
       ---------------------------------------------------------------       
           
SUPUHT -- UHT DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10046) --UHT
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC), 
    
       ---------------------------------------------------------------       
           
SUPREQ --REQUEIJAO DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10047) --REQUEIJAO
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),    
    
       ---------------------------------------------------------------       
           
SUPYOP --YOPRO DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10048) -- YOPRO
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),       
          
--------------------------------------------------------------------------------
           
SUPSUL --SULMINAS
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10050) -- SULMINAS
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),  
    
--------------------------------------------------------------------------------
           
SUPFIN --FINI
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (11007) -- FINI
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),           
    
--------------------------------------------------------------------------------
           
SUPGUL --GULOZITOS
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10044) -- GULOZITOS
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),             
              
--------------------------------------------------------------------------------
           
SUPECO --ECOFRESH
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (120427) -- ECOFRESH
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),             
    
--------------------------------------------------------------------------------
           
SUPDFT --DAFRUTA
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (120387) -- DAFRUTA
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),        
--------------------------------------------------------------------------------
           
SUPDNL --DANILLA
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (120424)  --DANILLA
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),    
    
--------------------------------------------------------------------------------
           
SUPSEA -- SEARA MASSA LEVE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10001) -- SEARA MASSA LEVE
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),       
     
--------------------------------------------------------------------------------
           
SUPHYT -- HYTS
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (1005) -- HYTS
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),     
     
--------------------------------------------------------------------------------
           
SUPSTM -- SANTA MASSA
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (1023) -- SANTA MASSA
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),  
     
--------------------------------------------------------------------------------
           
SUPFTP -- FRUTAP
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10041) -- FRUTAP
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),  
     
--------------------------------------------------------------------------------
           
SUPMGN --MARGARINA
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (1003) --MARGARINA
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),  

--------------------------------------------------------------------------------
           
TOTAL --TOTAL
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10041,1023,1005,10001,120424,120387,120427,10044,11007,10046,10047,120239,10048,10042,1003,10040)
        AND ped.data BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),     
                                                                                     
------------------------------------------META---------------------------------------------------    
META -- (Essa CTE obtem os valores da meta dos vendedores - que posteriormente é somado para a obtenção dos valores por vendedor)
AS (
SELECT d.CODSUPERVISOR CODSUPERVISOR,
       m.codusur, m.codigo CODSEC,
       NVL((CASE WHEN m.cliposprev IS NULL or m.cliposprev = 0 THEN 500 
       ELSE m.cliposprev END),100) AS cliposprev
FROM pontual.PCMETA M 
JOIN pontual.PCUSUARI C ON M.CODUSUR = C.CODUSUR
JOIN pontual.PCSUPERV D ON C.CODSUPERVISOR = D.CODSUPERVISOR
JOIN pontual.PCSECAO E ON M.CODIGO = E.CODSEC
WHERE M.data = TRUNC(SYSDATE, 'MM')
AND M.TIPOMETA = 'S'
AND E.CODSEC IN (10040, -- ACTIVIA DANONE
                1003, -- MARGARINA
                10042, -- DANONINHO DANONE
                10048, -- YOPRO DANONE
                120239, -- GRANADA DANONE
                10050, -- SULMINAS
                10047, -- REQUEIJÃO DANONE
                10046, -- UHT DANONE
                11007, -- FINI
                10044, -- GULOZITOS
                120427, -- ECOFRESH
                120387, -- DAFRUTA
                120424, -- DANILLA
                10001, -- SEARA MASSA LEVE
                1005, -- HYTS
                1023, -- SANTA MASSA
                10041) -- FRUTAP
AND d.CODSUPERVISOR IN (2,8)
),
-------------------------------------------------------------------------------------------------

DIAS AS 
(SELECT 
    (SELECT COUNT(*) AS QTDIASVENDAS 
    FROM PONTUAL.PCDIASUTEIS
    WHERE CODFILIAL = 3
    AND DIAVENDAS = 'S'
    AND TO_CHAR(DATA, 'MM') = TO_CHAR(SYSDATE, 'MM')
    AND TO_CHAR(DATA, 'YYYY') = TO_CHAR(SYSDATE, 'YYYY'))  as DIASUTEIS, 

    (SELECT COUNT(DIASDECORRIDOS)
    FROM (
        SELECT 
            CASE WHEN DATA <= SYSDATE-1 THEN 'D' ELSE 'F' END AS DIASDECORRIDOS
        FROM PONTUAL.PCDIASUTEIS
        WHERE CODFILIAL = 3
        AND DIAVENDAS = 'S'
        AND TO_CHAR(DATA, 'MM') = TO_CHAR(SYSDATE, 'MM')
        AND TO_CHAR(DATA, 'YYYY') = TO_CHAR(SYSDATE, 'YYYY')
    ) 
    WHERE DIASDECORRIDOS = 'D') AS DIASDECORR 
FROM DUAL) -- A 'DUAL' é uma tabela especial de uma linha e uma coluna presente por padrão no Oracle. É adequado para uso na seleção de uma pseudocoluna.

---------------------------------CONSULTAS PRINCIPAIS--------------------------------------------

-----------------------------------------PLF-----------------------------------------------------
SELECT 0 AS "ORDER", -- Pseudocoluna criada para fazer a ordenão das linhas
       'PLF TOTAL' AS CATEGORIA,
    -------------------------------------------------------------------
       to_number((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODUSUR = a.CODUSUR)) AS OBJETIVO,
    -------------------------------------------------------------------
       to_number(SUM(A.fat)) AS Realizado,
    -------------------------------------------------------------------
       to_number(TRUNC((SUM(A.FAT) / (SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODUSUR = a.CODUSUR)),5))
            as "% ATING.",
    -------------------------------------------------------------------
       to_number(TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    (SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (10040,10042,120239) 
                                AND m.CODUSUR = a.CODUSUR)
        ),5)) AS "% TEND.",
    -------------------------------------------------------------------    
        to_number(GREATEST(TRUNC((
        ((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODUSUR = a.CODUSUR)) - SUM(A.fat) 
            
         ),2),0))   as "R.A.F.",
    -------------------------------------------------------------------  
         to_number(GREATEST(( 
         ((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODUSUR = a.CODUSUR) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0)) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          (SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODUSUR = a.CODUSUR) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPPLF A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis


---------------------------------------ACTIVIA---------------------------------------------------
UNION
SELECT 1.0 AS "ORDER",
       'PLF/Activia' as CATEGORIA,
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------               
              
FROM SUPACT A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec


--------------------------------------DANONINHO--------------------------------------------------
UNION
SELECT 1.1 AS "ORDER",
       'PLF/Danoninho' as CATEGORIA,
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------                 
              
FROM SUPDHO A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec


---------------------------------------GRANADA---------------------------------------------------
UNION
SELECT 1.2 AS "ORDER",
       'PLF/Granada' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------            
              
FROM SUPGRA A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

-----------------------------------------UHT-----------------------------------------------------
UNION
SELECT 1.3 AS "ORDER",
       'UHT' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------                 
              
FROM SUPUHT A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

----------------------------------------REQUEIJÃO------------------------------------------------
UNION
SELECT 1.4 AS "ORDER",
       'REQUEIJÃO' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------                 
              
FROM SUPREQ A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

-------------------------------------------YOPRO-------------------------------------------------
UNION
SELECT 1.5 AS "ORDER",
       'YOPRO' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPYOP A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

----------------------------------------SULMINAS-------------------------------------------------
UNION
SELECT 2 AS "ORDER",
       'SULMINAS' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPSUL A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

----------------------------------------FINI--------------------------------------------
UNION
SELECT 2 AS "ORDER",
       'FINI' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPFIN A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

----------------------------------------GULOZITOS--------------------------------------------
UNION
SELECT 2 AS "ORDER",
       'GULOZITOS' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPGUL A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

---------------------------------------ECOFRESH-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'ECOFRESH' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPECO A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

---------------------------------------DAFRUTA-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'DAFRUTA' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPDFT A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

---------------------------------------DANILLA-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'DANILLA' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPDNL A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

---------------------------------------SEARA-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'MASSA LEVE' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPSEA A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

---------------------------------------HYTS-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'HYTS' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPHYT A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

--------------------------------------SANTA MASSA---------------------------------------
UNION
SELECT 2 AS "ORDER",
       'SANTA MASSA' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPSTM A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

------------------------------------------FRUTAP----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'FRUTAP' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPFTP A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

-----------------------------------------MARGARINA----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'MARGARINA' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPMGN A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, d.DIASDECORR, d.DIASuteis, a.codsec

-----------------------------------------TOTAL----------------------------------------
UNION
SELECT 3 AS "ORDER",
       'TOTAL' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE m.CODUSUR = a.CODUSUR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE m.CODUSUR = a.CODUSUR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE m.CODUSUR = a.CODUSUR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE m.CODUSUR = a.CODUSUR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE m.CODUSUR = a.CODUSUR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE m.CODUSUR = a.CODUSUR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              

FROM TOTAL A, DIAS d
WHERE a.CODUSUR = {rca}
GROUP BY a.CODUSUR, D.DIASUTEIS, D.diasdecorr, D.DIASUTEIS, D.diasdecorr



------------------ORDENAÇÃO------------------
    ORDER BY "ORDER" ASC, "R.A.F." DESC
