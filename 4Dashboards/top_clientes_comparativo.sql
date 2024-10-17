WITH WINT AS 
(SELECT NVL(VENDAS.CODCLI,  DEVOLUCAO.CODCLI) CODCLI, 
       NVL(VENDAS.CLIENTE, DEVOLUCAO.CLIENTE) CLIENTE, 
       VENDAS.CODATIV CODATV1,
       NVL(VENDAS.RAMO, DEVOLUCAO.RAMO) RAMO,
       SUM(NVL(VENDAS.VLREPASSE,0) - NVL(DEVOLUCAO.VLREPASSE,0)) VLREPASSE,
       MAX(NVL(VENDAS.DESCRICAOPLANOCLI,DEVOLUCAO.DESCRICAOPLANOCLI)) DESCRICAOPLANOCLI,
       SUM(NVL(VENDAS.QTVENDA,0) - NVL(DEVOLUCAO.QTDEVOLUCAO,0)) QTVENDA,
       SUM(NVL(VENDAS.VLVENDA,0) - NVL(DEVOLUCAO.VLDEVOLUCAO,0)) VLVENDA,
       SUM(NVL(VENDAS.VLVENDA_SEMST,0) - NVL(DEVOLUCAO.VLDEVOLUCAO_SEMST,0)) VLVENDA_SEMST,
       SUM(NVL(DEVOLUCAO.VLDEVOLUCAO,0)) VLDEVOLUCAO,
       SUM(NVL(DEVOLUCAO.VLDEVOLUCAO_SEMST,0)) VLDEVOLUCAO_SEMST,
       SUM(NVL(VENDAS.TOTPESO,0) - NVL(DEVOLUCAO.TOTPESO,0) ) TOTPESO,
       SUM(NVL(VENDAS.VLBONIFIC,0)) - SUM(NVL(DEVOLUCAO.VLBONIFIC, 0)) VLBONIFIC,
       SUM(NVL(VENDAS.VOLUME,0) - NVL(DEVOLUCAO.VOLUME,0)) VOLUME, 
       (SUM(NVL(DEVOLUCAO.VLDEVOLUCAO, 0)) /(CASE WHEN (SUM(NVL(VENDAS.VLVENDA, 0)) = 0) THEN 1 ELSE SUM(NVL(VENDAS.VLVENDA, 0)) END)) * 100 VLTROCA, 
       (SUM(NVL(DEVOLUCAO.QTDEVOLUCAO, 0)) /(CASE WHEN (SUM(NVL(VENDAS.QTVENDA, 0)) = 0) THEN 1 ELSE SUM(NVL(VENDAS.QTVENDA, 0)) END)) * 100 QTTROCA, 
       SUM(NVL(VENDAS.LITRAGEM,0)   - NVL(DEVOLUCAO.LITRAGEM,0)) LITRAGEM,
       SUM(NVL(VENDAS.VLREPASSEBNF,0)   - NVL(DEVOLUCAO.VLREPASSEBNF,0)) VLREPASSEBNF 
FROM  (SELECT CODCLI,
              CLIENTE,
              CODATIV,
              RAMO,
              MAX(DESCRICAOPLANOCLI) DESCRICAOPLANOCLI,
              SUM(NVL(QTVENDA,0)) QTVENDA,
              SUM(NVL(VLVENDA,0) + NVL(VALORST,0) + NVL(VALORIPI,0) ) VLVENDA,
              SUM(NVL(VLVENDA_SEMST,0)) VLVENDA_SEMST,
              SUM(NVL(TOTPESO,0)) TOTPESO,
              SUM(NVL(VLBONIFIC,0)) VLBONIFIC,
              SUM(NVL(VOLUME,0)) VOLUME,
              SUM(NVL(VLREPASSE,0)) VLREPASSE,
              SUM(NVL(VLREPASSEBNF,0)) VLREPASSEBNF,
              SUM(NVL(LITRAGEM,0)) LITRAGEM FROM (  SELECT PCMOV.CODCLI, 
         PCATIVI.RAMO, 
         PCATIVI.CODATIV, 
       PCNFSAID.NUMTRANSVENDA, 
 PCNFSAID.CODUSUR  CODUSUR, 
 NVL(PCNFSAID.CODSUPERVISOR,PCSUPERV.CODSUPERVISOR)  CODSUPERVISOR, 
       PCMOV.CODPROD, 
       PCNFSAID.CODFILIAL, 
      PCPRODUT.CODAUXILIAR, 
       PCCLIENT.CLIENTE,
       PCFORNEC.CODFORNECPRINC,
     PCFORNEC.FORNECEDOR,
       PCFORNEC.CODFORNEC,
       PCUSUARI.NOME, 
       PCSUPERV.NOME SUPERV, 
       PCPRODUT.CODEPTO, 
       PCPRODUT.CODSEC, 
       PCDEPTO.DESCRICAO DEPARTAMENTO, 
       PCSECAO.DESCRICAO SECAO, 
       PCNFSAID.CODPRACA, 
       PCPRACA.PRACA, 
       PCPRODUT.CODMARCA, 
       PCPRODUT.QTUNIT, 
       PCMARCA.MARCA, 
       PCCLIENT.ESTENT, 
       PCCLIENT.MUNICENT,
       PCCLIENT.CODCIDADE,
       PCCIDADE.NOMECIDADE,
       NVL(PCCLIENT.CODCLIPRINC, PCCLIENT.CODCLI) CODCLIPRINC, 
       (SELECT X.CLIENTE 
          FROM PONTUAL.PCCLIENT X 
         WHERE X.CODCLI = NVL(PCCLIENT.CODCLIPRINC, PCCLIENT.CODCLI)) CLIENTEPRINC, 
       ROUND( (NVL(PCPRODUT.VOLUME, 0) * NVL(PCMOV.QT, 0)),2)  VOLUME, 
      (NVL(PCPRODUT.LITRAGEM, 0) * NVL(PCMOV.QT, 0))  LITRAGEM, 
       PCPRODUT.DESCRICAO,
       PCPRODUT.EMBALAGEM,
       PCPRODUT.UNIDADE,
       PCPRODUT.CODFAB,
       PCNFSAID.CODPLPAG,
       PCNFSAID.NUMPED,
       PCNFSAID.CODCOB,
       PCCLIENT.CODPLPAG CODPLANOCLI,
       PCPLPAG.DESCRICAO DESCRICAOPCPLPAG,
       PCPLPAG.NUMDIAS, 
       0 QTMETA,
       0 QTPESOMETA,
       0 MIXPREV,
       0 CLIPOSPREV,
       ROUND((DECODE(PCMOV.CODOPER,  
                     'SB',         
                     PCMOV.QTCONT,   
                     0)) *           
       NVL(PCMOV.VLREPASSE, 0),      
       2) VLREPASSEBNF,              
         ROUND((NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.VLIPI,0)))),2) VALORIPI,
                 0 VALORIPIX,
         ROUND(NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,(nvl(pcmov.ST,0)+NVL(PCMOVCOMPLE.VLSTTRANSFCD,0)))),2) VALORST,
                 0 VALORSTX,
         (SELECT PCCLIENT.CODPLPAG || ' - ' || PCPLPAG.DESCRICAO  FROM PONTUAL.PCPLPAG WHERE PCCLIENT.CODPLPAG = PCPLPAG.CODPLPAG) DESCRICAOPLANOCLI,
       ((DECODE(PCMOV.CODOPER,  
                           'S', 
                           (NVL(DECODE(PCNFSAID.CONDVENDA, 
                                       7, 
                                       PCMOV.QTCONT, 
                                       PCMOV.QT), 
                                0)), 
                           'SM', 
                           (NVL(DECODE(PCNFSAID.CONDVENDA, 
                                       7, 
                                       PCMOV.QTCONT, 
                                       PCMOV.QT), 
                                0)), 
                           'ST', 
                           (NVL(DECODE(PCNFSAID.CONDVENDA, 
                                       7, 
                                       PCMOV.QTCONT, 
                                       PCMOV.QT), 
                                0)), 
                           'SB', 
                           (NVL(DECODE(PCNFSAID.CONDVENDA, 
                                       7, 
                                       PCMOV.QTCONT, 
                                       PCMOV.QT), 
                                0)), 
                           0))) QTVENDA, 
                  ((DECODE(PCMOV.CODOPER                                
                          ,'S'                                        
                          ,(NVL(DECODE(PCNFSAID.CONDVENDA,              
                                       7,                               
                                       PCMOV.QTCONT,                    
                                       PCMOV.QT),                       
                                0))                                     
                          ,'ST'                                       
                          ,(NVL(DECODE(PCNFSAID.CONDVENDA,              
                                       7,                               
                                       PCMOV.QTCONT,                    
                                       PCMOV.QT),                       
                                0))                                     
                          ,'SM'                                       
                          ,(NVL(DECODE(PCNFSAID.CONDVENDA,              
                                       7,                               
                                       PCMOV.QTCONT,                    
                                       PCMOV.QT),                       
                                0))                                     
                          ,'SB'                                       
                          ,(NVL(DECODE(PCNFSAID.CONDVENDA,              
                                       7,                               
                                       PCMOV.QTCONT,                    
                                       PCMOV.QT),                       
                                0))                                     
                          ,0)) * (NVL(PCMOV.CUSTOFIN, 0)   
                          )) VLCUSTOFIN,  
 CASE WHEN NVL(PCMOVCOMPLE.VLSUBTOTITEM,0) <> 0 THEN  
  DECODE(NVL(PCMOV.TIPOITEM,'N'),'I',0,NVL(PCMOVCOMPLE.VLSUBTOTITEM,0) + (DECODE(NVL(PCMOV.TIPOITEM,'N'),'I', NVL(PCMOV.QTCONT, 0), 0) * NVL(PCMOV.VLFRETE, 0))) - 
       (  ROUND((NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.VLIPI,0)))),2)) -  
       (  ROUND(NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.ST,0))),2)) 
 ELSE                                                
       ROUND((((DECODE(PCMOV.CODOPER,                                           
                       'S',                                                   
                       (NVL(DECODE(PCNFSAID.CONDVENDA,                          
                                   7,                                           
                                   PCMOV.QTCONT,                                
                                   PCMOV.QT),                                   
                            0)),                                                
                       'ST',                                                  
                       (NVL(DECODE(PCNFSAID.CONDVENDA,                          
                                   7,                                           
                                   PCMOV.QTCONT,                                
                                   PCMOV.QT),                                   
                            0)),                                                
                       'SM',                                                  
                       (NVL(DECODE(PCNFSAID.CONDVENDA,                          
                                   7,                                           
                                   PCMOV.QTCONT,                                
                                   PCMOV.QT),                                   
                            0)),                                                
                       0)) *                                                    
             (NVL(DECODE(PCNFSAID.CONDVENDA,                                    
                           7,                                                   
                           (NVL(PUNITCONT, 0) - NVL(PCMOV.VLIPI, 0) -           
                           (nvl(pcmov.ST,0)+NVL(PCMOVCOMPLE.VLSTTRANSFCD,0))) + NVL(PCMOV.VLFRETE, 0) +          
                           NVL(PCMOV.VLOUTRASDESP, 0) +                         
                           NVL(PCMOV.VLFRETE_RATEIO, 0) +                       
                           DECODE(PCMOV.TIPOITEM,                               
                                  'C',                                        
                                  (SELECT NVL((SUM(M.QTCONT *                   
                                                   NVL(M.VLOUTROS, 0)) /        
                                          PCMOV.QT), 0) VLOUTROS                
                                     FROM PONTUAL.PCMOV M                               
                                    WHERE M.NUMTRANSVENDA =                     
                                          PCMOV.NUMTRANSVENDA                   
                                      AND M.TIPOITEM = 'I'                    
                                      AND CODPRODPRINC = PCMOV.CODPROD),        
 'I', NVL(PCMOV.VLOUTROS, 0),DECODE(NVL(PCNFSAID.SOMAREPASSEOUTRASDESPNF,'N'),'N',NVL((PCMOV.VLOUTROS), 0),'S',NVL((NVL(PCMOV.VLOUTROS,0)-NVL(PCMOV.VLREPASSE,0)), 0)))
                           ,(NVL(PCMOV.PUNIT, 0) - NVL(PCMOV.VLIPI, 0) -         
                           (nvl(pcmov.ST,0)+NVL(PCMOVCOMPLE.VLSTTRANSFCD,0))) + NVL(PCMOV.VLFRETE, 0) +          
                           NVL(PCMOV.VLOUTRASDESP, 0) +                         
                           NVL(PCMOV.VLFRETE_RATEIO, 0) +                       
                           DECODE(PCMOV.TIPOITEM,                               
                                  'C',                                        
                                  (SELECT NVL((SUM(M.QTCONT *                   
                                                   NVL(M.VLOUTROS, 0)) /        
                                          PCMOV.QT), 0) VLOUTROS                
                                     FROM PONTUAL.PCMOV M                               
                                    WHERE M.NUMTRANSVENDA =                     
                                          PCMOV.NUMTRANSVENDA                   
                                      AND M.TIPOITEM = 'I'                    
                                      AND CODPRODPRINC = PCMOV.CODPROD),        
 'I', NVL(PCMOV.VLOUTROS, 0), DECODE(NVL(PCNFSAID.SOMAREPASSEOUTRASDESPNF,'N'),'N',NVL((PCMOV.VLOUTROS), 0),'S',NVL((NVL(PCMOV.VLOUTROS,0)-NVL(PCMOV.VLREPASSE,0)), 0)))
                    ),0)))),                                                    
             2) END AS VLVENDA,                                                 
                                                                                
       (((DECODE(PCMOV.CODOPER,                                                 
                 'S',                                                         
                 (NVL(DECODE(PCNFSAID.CONDVENDA, 7, PCMOV.QTCONT, PCMOV.QT),    
                      0)),                                                      
                 'ST',                                                        
                 (NVL(DECODE(PCNFSAID.CONDVENDA, 7, PCMOV.QTCONT, PCMOV.QT),    
                      0)),                                                      
                 'SM',                                                        
                 (NVL(DECODE(PCNFSAID.CONDVENDA, 7, PCMOV.QTCONT, PCMOV.QT),    
                      0)),                                                      
                 0)) *                                                          
       (NVL(DECODE(PCNFSAID.CONDVENDA,                                          
                     7,                                                         
                     PCMOV.PUNITCONT,                                           
                     NVL(PCMOV.PUNIT, 0) + NVL(PCMOV.VLFRETE, 0) +              
                     NVL(PCMOV.VLOUTRASDESP, 0) +                               
                     NVL(PCMOV.VLFRETE_RATEIO, 0) +                             
                     DECODE(PCMOV.TIPOITEM,                                     
                            'C',                                              
                            (SELECT (SUM(M.QTCONT * NVL(M.VLOUTROS, 0)) /       
                                    PCMOV.QT) VLOUTROS                          
                               FROM PONTUAL.PCMOV M                                     
                              WHERE M.NUMTRANSVENDA = PCMOV.NUMTRANSVENDA       
                                AND M.TIPOITEM = 'I'                          
                                AND CODPRODPRINC = PCMOV.CODPROD),              
 'I', NVL(PCMOV.VLOUTROS, 0), DECODE(NVL(PCNFSAID.SOMAREPASSEOUTRASDESPNF,'N'),'N',NVL((PCMOV.VLOUTROS), 0),'S',NVL((NVL(PCMOV.VLOUTROS,0)-NVL(PCMOV.VLREPASSE,0)), 0)))
                      - (nvl(pcmov.ST,0)+NVL(PCMOVCOMPLE.VLSTTRANSFCD,0))),               
              0)))) VLVENDA_SEMST,                                              
      ROUND(    (NVL(PCMOV.QT, 0) *(
       DECODE(PCNFSAID.CONDVENDA,
               5,
               DECODE(PCMOV.PBONIFIC, NULL, PCMOV.PTABELA, PCMOV.PBONIFIC)
               ,6, --- aqui
               DECODE(PCMOV.PBONIFIC, NULL, PCMOV.PTABELA, PCMOV.PBONIFIC),
               1,
               NVL(PCMOV.PBONIFIC,0),                                      
               14,
               NVL(PCMOV.PBONIFIC,0),                                      
               12,
               DECODE(PCMOV.PBONIFIC, NULL, PCMOV.PTABELA, PCMOV.PBONIFIC),
               0)) 
),2) VLBONIFIC,
               ((DECODE(PCMOV.CODOPER,
                           'S',
                           (NVL(DECODE(PCNFSAID.CONDVENDA,
                                       7,
                                       PCMOV.QTCONT,
                                       PCMOV.QT),
                                0)),
                           'ST',
                           (NVL(DECODE(PCNFSAID.CONDVENDA,
                                       7,
                                       PCMOV.QTCONT,
                                       PCMOV.QT),
                                0)),
                           'SM',
                           (NVL(DECODE(PCNFSAID.CONDVENDA,
                                       7,
                                       PCMOV.QTCONT,
                                       PCMOV.QT),
                                0)),
                           0))) QTVENDIDA,
       ROUND( (NVL(PCPRODUT.PESOBRUTO,PCMOV.PESOBRUTO) * NVL(PCMOV.QT, 0)),2) AS TOTPESO,
       ROUND(PCMOV.QT * (PCMOV.PTABELA
                       + NVL (pcmov.vlfrete, 0) + NVL (pcmov.vloutrasdesp, 0) + NVL (pcmov.vlfrete_rateio, 0) + NVL (pcmov.vloutros, 0) 
  ),2) VLTABELA,
       PCMOV.CODCLI QTCLIPOS,
       PCNFSAID.NUMTRANSVENDA QTNUMTRANSVENDA, 
      (SELECT PCFILIAL.FANTASIA 
              FROM PONTUAL.PCFILIAL  
             WHERE PCFILIAL.CODIGO = PCNFSAID.CODFILIAL AND ROWNUM = 1) FILIAL,
       PCPRODUT.CODPROD AS QTMIXCAD,
       PCMOV.CODPROD AS QTMIX, 
   (SELECT COUNT(*) FROM PONTUAL.PCPRODUT P
WHERE P.CODFORNEC = PCFORNEC.CODFORNEC AND NVL(P.REVENDA,'S')  = 'S' ) QTMIXCADNOVO,
 PCGERENTE.NOMEGERENTE,
 DECODE(PCNFSAID.CODGERENTE,NULL,PCSUPERV.CODGERENTE,PCNFSAID.CODGERENTE) CODGERENTE, 
 PCPRACA.ROTA,
 PCROTAEXP.DESCRICAO DESCROTA,
               (NVL(PCMOV.VLREPASSE,0) * DECODE(PCNFSAID.CONDVENDA,
              5,0,6,0,0,12,0,DECODE(PCMOV.CODOPER,'SB',0,NVL(PCMOV.QT, 0)) ))  AS VLREPASSE
  FROM PONTUAL.PCNFSAID,
       PONTUAL.PCPRODUT,
       PONTUAL.PCMOV,
       PONTUAL.PCCLIENT,
       PONTUAL.PCUSUARI,
       PONTUAL.PCSUPERV,
       PONTUAL.PCPLPAG,
       PONTUAL.PCFORNEC,
       PONTUAL.PCATIVI, 
       PONTUAL.PCPRACA,
       PONTUAL.PCDEPTO,
       PONTUAL.PCSECAO,
       PONTUAL.PCPEDC,
       PONTUAL.PCGERENTE,
       PONTUAL.PCCIDADE,
       PONTUAL.PCMARCA,
       PONTUAL.PCROTAEXP,
       PONTUAL.PCMOVCOMPLE
 WHERE PCMOV.NUMTRANSVENDA = PCNFSAID.NUMTRANSVENDA
   AND PCMOV.CODFILIAL = PCNFSAID.CODFILIAL 
   AND PCMOV.DTMOV BETWEEN  SYSDATE - INTERVAL '1' YEAR - 60 AND SYSDATE - INTERVAL '1' YEAR
   AND PCMOV.CODPROD = PCPRODUT.CODPROD
   AND PCNFSAID.CODPRACA = PCPRACA.CODPRACA(+)
   AND PCATIVI.CODATIV(+) = PCCLIENT.CODATV1
   AND PCMOV.CODCLI = PCCLIENT.CODCLI
   AND PCFORNEC.CODFORNEC = PCPRODUT.CODFORNEC
   AND  PCNFSAID.CODUSUR   = PCUSUARI.CODUSUR 
   AND PCPRACA.ROTA = PCROTAEXP.CODROTA(+)
   AND PCMOV.NUMTRANSITEM = PCMOVCOMPLE.NUMTRANSITEM(+)
   AND PCPRODUT.CODMARCA = PCMARCA.CODMARCA(+)
   AND PCCLIENT.CODCIDADE = PCCIDADE.CODCIDADE(+)
  AND PCMOV.CODOPER <> 'SR' 
  AND NVL(PCNFSAID.TIPOVENDA,'X') NOT IN ('SR', 'DF')
  AND PCMOV.CODOPER <> 'SO' 
   AND  NVL(PCNFSAID.CODSUPERVISOR,PCSUPERV.CODSUPERVISOR)   = PCSUPERV.CODSUPERVISOR
   AND PCNFSAID.CODPLPAG = PCPLPAG.CODPLPAG
   AND PCNFSAID.NUMPED = PCPEDC.NUMPED(+)
   AND PCPRODUT.CODEPTO = PCDEPTO.CODEPTO(+)
   AND PCPRODUT.CODSEC = PCSECAO.CODSEC(+)
   AND DECODE(PCNFSAID.CODGERENTE,NULL,PCSUPERV.CODGERENTE,PCNFSAID.CODGERENTE) = PCGERENTE.CODGERENTE 
   AND PCNFSAID.CODFISCAL NOT IN (522, 622, 722, 532, 632, 732)
   AND PCNFSAID.CONDVENDA NOT IN (4, 8, 10, 13, 20, 98, 99, 11)
   AND (PCNFSAID.DTCANCEL IS NULL)
       AND PCPRODUT.CODSEC IN ('1005','120387','10040','10042','120239','120424','10047','10046','10048','11007','10041','10044','1003','10001','1023','10050','{impulso}','{takehome}','{acai}') --seção
 AND  NVL(PCNFSAID.CODSUPERVISOR,PCSUPERV.CODSUPERVISOR) {supOffOn} ('{sup}')
   AND PCNFSAID.DTSAIDA BETWEEN  SYSDATE - INTERVAL '1' YEAR - 60 AND SYSDATE - INTERVAL '1' YEAR
           AND PCMOV.CODFILIAL IN('3')
           AND PCNFSAID.CODFILIAL IN('3')
)
        GROUP BY CODCLI,
              CLIENTE,
              CODATIV,
              RAMO) VENDAS, 
      
      ( SELECT CODCLI, CLIENTE, RAMO,
               MAX(DESCRICAOPLANOCLI) DESCRICAOPLANOCLI,
               SUM(NVL(QTDEVOLUCAO,0)) QTDEVOLUCAO,
               SUM(NVL(VLDEVOLUCAO,0)) VLDEVOLUCAO,
               SUM(NVL(VLDEVOLUCAO_SEMST,0)) VLDEVOLUCAO_SEMST,
               SUM(NVL(TOTPESO,0)) TOTPESO,
               SUM(NVL(VOLUME,0)) VOLUME,
               SUM(NVL(VLBONIFIC,0)) VLBONIFIC, 
               SUM(NVL(VLREPASSE,0)) VLREPASSE,
               SUM(NVL(VLREPASSEBNF,0)) VLREPASSEBNF,
   SUM(NVL(LITRAGEM,0)) LITRAGEM FROM  (SELECT PCFORNEC.CODFORNEC, 
       PCFORNEC.FORNECEDOR, 
       PCFORNEC.CODFORNECPRINC,
      (SELECT A.FORNECEDOR FROM PONTUAL.PCFORNEC A WHERE A.CODFORNEC = PCFORNEC.CODFORNECPRINC) FORNECEDORPRINC,
       PCNFENT.CODFORNEC CODCLI,
       PCCLIENT.CODATV1,
       DECODE(NVL(PCPEDC.NUMCAIXA,0),0,0,NVL(PCPEDC.NUMCAIXA,0)) CAIXA,
       PCNFENT.NUMNOTA ,
       PCNFENT.CODDEVOL,
       NVL(PCNFENT.VLOUTRAS,0) VLOUTRAS,
       NVL(PCNFENT.VLFRETE,0) VLFRETE,
       PCNFENT.CODFILIAL ,
       PCNFENT.CODMOTORISTADEVOL,
    (SELECT X.CLIENTE 
       FROM PONTUAL.PCCLIENT X
      WHERE X.CODCLI = NVL(PCCLIENT.CODCLIPRINC, PCCLIENT.CODCLI)) CLIENTEPRINC,
       (SELECT DISTINCT PCEMPR.NOME  
          FROM PONTUAL.PCEMPR                
         WHERE PCEMPR.MATRICULA = PCNFENT.CODMOTORISTADEVOL) NOMEMOTORISTA,
       PCNFENT.DTENT,
       PCNFENT.NUMTRANSENT,
       PCESTCOM.NUMTRANSVENDA, 
       PCEMPR.NOME NOMEFUNC,
       PCTABDEV.MOTIVO,
       PCCLIENT.CLIENTE,
       PCCLIENT.CODCIDADE,
       PCCIDADE.NOMECIDADE,
       PCMOV.CUSTOFIN,
       PCMOV.CODDEVOL DEVOLITEM,
       PCTABDEV2.MOTIVO MOTIVO2,
       PCCLIENT.ESTENT,
       PCCLIENT.MUNICENT,
       PCCLIENT.VIP,
       PCESTCOM.VLESTORNO,
       PCNFENT.OBS,
       PCMOV.CODOPER,
       PCMOV.ST,
       (DECODE(PCNFSAID.CONDVENDA,7,NVL(PCMOV.PUNITCONT,0),NVL(PCMOV.PUNIT,0))) PUNIT,
       PCPRODUT.DESCRICAO,
       PCPRODUT.CODAUXILIAR,
       PCPRODUT.EMBALAGEM,
       PCPRODUT.UNIDADE,
       PCMOV.CODPROD,
       NVL(PCPRODUT.QTUNIT,0) QTUNIT, 
       PCPRODUT.CODEPTO, 
       PCPRODUT.CODSEC, 
       PCPRODUT.CODFAB, 
       PCUSUARI.PERCENT, 
       PCUSUARI.PERCENT2, 
       PCDEPTO.DESCRICAO DEPARTAMENTO, 
       PCSECAO.DESCRICAO SECAO, 
 NVL(PCNFSAID.CODSUPERVISOR,PCSUPERV.CODSUPERVISOR)  CODSUPERVISOR, 
       PCMARCA.MARCA,
       PCATIVI.CODATIV,
       PCATIVI.RAMO,
       PCPRACA.CODPRACA, 
       DECODE(PCMOV.NUMREGIAO, NULL, PCPRACA.NUMREGIAO, PCMOV.NUMREGIAO) NUMREGIAO, 
       PCPRACA.ROTA, 
       PCPRACA.PRACA, 
       0 QTMETA,
       0 QTPESOMETA,
       0 MIXPREV,
       0 CLIPOSPREV,
       NVL(PCNFSAID.CODPLPAG,PCCLIENT.CODPLPAG) CODPLPAG, 
       PCNFSAID.NUMPED,
       PCNFSAID.CODCOB,
       PCNFSAID.CONDVENDA,
       PCNFSAID.PRAZOMEDIO,
       PCNFSAID.CODEMITENTE,
       PCPLPAG.DESCRICAO DESCRICAOPCPLPAG,
       NVL(PCPLPAG.NUMDIAS,0) NUMDIAS,
       PCUSUARI.NOME,
       PCNFENT.VLST,
       PCSUPERV.NOME AS SUPERV,
       ROUND(DECODE(PCNFSAID.CONDVENDA,                      
                    5,                                       
                    0,                        
                    DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'),  
                           'N',                            
                           NVL(PCMOV.QT, 0),                 
                           0)) * NVL(PCMOV.VLREPASSE, 0),    
                2) VLREPASSE,                                
       ROUND(DECODE(PCNFSAID.CONDVENDA,                      
                    5,                                       
                    NVL(PCMOV.QT, 0),                        
                    DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'),  
                           'N',                            
                           0,                                
                           NVL(PCMOV.QT, 0),                 
                           0)) * NVL(PCMOV.VLREPASSE, 0),    
                2) VLREPASSEBNF,                             
       0 VLVENDA, 
       0 QTBONIFIC,
      (SELECT PCFILIAL.FANTASIA 
              FROM PONTUAL.PCNFENT P, PONTUAL.PCFILIAL  
             WHERE P.CODFILIAL = PCFILIAL.CODIGO 
               AND P.NUMTRANSENT = PCNFENT.NUMTRANSENT  AND ROWNUM = 1) FILIAL,
 (NVL(PCMOV.QT,0)) QT,        
     (NVL(PCMOV.QT,0)) QTDEVOLUCAO,
 CASE WHEN NVL(PCMOVCOMPLE.VLSUBTOTITEM,0) <> 0 THEN  
  NVL(PCMOVCOMPLE.VLSUBTOTITEM,0) -                  
       (  ROUND((NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.VLIPI,0)))),2)) -  
       (  ROUND(NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.ST,0))),2)) 
 ELSE                                                
  (DECODE(PCNFSAID.CONDVENDA, 5, 0, DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'), 'N', NVL(PCMOV.QT, 0), 0)) * 
  DECODE(PCNFSAID.CONDVENDA,                                                    
          5,                                                                    
          0,                                                                    
          6,                                                                    
          0,                                                                                                                                    
          0,                                                                    
          (DECODE(PCMOV.PUNIT,                                                  
                  0,                                                            
                  PCMOV.PUNITCONT,                                              
                  NULL,                                                         
                  PCMOV.PUNITCONT,                                              
                  PCMOV.PUNIT) + NVL(PCMOV.VLFRETE, 0) +                        
          NVL(PCMOV.VLOUTRASDESP, 0) + NVL(PCMOV.VLFRETE_RATEIO, 0)             
  - (decode(NVL(PCNFSAID.SOMAREPASSEOUTRASDESPNF,'N'),'N', (DECODE(NVL(PCMOV.VLOUTROS,0),0,NVL(PCMOV.VLREPASSE,0),0)),'S',(NVL(PCMOV.VLREPASSE,0)))) 
          + NVL(PCMOV.VLOUTROS, 0)))) END AS VLDEVOLUCAO,                          
  (DECODE(PCNFSAID.CONDVENDA, 5, 0, DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'), 'N', NVL(PCMOV.QT, 0), 0)) * 
  DECODE(PCNFSAID.CONDVENDA,                                                    
          5,                                                                    
          0,                                                                    
          6,                                                                    
          0,                                                            
          0,                                                                    
          (nvl(PCMOV.ST,0) + NVL(PCMOVCOMPLE.VLSTTRANSFCD,0)) )) VALORST,                                          
          0 VALORSTX,                                                          
  (DECODE(PCNFSAID.CONDVENDA, 5, 0, DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'), 'N', NVL(PCMOV.QT, 0), 0)) * 
  DECODE(PCNFSAID.CONDVENDA,                                                    
          5,                                                                    
          0,                                                                    
          6,                                                                    
          0,                                                                                                                                   
          0,                                                                    
          nvl(PCMOV.VLIPI,0) )) VALORIPI,                                          
          0 VALORIPIX,                                                          
  (NVL(PCMOV.QT, 0) *                                                           
  DECODE(PCNFSAID.CONDVENDA,                                                    
          5,                                                                    
          0,                                                                    
          6,                                                                    
          0,                                                                                                                                     
          0,                                                                    
          (DECODE(PCMOV.PUNIT,                                                  
                  0,                                                            
                  PCMOV.PUNITCONT,                                              
                  NULL,                                                         
                  PCMOV.PUNITCONT,                                              
                  PCMOV.PUNIT) + NVL(PCMOV.VLOUTROS, 0) -                       
          (NVL(PCMOV.ST,0) + NVL(PCMOVCOMPLE.VLSTTRANSFCD,0)) + NVL(PCMOV.VLFRETE, 0)))) VLDEVOLUCAO_SEMST,        
  (NVL(PCMOV.QT, 0) *                                                           
  (DECODE(PCNFSAID.CONDVENDA,                                                   
          5,                                                                    
          NVL(PCMOV.PUNITCONT, 0),                                              
          0) + NVL(PCMOV.VLOUTROS, 0) +                                         
               NVL(PCMOV.VLFRETE, 0))) VLDEVOLUCAOBNF,                          
  (NVL(PCMOV.QT, 0) *                                                           
  (DECODE(PCNFSAID.CONDVENDA,                                                   
           5,                                                                   
           NVL(PCMOV.PUNITCONT, 0),                                             
           6, --aqui                                                                                                        
           NVL(PCMOV.PUNITCONT, 0),                                             
           12,                                                                  
           NVL(PCMOV.PUNITCONT, 0),                                             
           0) + DECODE(PCNFSAID.CONDVENDA,                                      
                         5,                                                     
                         NVL(PCMOV.VLOUTROS, 0),                                
                         6,                                                                                                      
                         NVL(PCMOV.VLOUTROS, 0),                                
                         12,                                                    
                         NVL(PCMOV.VLOUTROS, 0)) +                              
  DECODE(PCNFSAID.CONDVENDA,                                                    
           5,                                                                   
           NVL(PCMOV.VLFRETE, 0),                                               
           6,                                                                                                                                    
           NVL(PCMOV.VLFRETE, 0),                                               
           12,                                                                  
           NVL(PCMOV.VLFRETE, 0)))) VLDEVOLUCAOBONI,                            
  (NVL(PCMOV.QT, 0) * NVL(PCMOV.CUSTOFIN, 0)) VLCMVDEVOL,                       
  (NVL(PCMOV.QT, 0) * (NVL(PCMOV.CUSTOFIN, 0)                                   
   )) VLCUSTOFIN,                                                               
  (NVL(PCPRODUT.LITRAGEM, 0) * NVL(PCMOV.QT, 0)) LITRAGEM,                      
  (NVL(PCPRODUT.VOLUME, 0) * NVL(PCMOV.QT, 0)) VOLUME,                          
  (DECODE(PCMOV.PBASERCA,                                                       
          NULL,                                                                 
          NVL(PCMOV.PBASERCA, NVL(PCMOV.PTABELA, 0)),                           
          NVL(PCMOV.PTABELA, 0)) * NVL(PCMOV.QT, 0)) DEVOLTAB,                  
  (NVL(PCPRODUT.PESOBRUTO,PCMOV.PESOBRUTO) * NVL(PCMOV.QT, 0)) AS TOTPESO,     
  
  ROUND((NVL(PCMOV.QT, 0) *                                                     
        DECODE(PCNFSAID.CONDVENDA,                                              
                5,                                                              
                DECODE(PCMOV.PBONIFIC,                                          
                       NULL,                                                    
                       PCMOV.PTABELA,                                           
                       PCMOV.PBONIFIC) /*+ NVL(PCMOV.VLFRETE, 0)*/ +                
                NVL(PCMOV.VLOUTRASDESP, 0) +                                    
                NVL(PCMOV.VLFRETE_RATEIO, 0) + NVL(PCMOV.VLOUTROS, 0)           
                ,6,                                                             
                DECODE(PCMOV.PBONIFIC,                                          
                       NULL,                                                    
                       PCMOV.PTABELA,                                           
                       PCMOV.PBONIFIC),                                         
                1,                                                              
                NVL(PCMOV.PBONIFIC,0),                                           
                14,                                                                                                                      
                DECODE(PCMOV.PBONIFIC,                                          
                       NULL,                                                    
                       PCMOV.PTABELA,                                           
                       PCMOV.PBONIFIC),                                         
                12,                                                             
                DECODE(PCMOV.PBONIFIC,                                          
                       NULL,                                                    
                       PCMOV.PTABELA,                                           
                       PCMOV.PBONIFIC),                                         
                0)                                                              
        ),2) VLBONIFIC,                                                        

       NVL(PCCLIENT.CODCLIPRINC,PCCLIENT.CODCLI) CODCLIPRINC,  
 PCNFENT.CODUSURDEVOL  CODUSUR, 
 PCNFENT.CODUSURDEVOL  CODUSURDEVOL, 
       CASE WHEN  (  SELECT SUM ( NVL(PCMOV.QT, 0) * (NVL(PCMOV.PUNIT, 0) + NVL(PCMOV.VLOUTROS, 0)) ) FROM PONTUAL.PCMOV M, PONTUAL.PCESTCOM E, PONTUAL.PCNFENT  F
         WHERE E.NUMTRANSENT = F.NUMTRANSENT AND M.NUMTRANSENT = F.NUMTRANSENT
         AND M.CODOPER = 'ED' AND M.DTCANCEL IS NULL
         AND PCNFSAID.NUMTRANSVENDA = E.NUMTRANSVENDA )  >= NVL(PCNFSAID.VLTOTAL,0) THEN
            PCFORNEC.CODFORNEC 
            ELSE
            0 END DEVOLVIDO, 
      (SELECT PCCLIENT.CODPLPAG || ' - ' || PCPLPAG.DESCRICAO  FROM PONTUAL.PCPLPAG WHERE PCCLIENT.CODPLPAG = PCPLPAG.CODPLPAG) DESCRICAOPLANOCLI,
      PCGERENTE.NOMEGERENTE,
      DECODE(PCNFSAID.CODGERENTE,NULL,PCSUPERV.CODGERENTE,PCNFSAID.CODGERENTE) CODGERENTE  
      , PCROTAEXP.DESCRICAO DESCROTA
  FROM PONTUAL.PCNFENT, PONTUAL.PCESTCOM, PONTUAL.PCEMPR, PONTUAL.PCNFSAID, PONTUAL.PCMOV, PONTUAL.PCPRODUT, PONTUAL.PCCLIENT, PONTUAL.PCFORNEC, PONTUAL.PCPRACA, PONTUAL.PCTABDEV, PONTUAL.PCTABDEV PCTABDEV2, 
       PONTUAL.PCDEPTO, PONTUAL.PCSECAO, PONTUAL.PCUSUARI, PONTUAL.PCPLPAG, PONTUAL.PCSUPERV, PONTUAL.PCATIVI, PONTUAL.PCPEDC, PONTUAL.PCCIDADE, PONTUAL.PCMARCA, PONTUAL.PCGERENTE, PONTUAL.PCMOVCOMPLE,PONTUAL.PCROTAEXP 
 ,(SELECT DISTINCT CASE                                          
            WHEN PED.CONDVENDA = 7 THEN                          
             (SELECT DISTINCT P1.NUMPED                          
                FROM PONTUAL.PCPEDC P1, PONTUAL.PCESTCOM E1                      
               WHERE E1.NUMTRANSENT = ESTC.NUMTRANSENT           
                 AND P1.NUMTRANSVENDA = E1.NUMTRANSVENDA         
                 AND P1.NUMPEDENTFUT = PED.NUMPED                
                 AND P1.CONDVENDA = 8)                           
            WHEN PED.CONDVENDA = 8 THEN                          
             (SELECT DISTINCT P2.NUMPED                          
                FROM PONTUAL.PCPEDC P2, PONTUAL.PCESTCOM E2                      
               WHERE E2.NUMTRANSENT = ESTC.NUMTRANSENT           
                 AND P2.NUMTRANSVENDA = E2.NUMTRANSVENDA         
                 AND P2.NUMPED = PED.NUMPEDENTFUT                
                 AND P2.CONDVENDA = 7)                           
          END TEMVENDATV8,                                       
          PED.NUMTRANSVENDA,                                     
          ESTC.NUMTRANSENT                                       
     FROM PONTUAL.PCPEDC PED, PONTUAL.PCESTCOM ESTC                              
    WHERE PED.NUMTRANSVENDA(+) = ESTC.NUMTRANSVENDA
   AND PED.DATA BETWEEN  SYSDATE - INTERVAL '1' YEAR - 60 AND SYSDATE - INTERVAL '1' YEAR
      ) TEMVENDATV8 
 WHERE PCNFENT.NUMTRANSENT = PCESTCOM.NUMTRANSENT
   AND PCCLIENT.CODPRACA = PCPRACA.CODPRACA
   AND PCESTCOM.NUMTRANSENT = PCMOV.NUMTRANSENT
   AND PCFORNEC.CODFORNEC = PCPRODUT.CODFORNEC
   AND PCNFSAID.NUMPED  = PCPEDC.NUMPED(+)
   AND PCNFENT.CODDEVOL = PCTABDEV.CODDEVOL(+)
   AND PCMOV.CODDEVOL = PCTABDEV2.CODDEVOL(+)
   AND PCPRODUT.CODEPTO = PCDEPTO.CODEPTO(+)
   AND PCPRACA.ROTA = PCROTAEXP.CODROTA(+)
AND PCNFENT.CODUSURDEVOL = PCUSUARI.CODUSUR(+)
AND NVL(PCNFSAID.CODSUPERVISOR,PCUSUARI.CODSUPERVISOR) = PCSUPERV.CODSUPERVISOR
   AND PCPRODUT.CODSEC = PCSECAO.CODSEC(+)
   AND PCCLIENT.CODATV1 = PCATIVI.CODATIV(+)
   AND PCNFENT.CODFUNCLANC  = PCEMPR.MATRICULA(+)
   AND PCESTCOM.NUMTRANSVENDA = PCNFSAID.NUMTRANSVENDA(+)
   AND PCCLIENT.CODCIDADE = PCCIDADE.CODCIDADE(+)
   AND NVL(PCNFSAID.CODPLPAG,PCCLIENT.CODPLPAG) = PCPLPAG.CODPLPAG
   AND PCPRODUT.CODMARCA = PCMARCA.CODMARCA(+)
   AND PCMOV.NUMTRANSITEM = PCMOVCOMPLE.NUMTRANSITEM(+)
 AND DECODE(PCNFSAID.CODGERENTE,NULL,PCSUPERV.CODGERENTE,PCNFSAID.CODGERENTE) = PCGERENTE.CODGERENTE
      -- numtransvenda = 0 refere-se a devolucoes avulsas que nao
      -- devem ser incluidas no resumo de faturamento
   AND PCMOV.CODPROD = PCPRODUT.CODPROD
   AND PCNFENT.CODFORNEC = PCCLIENT.CODCLI 
   AND PCNFENT.TIPODESCARGA IN ('6', '7', 'T')
   AND NVL(PCNFENT.CODFISCAL,0) IN (131, 132, 231, 232, 199, 299)
   AND PCMOV.DTCANCEL IS NULL
   AND PCMOV.CODOPER = 'ED' 
   AND NVL(PCNFENT.TIPOMOVGARANTIA, -1) = -1
   AND NVL(PCNFENT.OBS, 'X') <> 'NF CANCELADA'
    AND TEMVENDATV8.NUMTRANSENT(+) = PCNFENT.NUMTRANSENT       
          AND NVL(PCNFSAID.CONDVENDA, 0) NOT IN (4, 8, 10, 13, 20, 98, 99, 11)
   AND PCNFENT.DTENT BETWEEN  SYSDATE - INTERVAL '1' YEAR - 60 AND SYSDATE - INTERVAL '1' YEAR


       AND PCPRODUT.CODSEC IN ('1005','120387','10040','10042','120239','120424','10047','10046','10048','11007','10041','10044','1003','10001','1023','10050','{impulso}','{takehome}','{acai}') --seção
           AND PCMOV.CODFILIAL IN('3')
           AND PCNFENT.CODFILIAL IN('3')
   AND PCNFENT.DTENT BETWEEN  SYSDATE - INTERVAL '1' YEAR - 60 AND SYSDATE - INTERVAL '1' YEAR
   AND PCMOV.DTMOV BETWEEN  SYSDATE - INTERVAL '1' YEAR - 60 AND SYSDATE - INTERVAL '1' YEAR
AND  NVL(PCNFSAID.CODSUPERVISOR,PCSUPERV.CODSUPERVISOR) {supOffOn} ('{sup}')
)

        GROUP BY CODCLI, CLIENTE, RAMO) DEVOLUCAO,
     PONTUAL.PCCLIENT
WHERE PCCLIENT.CODCLI = VENDAS.CODCLI(+)
  AND PCCLIENT.CODCLI = DEVOLUCAO.CODCLI(+)
  AND ( ( NVL(VENDAS.QTVENDA,0) <> 0) or  ( NVL(DEVOLUCAO.QTDEVOLUCAO,0) <> 0) or  ( NVL(DEVOLUCAO.VLDEVOLUCAO,0) <> 0) OR (NVL(VENDAS.TOTPESO,0) <> 0)  OR 
      (NVL(VENDAS.VLVENDA,0) <> 0) OR  ( NVL(DEVOLUCAO.LITRAGEM,0) <> 0) OR (NVL(VENDAS.VLBONIFIC,0) <> 0)  OR (NVL(VENDAS.CODCLI,0) <> 0)) 
GROUP BY VENDAS.CODCLI,
       VENDAS.CLIENTE,
       DEVOLUCAO.CODCLI,
       DEVOLUCAO.CLIENTE,
       DEVOLUCAO.RAMO,
       VENDAS.CODATIV,
       VENDAS.RAMO 
ORDER BY VLVENDA DESC),

USUR_CLI AS (
    SELECT 
    usur.codsupervisor,
    USUR.CODUSUR,
    SUBSTR(USUR.NOME, INSTR(USUR.NOME, ' ') + 1, INSTR(USUR.NOME, ' ', INSTR(USUR.NOME, ' ') + 1) - INSTR(USUR.NOME, ' ') - 1) AS RCA, -- EXTRAI O NOME
    C.CODCLI, 
    C.CLIENTE
FROM
    PONTUAL.PCUSUARI USUR
LEFT JOIN 
    PONTUAL.PCCLIENT C ON USUR.CODUSUR = C.CODUSUR1
WHERE
    USUR.NOME LIKE 'PMU%'
)
---------------------------------------------------------------------------------------------------------------------------------------

SELECT
        RANK() OVER (ORDER BY W.VLVENDA DESC) AS "RANK",
        W.CODCLI codcli,
        SUBSTR(W.CLIENTE,0,28) AS CLIENTE, 
        UC.RCA VENDEDOR,
        W.VLVENDA AS FATURADO
FROM
        WINT W
LEFT JOIN  
        USUR_CLI UC ON UC.CODCLI = W.CODCLI
