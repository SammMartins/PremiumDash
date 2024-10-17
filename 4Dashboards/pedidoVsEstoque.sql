SELECT Distinct(a.CODPROD) || '' codprod, c.descricao, 
       '' || SUM(a.QT) "Itens Pedidos", 
       '' || (b.qtest - b.qtreserv) "QT. Estoque", 
       '' || SUM(a.QT) - (b.qtest - b.qtreserv) as "Corte Previsto"
from pontual.pcpedi a
    JOIN pontual.PCest b on a.codprod = b.codprod
    join pontual.pcprodut c on a.codprod = c.codprod
WHERE a.DATA > SYSDATE - 5
    AND a.posicao in ('B','P')
    AND (a.QT - (b.qtest - b.qtreserv)) > 0
    --AND a.codprod = 18443
    AND a.posicao in ('B','P')
    and b.codfilial = 3
group by a.codprod,c.descricao,b.qtest,b.qtreserv
ORDER BY "Corte Previsto" DESC