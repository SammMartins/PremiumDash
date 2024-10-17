WITH BASE_ATIVA AS (
    SELECT  
        COUNT(DISTINCT(USUARI.CODCLI)) QTCLIATIVOS,
        USUARI.codusur
    FROM (
        SELECT 
            PCCLIENT.CODCLI,
            PCCLIENT.CODusur1 codusur 
        FROM 
            PONTUAL.PCCLIENT, 
            PONTUAL.PCUSUARI, 
            PONTUAL.PCSUPERV, 
            PONTUAL.PCPRACA                                                         
        WHERE 
            PCCLIENT.CODUSUR1 = PCUSUARI.CODUSUR 
            AND PCUSUARI.CODSUPERVISOR = PCSUPERV.CODSUPERVISOR(+)          
            AND PCCLIENT.CODPRACA = PCPRACA.CODPRACA          
            AND PCCLIENT.DTULTCOMP >= sysdate - 90            
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
            AND PCUSUARI.CODSUPERVISOR IN (2, 8)
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
        
        UNION                                                                      
                                                                                   
        SELECT                                                                  
            PCCLIENT.CODCLI,
            PCCLIENT.CODusur1 codusur                                                
        FROM                                                                    
            PONTUAL.PCCLIENT,                                                             
            PONTUAL.PCUSUARI, 
            PONTUAL.PCSUPERV, 
            PONTUAL.PCPRACA                                                         
        WHERE                                                                   
            PCCLIENT.CODUSUR2 = PCUSUARI.CODUSUR                             
            AND PCUSUARI.CODSUPERVISOR = PCSUPERV.CODSUPERVISOR(+)                 
            AND PCCLIENT.CODPRACA = PCPRACA.CODPRACA          
            AND PCCLIENT.DTULTCOMP >= sysdate - 90             
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
            AND PCUSUARI.CODSUPERVISOR IN (2, 8)
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
                    
        UNION                                                                      
                                                                                   
        SELECT                                                                
            PCCLIENT.CODCLI,
            PCCLIENT.CODusur1 codusur                                        
        FROM                                                                  
            PONTUAL.PCUSURCLI,                                                         
            PONTUAL.PCCLIENT,                                                          
            PONTUAL.PCUSUARI, 
            PONTUAL.PCSUPERV, 
            PONTUAL.PCPRACA                                                         
        WHERE     
            PCUSURCLI.CODUSUR = PCUSUARI.CODUSUR                        
            AND PCUSUARI.CODSUPERVISOR = PCSUPERV.CODSUPERVISOR(+)           
            AND PCCLIENT.CODPRACA = PCPRACA.CODPRACA                         
            AND PCUSURCLI.CODCLI = PCCLIENT.CODCLI                        
            AND PCCLIENT.DTULTCOMP >= sysdate - 90       
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
            AND PCUSUARI.CODSUPERVISOR IN (2, 8)
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
       
    ) USUARI

    GROUP BY
        USUARI.CODUSUR        
),

SKU AS ( 
    SELECT 
        COUNT(DISTINCT(A.CODCLI)) DN,
        A.CODUSUR,
        ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT(A.CODCLI)) DESC) AS RN
    FROM
        PONTUAL.PCPEDI A
    WHERE
        A.CODPROD IN (SELECT CODPROD FROM PONTUAL.PCPRODUT WHERE CODFORNEC = 1719)
        AND A.DATA BETWEEN '01-aug-2024' AND '31-aug-2024'
        AND A.VLBONIFIC = 0
        AND (A.CODPROD IN (18645, 18944)
        OR (A.CODPROD = 18639 OR A.CODPROD = 18637))
        
    GROUP BY
        A.CODUSUR
    HAVING
        COUNT(DISTINCT A.CODPROD) = 3
        AND COUNT(DISTINCT CASE WHEN A.CODPROD IN (18645, 18944) THEN A.CODPROD END) = 2
        AND COUNT(DISTINCT CASE WHEN A.CODPROD IN (18639, 18637) THEN A.CODPROD END) = 1
        AND COUNT(DISTINCT(A.CODCLI)) >= 15
    ORDER BY 
        1 DESC
),

