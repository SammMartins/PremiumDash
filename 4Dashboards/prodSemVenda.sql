WITH DATAVENDA AS 
(
    SELECT MAX(c.DATA) data, c.CODPROD
        FROM PONTUAL.PCPEDI C 
    WHERE c.DATA BETWEEN SYSDATE - 240 AND SYSDATE 
    GROUP BY c.CODPROD
),
PRECO AS
(
    SELECT p.codprod, MAX(p.pvenda) valor FROM PONTUAL.PCPRECO p GROUP BY p.codprod
)
 
SELECT a.CODPROD || '', a.DESCRICAO "DESCRIÇÃO",
       TO_CHAR(b.dtultent, 'DD/MM/YY') "DTULTENT",
       b.qtultent || '' "QTDULTENT",
       (b.qtest - b.qtreserv) || '' "Estoque",
       TRUNC(sysdate - c.data, 0) || ' Dias (' || TO_CHAR(c.data, 'DD/MM/YY') || ')' "Dias sem Venda"
       --,TRUNC(p.valor * (b.qtest - b.qtreserv),2) "Valor Aproximado perda em vendas"
       
FROM PONTUAL.PCPRODUT a
JOIN PONTUAL.PCest b ON a.codprod = b.codprod
JOIN DATAVENDA c ON a.codprod = c.codprod
JOIN PRECO p on a.codprod = p.codprod

WHERE c.data < SYSDATE - 7
    AND (b.qtest - b.qtreserv) > 0
    AND a.codfornec = {fornec}
    AND b.codfilial = 3
ORDER BY "Estoque" DESC