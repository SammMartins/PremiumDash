from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts  import TTFont
from reportlab.pdfbase          import pdfmetrics

# Função para desenhar uma régua
def regua(c, orientacao):
    if orientacao == "Vertical":
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

    elif orientacao == "Horizontal":
        c.drawString(50, 580, 'x50')
        c.drawString(100, 580, 'x100')
        c.drawString(150, 580, 'x150')
        c.drawString(200, 580, 'x200')
        c.drawString(250, 580, 'x250')
        c.drawString(300, 580, 'x300')
        c.drawString(350, 580, 'x350')
        c.drawString(400, 580, 'x400')
        c.drawString(450, 580, 'x450')
        c.drawString(500, 580, 'x500')
        c.drawString(550, 580, 'x550')
        c.drawString(600, 580, 'x600')
        c.drawString(650, 580, 'x650')
        c.drawString(700, 580, 'x700')
        c.drawString(750, 580, 'x750')
        c.drawString(800, 580, 'x800')
        
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



# Função para desenhar um reticulado
def reticula(pdf):
    pdf.setStrokeColor(colors.lightgrey)
    pdf.setLineWidth(0.2)
    
    largura, altura = pdf._pagesize  # Obtém a largura e altura da página
    
    for x in range(0, int(largura) + 1, 10):  # Inclui a linha na posição máxima
        pdf.line(x, 0, x, altura)
        
    for y in range(0, int(altura) + 1, 10):  # Inclui a linha na posição máxima
        pdf.line(0, y, largura, y)

# Função para converter milímetros em pontos (mm -> pt)
def mm2pt(mm):
    return mm / 0.352777778 

# Cria um dataframe de exemplo
def df_Exemplo():
    import pandas as pd
    
    df = pd.DataFrame({
        'Nome': ['João', 'Maria', 'José', 'Ana', 'Pedro'],
        'Idade': [25, 30, 21, 28, 35],
        'Sexo': ['M', 'F', 'M', 'F', 'M'],
        'Salário': [2500, 3000, 2000, 2800, 3500],
        'Cargo': ['Analista', 'Gerente', 'TI', 'Gerente', 'Diretor']
    })
    
    return df