SKU_VOL AS ( 
    SELECT 
        SUM(A.QT) VOL,
        A.CODUSUR,
        ROW_NUMBER() OVER (ORDER BY SUM(A.QT) DESC) AS RN
    FROM
        PONTUAL.PCPEDI A
    WHERE
        A.CODPROD IN (SELECT CODPROD FROM PONTUAL.PCPRODUT WHERE CODFORNEC = 1719)
        AND A.DATA BETWEEN '01-aug-2024' AND '31-aug-2024'
        AND A.VLBONIFIC = 0
        AND (A.CODPROD IN (18645, 18944)
        OR (A.CODPROD = 18639 OR A.CODPROD = 18637))
        
    GROUP BY
        A.CODUSUR
    HAVING
        COUNT(DISTINCT A.CODPROD) = 3
        AND COUNT(DISTINCT CASE WHEN A.CODPROD IN (18645, 18944) THEN A.CODPROD END) = 2
        AND COUNT(DISTINCT CASE WHEN A.CODPROD IN (18639, 18637) THEN A.CODPROD END) = 1
        AND COUNT(DISTINCT(A.CODCLI)) >= 15        
    ORDER BY 
        1 DESC
),

POSIT AS ( 
    SELECT 
        A.CODCLI,
        A.CODUSUR,
        SUM(A.QT * A.PVENDA) TICKET
    FROM
        PONTUAL.PCPEDI A
    WHERE
        A.CODPROD IN (SELECT CODPROD FROM PONTUAL.PCPRODUT WHERE CODFORNEC = 1719)
        AND A.DATA BETWEEN '01-aug-2024' AND '31-aug-2024'
        AND A.VLBONIFIC = 0

    GROUP BY
        A.CODCLI, 
        A.CODUSUR
)


SELECT  
    usur.codsupervisor AS SUP,
    USUR.CODUSUR COD,
    SUBSTR(USUR.NOME, INSTR(USUR.NOME, ' ') + 1, INSTR(USUR.NOME, ' ', INSTR(USUR.NOME, ' ') + 1) - INSTR(USUR.NOME, ' ') - 1) AS RCA, -- EXTRAI O NOME
    B.QTCLIATIVOS "BASE",
    COUNT(DISTINCT(C.CODCLI)) AS "DN",
    (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) || '%' "%" ,
    TRUNC(NVL(AVG(C.TICKET),0.00),2) "TICKET_MÉDIO",

    (CASE 
        WHEN S.RN = 1 THEN 'SIM'
        ELSE 'NÃO'
    END) AS "MAIOR_DN_SKU's",

    (CASE 
        WHEN SV.RN = 1 THEN 'SIM'
        ELSE 'NÃO'
    END) AS "MAIOR_VOLUME_SKU's",

    (CASE
        WHEN NVL(AVG(C.TICKET), 0.00) > 200 THEN
            CASE
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 55 THEN 350.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 50 THEN 300.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 45 THEN 250.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 40 THEN 200.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 35 THEN 150.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 30 THEN 100.00
                ELSE 0.00
            END
        ELSE
            CASE
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 55 THEN 175.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 50 THEN 150.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 45 THEN 125.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 40 THEN 100.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 35 THEN 75.00
                WHEN (TRUNC((COUNT(DISTINCT(C.CODCLI))) / (B.QTCLIATIVOS), 2) * 100) >= 30 THEN 50.00
                ELSE 0.00
            END
    END +
    CASE 
        WHEN S.RN = 1 THEN 100 
        ELSE 0 
    END +
    CASE 
        WHEN SV.RN = 1 THEN 100 
        ELSE 0 
    END) AS "R$"

FROM 
    PONTUAL.PCUSUARI USUR
LEFT JOIN 
    BASE_ATIVA B ON USUR.CODUSUR = B.CODUSUR
LEFT JOIN 
    POSIT C ON USUR.CODUSUR = C.CODUSUR
LEFT JOIN 
    SKU S ON USUR.CODUSUR = S.CODUSUR 
LEFT JOIN 
    SKU_VOL SV ON USUR.CODUSUR = SV.CODUSUR 
GROUP BY 
    USUR.CODUSUR, 
    USUR.NOME,
    usur.codsupervisor,
    B.QTCLIATIVOS,
    S.RN,
    SV.RN
HAVING 
    USUR.NOME LIKE 'PMU%' 
AND 
    USUR.CODUSUR NOT IN (2, 160, 10)
ORDER BY
    10 DESC, 
    6 DESC,
    7 DESC,
    5 DESC