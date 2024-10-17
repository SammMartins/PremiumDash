import pandas as pd
import streamlit as st
import datetime
import requests
from io import BytesIO
import base64
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from babel.numbers import format_currency as babel_format_currency


# ----------------- Função para formatar números -----------------
def format_number(value):
    # Verificar se o valor é uma string e convertê-lo para float
    if isinstance(value, str):
        value = float(value.replace('R$', '').replace('.', '').replace(',', '.'))
    return 'R${:,.0f}'.format(value).replace(",", "v").replace(".", ",").replace("v", ".")

# ----------------- Função Define datas -----------------
def data_semana_ini(): # retorna data de início da semana
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    return start_of_week

def data_semana_fim(): # retorna data de fim da semana
    return datetime.date.today()

# ---------------- Função para criar um link de download da tabela em Excel ----------------
def getTableXls(df):
    to_excel = BytesIO()
    df.to_excel(to_excel, index=False)  # removido o argumento encoding
    to_excel.seek(0)
    b64 = base64.b64encode(to_excel.read()).decode()  # algumas conversões de strings <-> bytes necessárias aqui
    href = f'<br><a class="download" href="data:application/vnd.ms-excel;base64,{b64}" download="TabelaExcel.xls">BAIXAR</a>'
    st.toast('Clique em BAIXAR para obter o arquivo')
    return href

# ---------------- Função para criar um link de download da tabela em PDF ----------------
def getTablePdf(df):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    p.setFont("Helvetica", 8)

    # Margens e espaçamento
    margin = 40
    line_height = 15  # Aumenta o espaçamento entre as linhas
    col_width = (width - 2 * margin) / len(df.columns)  # Largura das colunas para caber na página

    # Cabeçalho
    x = margin
    y = height - margin
    for col in df.columns:
        p.drawString(x + 2, y - 2, str(col))  # Adiciona um pequeno espaçamento para os caracteres
        x += col_width
    y -= line_height

    # Linha abaixo do cabeçalho
    p.line(margin, y + line_height / 2, width - margin, y + line_height / 2)

    # Dados
    for row in df.itertuples(index=False):
        x = margin
        for value in row:
            value = str(value)
            if len(value) * 4 > col_width:
                value = value[:int(col_width / 4) - 3] + '...'
            p.drawString(x + 2, y - 2, value)  # Adiciona um pequeno espaçamento para os caracteres
            x += col_width
        y -= line_height
        p.line(margin, y + line_height / 2, width - margin, y + line_height / 2)  # Linha entre as linhas de dados
        if y < margin:  # Nova página se não houver espaço
            p.showPage()
            y = height - margin
            # Redesenha o cabeçalho em nova página
            x = margin
            for col in df.columns:
                p.drawString(x + 2, y - 2, str(col))
                x += col_width
            y -= line_height
            p.line(margin, y + line_height / 2, width - margin, y + line_height / 2)

    p.save()
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<br><a class="download" href="data:application/pdf;base64,{b64}" download="TabelaPDF.pdf">BAIXAR</a>'
    return href

# ---------------- Função para obter coordenadas de um CEP usando a awesomeAPI ----------------
def get_coords_from_cep(cep):
    # Converter para string
    cep = str(cep)
    # Remove caracteres não numéricos
    cep = ''.join(filter(str.isdigit, cep))

    # Realiza a requisição 
    response = requests.get(f"https://cep.awesomeapi.com.br/json/{cep}")

    # Verifica se a requisição foi bem sucedida e se não retornou erro
    if response.status_code == 200: # 200 significa que a requisição foi bem sucedida
        # Converte a resposta HTTP de JSON para um dicionário Python
        data = response.json()
        if 'erro' not in data:
            return data.get('lat'), data.get('lng')
    return None

# Função para formatar moeda
def format_currency(value, currency, locale):
    return babel_format_currency(value, currency, locale=locale)

# Função para formatar data
def format_date_value(date, locale):
    return format_date(date, locale=locale)