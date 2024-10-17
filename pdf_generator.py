from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import base64
from typing import Final

from utils_pdf import regua, reticula

def flash_pdf(df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = letter

    c.drawString(50, 810, 'x50')
    c.drawString(100, 810, 'x100')
    c.drawString(150, 810, 'x150')
    c.drawString(200, 810, 'x200')
    c.drawString(250, 810, 'x250')
    c.drawString(300, 810, 'x300')
    c.drawString(350, 810, 'x350')
    c.drawString(400, 810, 'x400')
    c.drawString(450, 810, 'x450')
    c.drawString(500, 810, 'x500')
    c.drawString(550, 810, 'x550')
    c.drawString(600, 810, 'x600')
    c.drawString(650, 810, 'x650')
    c.drawString(700, 810, 'x700')
    c.drawString(750, 810, 'x750')
    c.drawString(800, 810, 'x800')

    c.drawString(10, 50, 'y50')
    c.drawString(10, 100, 'y100')
    c.drawString(10, 150, 'y150')
    c.drawString(10, 200, 'y200')
    c.drawString(10, 250, 'y250')
    c.drawString(10, 300, 'y300')
    c.drawString(10, 350, 'y350')
    c.drawString(10, 400, 'y400')
    c.drawString(10, 450, 'y450')
    c.drawString(10, 500, 'y500')
    c.drawString(10, 550, 'y550')
    c.drawString(10, 600, 'y600')
    c.drawString(10, 650, 'y650')
    c.drawString(10, 700, 'y700')
    c.drawString(10, 750, 'y750')
    c.drawString(10, 800, 'y800')

    # Define margens
    left_margin = 0
    bottom_margin = 0
    top_margin = 80
    right_margin = 0

    # Define o título do documento
    c.setTitle("Tabela de Desempenho")
    c.setAuthor("Sistema de Dashboards")
    c.setSubject("Desempenho na Campanha Gulozitos")
    c.setKeywords(["PDF", "Desempenho", "Campanha"])

    if hasattr(df, 'values'):
        data = [df.columns.tolist()] + df.values.tolist()

    # Cria a tabela
    table = Table(data)

    # Define o estilo da tabela
    cor_1: Final = colors.HexColor("#070717")  # Azul escuro
    cor_2: Final = colors.HexColor("#ffffff")  # Branco
    cor_3: Final = colors.HexColor("#073c55")  # Azul claro 
    positivo: Final = colors.HexColor("#35DB69")  # Verde
    negativo: Final = colors.HexColor("#DB3835")  # Vermelho

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), cor_1),
        ('TEXTCOLOR', (0, 0), (-1, 0), cor_2),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), cor_2),
        ('GRID', (0, 0), (-1, -1), 1, cor_3),
    ])

    # Índice da coluna "status"
    status_col_idx = 8  

    # Estilizando as células da coluna "status" com base nos valores
    for i, row in enumerate(data[1:], start=1):  # Começa do 1 para ignorar o cabeçalho
        if row[status_col_idx] == "↑↑↑":
            style.add('BACKGROUND', (status_col_idx, i), (status_col_idx, i), positivo)
        elif row[status_col_idx] == "↓↓↓":
            style.add('BACKGROUND', (status_col_idx, i), (status_col_idx, i), negativo)

    table.setStyle(style)

    # Define a posição inicial da tabela
    table.wrapOn(c, width - left_margin - right_margin, height - top_margin - bottom_margin)
    table.drawOn(c, left_margin, height - top_margin - table._height)

    c.showPage()
    c.save()

    regua(c, "Vertical")
    reticula(c)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<br><a class="download" href="data:application/pdf;base64,{b64}" download="TabelaPDF.pdf">BAIXAR</a>'
    return href