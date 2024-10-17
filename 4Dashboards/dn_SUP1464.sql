WITH DN_TOTAL as (   --TOTAL
        SELECT PED.CODSUPERVISOR AS RCA,
            COUNT(DISTINCT PED.CODCLI) AS DN
        FROM PONTUAL.PCPEDC PED
            JOIN PONTUAL.PCPEDI PEDI ON PEDI.NUMPED = PED.NUMPED
            JOIN PONTUAL.PCPRODUT PROD ON PEDI.CODPROD = PROD.CODPROD
        WHERE PED.DATA BETWEEN TRUNC(SYSDATE, 'MM') and LAST_DAY(SYSDATE)
            AND PROD.CODFORNEC = {fornec}
            AND PED.CODSUPERVISOR = {sup}
            AND PED.DTCANCEL IS NULL
            AND PED.POSICAO IN ('F')
            AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        GROUP BY PED.CODSUPERVISOR),

       ---------------------------------------------------------------   

META AS (
        SELECT PED.CODSUPERVISOR AS RCA,
            COUNT(DISTINCT PED.CODCLI) AS META
        FROM PONTUAL.PCPEDC PED
            JOIN PONTUAL.PCPEDI PEDI ON PEDI.NUMPED = PED.NUMPED
            JOIN PONTUAL.PCPRODUT PROD ON PEDI.CODPROD = PROD.CODPROD
        WHERE PED.DATA BETWEEN TRUNC(TRUNC(SYSDATE, 'MM') - 90) and TRUNC(SYSDATE, 'MM')
            AND PROD.CODFORNEC = {fornec}
            AND PED.CODSUPERVISOR =  {sup}
            AND PED.DTCANCEL IS NULL
            AND PED.POSICAO = 'F'
            AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        GROUP BY PED.CODSUPERVISOR)

--------------------------------------------------------------------------------------------------------------------
SELECT NVL(META.META, 0) AS OBJETIVO, 
    NVL(DN_TOTAL.DN, 0) AS REALIZADO, 
    GREATEST(NVL(META.META, 0) - NVL(DN_TOTAL.DN, 0), 0) AS "R.A.F.",
    (NVL(DN_TOTAL.DN, 1) / NVL(META.META, 1)) AS "% ATINGIDO"
FROM   DN_TOTAL
JOIN   META ON DN_TOTAL.RCA = META.RCA
