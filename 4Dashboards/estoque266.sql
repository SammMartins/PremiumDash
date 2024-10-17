WITH PARAMETROS                                                 
  AS (SELECT PCFILIAL.CODIGO CODFILIAL                          
           , COALESCE(PCPARAMFILIAL.VALOR, PCCONSUM.BLOQUEIAVENDAESTPENDENTE) BLOQUEIAVENDAESTPENDENTE                                 
           , NVL(PCPARAMETROWMS.VALOR,'N') DESBLOQUEARPRODFIMOS 
           , NVL(PCFILIAL.USAWMS, 'N') USAWMS                 
           , NVL (PCFILIAL.AUTOSERVICO, 'S') AUTOSERVICO      
        FROM PONTUAL.PCFILIAL                                           
           , PONTUAL.PCCONSUM
           , PONTUAL.PCPARAMFILIAL                                      
           , PONTUAL.PCPARAMETROWMS                                     
       WHERE PCFILIAL.CODIGO <> '99'                          
         AND PCFILIAL.DTEXCLUSAO IS NULL                        
         AND PCFILIAL.CODIGO        = PCPARAMETROWMS.CODFILIAL(+) 
         AND PCPARAMETROWMS.NOME(+) = 'DESBLOQUEARPRODFIMOS'  
         AND PCFILIAL.CODIGO        = PCPARAMFILIAL.CODFILIAL(+)  
         AND PCPARAMFILIAL.NOME(+)  = 'BLOQUEIAVENDAESTPENDENTE'                                                                     
AND PCFILIAL.CODIGO IN('3')                                                 
  AND (PCFILIAL.CODIGO IN (SELECT PCLIB.CODIGOA               
                           FROM PONTUAL.PCLIB                         
                           WHERE CODTABELA = 1                
                              )          
          OR EXISTS (SELECT PCLIB.CODIGOA                     
                     FROM PONTUAL.PCLIB                               
                     WHERE CODTABELA = 1                            
                       AND PCLIB.CODIGOA = '99'))           
       )                                                        
   , LOGDESBLOQUEIO                                             
     AS (SELECT PCLOGDESBLOQUEIO.CODPROD                        
              , PCLOGDESBLOQUEIO.CODFILIAL                      
              , MAX(PCLOGDESBLOQUEIO.CODFUNCDESBLOQUEIO) AS CODFUNCDESBLOQUEIO                                                         
              , MAX(PCLOGDESBLOQUEIO.OBS) OBS                   
           FROM PONTUAL.PCLOGDESBLOQUEIO                                
              , PONTUAL.PARAMETROS                                      
          WHERE PCLOGDESBLOQUEIO.CODFILIAL = PARAMETROS.CODFILIAL 
            AND PCLOGDESBLOQUEIO.DTDESBLOQUEIO = (SELECT MAX(LOG.DTDESBLOQUEIO)                                                        
                                                    FROM PONTUAL.PCLOGDESBLOQUEIO LOG                                                          
                                                   WHERE LOG.CODFILIAL = PARAMETROS.CODFILIAL                                          
                                                     AND LOG.CODPROD   = PCLOGDESBLOQUEIO.CODPROD                                      
                                                     AND LOG.CODFILIAL = PCLOGDESBLOQUEIO.CODFILIAL                                    
                                                     AND LOG.DTDESBLOQUEIO >= (SYSDATE - 150)                                          
                                                  )             
          GROUP                                                 
             BY PCLOGDESBLOQUEIO.CODPROD                        
              , PCLOGDESBLOQUEIO.CODFILIAL),

FORNEC AS
(SELECT DISTINCT
        F.CODFORNEC

    FROM
        PONTUAL.PCFORNEC F
    JOIN
        PONTUAL.PCPRODUT P ON F.CODFORNEC = P.CODFORNEC
    JOIN
        PONTUAL.PCPEDI D ON P.CODPROD = D.CODPROD
    WHERE
        D.DATA BETWEEN SYSDATE - 32 AND SYSDATE),

preco as (SELECT DISTINCT 
    PCPRODUT.CODPROD,
    PCPRODUT.DESCRICAO, 
    PCPRODUT.CODFORNEC,
    PCEST.CUSTOREAL, 
    PCEST.CUSTOFIN, 
    PCEST.CUSTOULTENT,  
    PCTABPR.PTABELA
FROM 
    PONTUAL.PCPRODUT
    INNER JOIN PONTUAL.PCEST ON PCPRODUT.CODPROD = PCEST.CODPROD
    INNER JOIN PONTUAL.PCTABPR ON PCPRODUT.CODPROD = PCTABPR.CODPROD
WHERE 
    PCEST.CODFILIAL = 3 
    AND PCTABPR.NUMREGIAO IN (1)
    AND NVL(PCTABPR.EXCLUIDO, 'N') <> 'S'
    AND PCPRODUT.DESCRICAO LIKE '%'
    AND NVL(PCPRODUT.OBS, 'X') <> 'PV'
    AND PCPRODUT.CODFORNEC IN (
        SELECT 
            DISTINCT FORNEC.CODFORNEC
        FROM
            FORNEC
    )
)              
              
                                   
                                                                
SELECT PCEST.CODPROD || ''
     , PCEST.DTULTENT
     , PCPRODUT.DESCRICAO
     , SUBSTR(PCPRODUT.CODFORNEC,0,20) Fornecedor
     , (SELECT F.FORNECEDOR FROM PONTUAL.PCFORNEC F WHERE F.CODFORNEC = PCPRODUT.CODFORNEC) AS FORNECEDOR                               
     , PCPRODUT.EMBALAGEM 
     , PCEST.qtultent
     , NVL (PCPRODUT.QTUNITCX, 0) QTUNITCX
     , NVL(PCEST.QTESTGER, 0) + NVL(PCEST.QTRESERV, 0) qtdest                                                   
     , PONTUAL.PKG_ESTOQUE.ESTOQUE_DISPONIVEL(TRUNC(PCEST.CODPROD,2), TRUNC(PCEST.CODFILIAL,2), 'V') || '' QTDISP
    , PRECO.CUSTOREAL * PONTUAL.PKG_ESTOQUE.ESTOQUE_DISPONIVEL(TRUNC(PCEST.CODPROD, 2), TRUNC(PCEST.CODFILIAL, 2), 'V') AS "CUSTO EST."   
     , PRECO.PTABELA * PONTUAL.PKG_ESTOQUE.ESTOQUE_DISPONIVEL(TRUNC(PCEST.CODPROD, 2), TRUNC(PCEST.CODFILIAL, 2), 'V') AS "VALOR EST."
   , (NVL(PCEST.QTBLOQUEADA, 0) - NVL(PCEST.QTINDENIZ, 0)) QTBLOQMENOSAVARIA                                                         
   , TRUNC((NVL(PCEST.QTESTGER, 0) / DECODE(NVL(PCPRODUT.QTUNITCX, 1), 0, 1, NVL(PCPRODUT.QTUNITCX, 1))),0) || 'CX.' QTESTMASTER                       
     
FROM PONTUAL.PCEST                                                    
     , PONTUAL.PCPRODUT
     , PONTUAL.PCPRODFILIAL                                             
     , PONTUAL.PARAMETROS                                               
     , PONTUAL.LOGDESBLOQUEIO
     , preco                                      
WHERE PARAMETROS.CODFILIAL = PCEST.CODFILIAL                    
  AND PCPRODUT.CODPROD     = PCEST.CODPROD                      
  AND PCEST.CODFILIAL      = PCPRODFILIAL.CODFILIAL             
  AND PCEST.CODPROD        = PCPRODFILIAL.CODPROD               
  AND PCEST.CODFILIAL      = LOGDESBLOQUEIO.CODFILIAL(+)        
  AND PCEST.CODPROD        = LOGDESBLOQUEIO.CODPROD(+)        
  AND PCEST.CODPROD        = preco.codprod(+)
AND PCEST.CODFILIAL IN('3')                                                        
   AND (((PCPRODUT.OBS2 NOT IN ('FL')) OR (PCPRODUT.OBS2 IS NULL))                                                             
   AND ((PCPRODFILIAL.FORALINHA NOT IN ('S')) OR (PCPRODFILIAL.FORALINHA IS NULL)))                                            
  AND PCPRODUT.CODPROD NOT IN (14568)
  AND PCPRODUT.DESCRICAO NOT LIKE '%FREEZER%'
  AND PCPRODUT.DESCRICAO NOT LIKE '%PALLET%'
  AND PCPRODUT.DESCRICAO NOT LIKE '%PALET%'
  AND PCEST.DTULTENT IS NOT NULL

