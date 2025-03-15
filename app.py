# Módulos da bibliotecas Python
from datetime import datetime, timedelta
from turtle import left
from dateutil.relativedelta import relativedelta
import math
import time as tm
from matplotlib.pylab import f
import numpy as np
from configparser import ConfigParser
from typing import Final
import random

# Módulos Python para Dashboards e outros usos
import numpy as np
import pandas as pd
import streamlit as st
from st_keyup import st_keyup # Módulo para capturar eventos de teclado
from streamlit_extras.stylable_container import stylable_container # Módulo para estilizar os containers
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header
import locale
import bleach 


# Módulos da aplicação e locais 
from dataset import (df1, df2, df3, df4, diasUteis, diasDecorridos, flash322RCA, flashDN322RCA, flash1464RCA, 
                     flash322RCA_semDev, flashDN1464RCA, flash1464SUP, flashDN1464SUP, flash322SUP, flashDN322SUP, 
                     top100Cli, top100Cli_comparativo, metaCalc, metaSupCalc, verbas, trocaRCA, top10CliRCA, 
                     pedErro, devolucao, campanhaDanone, inad, pedCont, estoque266, qtdVendaProd, prodSemVenda, 
                     cliente_semVenda, pedidoVsEstoque, campanhaYoPRO, ceps, cortesEquipe, cortesFornec, campanhaGulao,
                     inadimplenciaSup, nomesRCA, nomesFornec, nomesSup, mix_ideal_dn, mix_ideal_listaCli_listaSku)
from grafic import  gerar_graficoVendas
from utils import   (format_number, data_semana_ini, data_semana_fim, getTableXls, getTablePdf, get_coords_from_cep, 
                     format_currency, format_date_value)
from pdf_generator  import flash_pdf


# Inicializa st.session_state
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = ':beginner: INÍCIO'
if 'buttons_pressed' not in st.session_state:
    st.session_state['buttons_pressed'] = {
        ':beginner: INÍCIO': False,
        ':dollar: VENDA': False,
        ':bar_chart: FLASH': False,
        ':dart: META': False,
        ':department_store: CLIENTES': False,
        ':bank: VERBAS': False,
        ':point_up: DEDO DURO': False,
        ':notebook:': False
    }

def set_active_tab(tab_name):
    st.session_state['active_tab'] = tab_name
    st.session_state['buttons_pressed'][tab_name] = True

# Função de formatação personalizada
def custom_format(x):
    return '{:,.2f}'.format(x).replace(",", "@").replace(".", ",").replace("@", ".")

# Alterar a formatação de exibição para usar ponto como separador de milhares e vírgula como separador decimal
pd.options.display.float_format = custom_format

meses = {
    1: "JANEIRO",
    2: "FEVEREIRO",
    3: "MARÇO",
    4: "ABRIL",
    5: "MAIO",
    6: "JUNHO",
    7: "JULHO",
    8: "AGOSTO",
    9: "SETEMBRO",
    10: "OUTUBRO",
    11: "NOVEMBRO",
    12: "DEZEMBRO"
}
path = '/home/ti_premium/PyDashboards/PremiumDashboards/'

# Variáveis de Globais ---------------------------------------------------
nomesRCA_result = nomesRCA() # '0': Código | '1': Nome | '2': Nome Completo | '3': Código de Supervisor

nomesFornec_result = nomesFornec() # '0': Código | '1': Fantasia | '2': Razão Social

nomesSup_result = nomesSup() # '0': Código | '1': Nome | '2': Nome Completo | '3': Código de RCA

# ----------------------- Configuração do dashboard
st.set_page_config(page_title="PREMIUM DASH", page_icon='https://cdn-icons-png.flaticon.com/512/8556/8556430.png', layout="wide", initial_sidebar_state="expanded")
                        
# Cria o Cabeçalho
header = f"""
<body>
    <header>
        <div class="header-container">
            <img src="https://sammmartins.github.io/premiumdistribuidoravca/premium_pqna.png" class="logoPremium" alt="Logo Premium">
        </div>
    </header>
</body>
"""
# ------ Estilos CSS personalizados
with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/header.css', "r") as file:
    cssHeader = file.read()
cssHeader = f"""
    <style>
        {cssHeader}
    </style>
"""

# Exibe o Cabeçalho
st.markdown(header, unsafe_allow_html=True)
st.markdown(cssHeader, unsafe_allow_html=True) # Aplicando os estilos CSS

# ------ Estilos CSS personalizados
with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/button1.css', "r") as file:
    cssButton1 = file.read()  

with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/button2.css', "r") as file:
    cssButton2 = file.read()  

with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/divider1.css', "r") as file:
    cssDivider = file.read()  

with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/title1.css', "r") as file:
    cssTitle1 = file.read()  

with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/metric1.css', "r") as file:
    cssMetric1 = file.read()  

# ----------------------- Dashboard Layout ----------------------- #
tabs = st.tabs([":beginner: INÍCIO", ":dollar: VENDA", ":bar_chart: FLASH", ":dart: META", ":department_store: CLIENTES", ":bank: VERBAS", ":point_up: DEDO DURO", ":notebook:"])

# Botão para iniciar st.session_state e carregar os Dashboards de cada aba (tabs). Cabeçalho das Abas.
with tabs[0]:
    if not st.session_state['buttons_pressed'][':beginner: INÍCIO']:
        # ------------------ TELA DE LOGIN ------------------ #
        lc1, lc2, lc3 = st.columns([1, 0.5, 1])
        with lc2:
            login = st.container(border=True)
            with login:
                st.title("LOGIN", anchor = False)
                usernameSemTratar = st_keyup("Usuário", type="text", max_chars = 20)
                passwordSemTratar = st_keyup("Senha", type="password", max_chars = 14)

                with stylable_container(key="ACESSAR",css_styles = cssButton1):
                    login_button = st.button("ACESSAR", key="ACESSAR", use_container_width=True) # use_container_width para ocupar toda a largura do container
            
                if login_button:
                    usernameInput = bleach.clean(usernameSemTratar)
                    passwordInput = bleach.clean(passwordSemTratar)
                    with open('/home/ti_premium/dbpath.txt', 'r') as file:
                        dbpath = file.read().strip().strip("'")
                    config = ConfigParser()
                    files = config.read(dbpath)
                    if not files:
                        st.error(":x: Erro de leitura")
                        raise ValueError(f"Não foi possível ler o arquivo: {dbpath}")
                
                    try:
                        username = config.get(f'{usernameInput}_user_dashboard', 'username')
                        password = config.get(f'{usernameInput}_user_dashboard', 'password')
                        if 'control' not in st.session_state:
                            # Armazena control no estado da sessão caso já não tenha sido feito
                            st.session_state['control'] = int(config.get(f'{usernameInput}_user_dashboard', 'control'))

                    except Exception as e:
                        st.error(":x: Usuário ou senha inválido!")

                    
                    if usernameInput == username and passwordInput == password:
                        st.success("Login aprovado!")
                        st.session_state['buttons_pressed'][':beginner: INÍCIO'] = True
                        
                    else:
                        st.error(":x: Usuário ou senha inválido!")
                        if 'control' not in st.session_state:
                            st.session_state['control'] = 0

        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col3:
            containerLogin3 = st.container(border=True)
            containerLogin3.subheader("Novidades no Dashboard:", divider="gray")
            containerLogin3.markdown("Painel de campanhas disponível na aba de :dollar: VENDA")
            containerLogin3.markdown("Painel de cortes disponível na aba de :point_up: DEDO DURO")
            containerLogin3.subheader("Tutoriais:", divider="gray")
            containerLogin3.markdown("EM BREVE!")

        with col2:
            containerLogin2 = st.container(border=True)
            containerLogin2.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/decisao.png', use_column_width=True)

        with col1:
            containerLogin1 = st.container(border=True)
            containerLogin1.subheader("Dashboards e Decisões:", divider="gray")
            containerLogin1.markdown("Existem três modelos de tomada de decisão: o racional, o intuitivo e o criativo.")
            containerLogin1.markdown("Pensando no modelo racional, os Dashboards são uma ferramenta indispensável para a tomada de decisão:")
            containerLogin1.markdown("1. Primeiramente defina o objetivo.")
            containerLogin1.markdown("2. Busque por dados e informações, através dos diversos painéis disponíveis.")
            containerLogin1.markdown("3. Realize um brainstorming de soluções. Em outras palavras: reúna a equipe para discutir possíveis soluções.")
            containerLogin1.markdown("4. Escolha a melhor solução.")
            containerLogin1.markdown("5. Por fim, crie um planejamento estratégico e mensure de resultados.")



    else:
        # ------------------ TELA DE LOGIN ------------------ #
        lc1, lc2, lc3 = st.columns([1, 0.5, 1])
        with lc2:
            login = st.container(border=True)
            with login:
                st.title("LOGIN", anchor = False)
                st.success("Seu login está aprovado!")

        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col3:
            containerLogin3 = st.container(border=True)
            containerLogin3.subheader("Novidades no Dashboard:", divider="gray")
            containerLogin3.markdown("Painel de campanhas disponível na aba de :dollar: VENDA")
            containerLogin3.markdown("Painel de cortes disponível na aba de :point_up: DEDO DURO")
            containerLogin3.subheader("Tutoriais:", divider="gray")
            containerLogin3.markdown("EM BREVE!")

        with col2:
            containerLogin2 = st.container(border=True)
            containerLogin2.image('/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/decisao.png', use_column_width=True)

        with col1:
            containerLogin1 = st.container(border=True)
            containerLogin1.subheader("Dashboards e Decisões:", divider="gray")
            containerLogin1.markdown("Existem três modelos de tomada de decisão: o racional, o intuitivo e o criativo.")
            containerLogin1.markdown("Pensando no modelo racional, os Dashboards são uma ferramenta indispensável para a tomada de decisão:")
            containerLogin1.markdown("1. Primeiramente defina o objetivo.")
            containerLogin1.markdown("2. Busque por dados e informações, através dos diversos painéis disponíveis.")
            containerLogin1.markdown("3. Realize um brainstorming de soluções. Em outras palavras: reúna a equipe para discutir possíveis soluções.")
            containerLogin1.markdown("4. Escolha a melhor solução.")
            containerLogin1.markdown("5. Por fim, crie um planejamento estratégico e mensure de resultados.")


with tabs[1]:
    if not st.session_state['buttons_pressed'][':dollar: VENDA']:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/1358/1358684.png', width=180)
        with c2:
            st.title("PAINEL DE VENDAS", anchor = False)
            st.markdown(":page_with_curl: Faturado e não faturado semelhante a rotina 322 Winthor Totvs")
            st.markdown(":iphone: Apenas pedidos digitados pelo vendedor são exibidos")
            if 'control' in st.session_state and st.session_state['control'] >= 5:
                st.button('CARREGAR', key="loadVENDA", on_click=set_active_tab, args=(':dollar: VENDA',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")
    else:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/1358/1358684.png', width=180)
        with c2:
            st.title("PAINEL DE VENDAS", anchor = False)
            st.markdown(":page_with_curl: Faturado e não faturado semelhante a rotina 322 Winthor Totvs")
            st.markdown(":iphone: Apenas pedidos digitados pelo vendedor são exibidos")
            if 'control' in st.session_state and st.session_state['control'] >= 5:
                st.button('CARREGAR', key="loadVENDA", on_click=set_active_tab, args=(':dollar: VENDA',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")

with tabs[2]:
    if not st.session_state['buttons_pressed'][':bar_chart: FLASH']:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/7890/7890470.png', width=180)
        with c2:
            st.title("RELATÓRIO FLASH", anchor = False)
            st.markdown(":rocket: Um painel completo sobre seu :blue[desempenho] de vendas")
            st.markdown(":moneybag: Tenha controle sobre sua :green[remuneração] mensal")
            if 'control' in st.session_state and st.session_state['control'] >= 5:
                st.button('CARREGAR', key="loadFLASH", on_click=set_active_tab, args=(':bar_chart: FLASH',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")
    else:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/7890/7890470.png', width=180)
        with c2:
            st.title("RELATÓRIO FLASH", anchor = False)
            st.markdown(":rocket: Um painel completo sobre seu :blue[desempenho] de vendas")
            st.markdown(":moneybag: Tenha controle sobre sua :green[remuneração] mensal")
            if 'control' in st.session_state and st.session_state['control'] >= 5:
                st.button('CARREGAR', key="loadFLASH", on_click=set_active_tab, args=(':bar_chart: FLASH',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")                

with tabs[3]:
    if not st.session_state['buttons_pressed'][':dart: META']:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/8213/8213190.png', width=180)
        with c2:
            st.title("CONSULTAR META", anchor = False)
            st.markdown("Painel destinado a :blue[CONSULTA] das metas")
            st.markdown("<br>", unsafe_allow_html=True)
            if 'control' in st.session_state and st.session_state['control'] >= 5:
                st.button('CARREGAR', key="loadMETA", on_click=set_active_tab, args=(':dart: META',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")
    else:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/8213/8213190.png', width=180)
        with c2:
            st.title("CONSULTAR META", anchor = False)
            st.markdown("Painel destinado a :blue[CONSULTA] das metas")
            st.markdown("<br>", unsafe_allow_html=True)
            if 'control' in st.session_state and st.session_state['control'] >= 5:
                st.button('CARREGAR', key="loadMETA", on_click=set_active_tab, args=(':dart: META',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")            

with tabs[4]:
    if not st.session_state['buttons_pressed'][':department_store: CLIENTES']:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/5434/5434400.png', width=180)
        with c2:
            st.title("RELATÓRIO CLIENTES", anchor = False)
            st.markdown("Painel destinado a :blue[análise detalhada] dos principais clientes")
            st.markdown("<br>", unsafe_allow_html=True)
            if 'control' in st.session_state and st.session_state['control'] >= 5:            
                st.button('CARREGAR', key="loadCLIENTES", on_click=set_active_tab, args=(':department_store: CLIENTES',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")                  
    else:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/5434/5434400.png', width=180)
        with c2:
            st.title("RELATÓRIO CLIENTES", anchor = False)
            st.markdown("Painel destinado a :blue[análise detalhada] dos principais clientes")
            st.markdown("<br>", unsafe_allow_html=True)
            if 'control' in st.session_state and st.session_state['control'] >= 5:            
                st.button('CARREGAR', key="loadCLIENTES", on_click=set_active_tab, args=(':department_store: CLIENTES',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")   

with tabs[5]:
    if not st.session_state['buttons_pressed'][':bank: VERBAS']:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/1649/1649628.png', width=180)
        with c2:
            st.title("CONSULTAR VERBA", anchor = False)
            st.markdown("Painel destinado a consultar :green[VERBAS]")
            st.markdown("<br>", unsafe_allow_html=True)
            if 'control' in st.session_state and st.session_state['control'] >= 5:                     
                st.button('CARREGAR', key="loadVERBAS", on_click=set_active_tab, args=(':bank: VERBAS',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")               
    else:
        c1, c2 = st.columns([0.300, 1])
        with c1:
            st.image('https://cdn-icons-png.flaticon.com/512/1649/1649628.png', width=180)
        with c2:
            st.title("CONSULTAR VERBA", anchor = False)
            st.markdown("Painel destinado a consultar :green[VERBAS]")
            st.markdown("<br>", unsafe_allow_html=True)
            if 'control' in st.session_state and st.session_state['control'] >= 5:                     
                st.button('CARREGAR', key="loadVERBAS", on_click=set_active_tab, args=(':bank: VERBAS',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")   

with tabs[6]:
    if not st.session_state['buttons_pressed'][':point_up: DEDO DURO']:
        colum1, colum2 = st.columns([0.300, 1])
        with colum1:
            st.image('https://cdn-icons-png.flaticon.com/512/4380/4380709.png', width=180)
        with colum2:    
            st.title(":point_up: DEDO DURO", anchor = False)
            st.markdown("Painel destinado a apontar :red[ERROS] e :red[PROBLEMAS] diversos")
            st.markdown("<br>", unsafe_allow_html=True)
            if 'control' in st.session_state and st.session_state['control'] >= 3:                  
                st.button('CARREGAR', key="loadDEDODURO", on_click=set_active_tab, args=(':point_up: DEDO DURO',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")               
    else:
        colum1, colum2 = st.columns([0.300, 1])
        with colum1:
            st.image('https://cdn-icons-png.flaticon.com/512/4380/4380709.png', width=180)
        with colum2:    
            st.title(":point_up: DEDO DURO", anchor = False)
            st.markdown("Painel destinado a apontar :red[ERROS] e :red[PROBLEMAS] diversos")
            st.markdown("<br>", unsafe_allow_html=True)
            if 'control' in st.session_state and st.session_state['control'] >= 3:                  
                st.button('CARREGAR', key="loadDEDODURO", on_click=set_active_tab, args=(':point_up: DEDO DURO',))
            else:
                st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")         

with tabs[7]:
    if not st.session_state['buttons_pressed'][':notebook:']:
        if 'control' in st.session_state and st.session_state['control'] >= 6:         
            st.button('CARREGAR', key="loadNOTEBOOK", on_click=set_active_tab, args=(':notebook:',))
        else:
            st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")    
    else:
        if 'control' in st.session_state and st.session_state['control'] >= 6:         
            st.button('CARREGAR', key="loadNOTEBOOK", on_click=set_active_tab, args=(':notebook:',))
        else:
            st.error(":x: RECURSO BLOQUEADO PARA ESSE USUÁRIO")  

# --------------------------- Flash ------------------- # ------------------- # ------------------- # ------------------- # ------------------- # 
if st.session_state['active_tab'] == ':bar_chart: FLASH':
    with tabs[2]:
        st.divider()
        st.markdown("<br>", unsafe_allow_html=True)
        col_1, col_2 = st.columns([0.70, 1])
        with col_1:
            with st.expander("SELEÇÃO DE PARÂMETROS"): 
                notFatOn = st.toggle(":red[CONSIDERAR PEDIDOS NÃO FATURADOS NO RESULTADO]", help="Selecione para exibir pedidos digitados que não foram faturados")
                if notFatOn == True:
                    devOn = st.toggle(":red[ABATER DEVOLUÇÃO DO RESULTADO]", help="Selecione para abater devoluções dos pedidos não faturados.", value=True)
                
        st.markdown("<br>", unsafe_allow_html=True)

        with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
            tm.sleep(2)
            aba2_1, aba2_2, aba2_3, mix = st.tabs([":bar_chart: :red[Gerencial - Inativo]", ":male-office-worker: :blue[Supervisor]", ":man: :green[Vendedor]", ":material/shopping_basket: CAMPEÕES DE VENDA DANONE"])
            dias_uteis_result = str(diasUteis()).split()[-1]
            dias_decor_result = str(diasDecorridos()).split()[-1]
        # -------------------------------- Mix de Produtos -------------------------------- # -------------------------------- #
        with mix:
            st.title(":material/shopping_basket: CAMPEÕES DE VENDA DANONE", anchor = False)
            col1, col2 = st.columns([1, 3])
            with col1:
                vendedorName = st.selectbox(":man: VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='cesta_rca', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
                if vendedorName == "LEONARDO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (140,),index=0, key='cesta_140', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "EDNALDO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (141,),index=0, key='cesta_141', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "VAGNER":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (142,),index=0, key='cesta_142', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "DEIVID":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (143,),index=0, key='cesta_143', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "BISMARCK":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (145,),index=0, key='cesta_145', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LUCIANA":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (147,),index=0, key='cesta_147', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MATHEUS":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (148,),index=0, key='cesta_148', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MARCIO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (150,),index=0, key='cesta_150', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LEANDRO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (151,),index=0, key='cesta_151', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "REGINALDO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (152,),index=0, key='cesta_152', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ROBSON":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (153,),index=0, key='cesta_153', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "JOAO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (154,),index=0, key='cesta_154', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "TAYANE":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (155,),index=0, key='cesta_155', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MURILO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (156,),index=0, key='cesta_156', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LUCAS":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (157,),index=0, key='cesta_157', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "DEYVISON":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (158,),index=0, key='cesta_158', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ZEFERINO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (161,),index=0, key='cesta_161', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "EPAMINONDAS":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (164,),index=0, key='cesta_164', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "GLAUBER":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (167,),index=0, key='cesta_167', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MATEUS":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (168,),index=0, key='cesta_168', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "THIAGO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (169,),index=0, key='cesta_169', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "FILIPE":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (170,),index=0, key='cesta_170', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ROMILSON":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (172,),index=0, key='cesta_172', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "VALDEME":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (174,),index=0, key='cesta_174', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                else:
                    vendedorCod = st.selectbox("ERRO", (999,),index=0, key='cesta_0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")

                carregar_cesta = st.button("CARREGAR", key="carregar_cesta", use_container_width=True)
            
            if carregar_cesta:
                st.markdown("<br><br>", unsafe_allow_html=True)
                resultado_mix_ideal_dn = mix_ideal_dn(vendedorCod)
               
                resultado_mix_ideal_dn = resultado_mix_ideal_dn[0][0]  

                
                colored_header(
                    label="CESTA DE PRODUTOS",
                    description=f"INDICES PARA O MIX IDEAL DE PRODUTOS - {vendedorName}",
                    color_name="light-blue-70",
                )

                st.session_state['dn_danone_vendedor'] = int(resultado_mix_ideal_dn) 


                if st.session_state['dn_danone_vendedor'] == 0:
                    st.error(":material/error: Sem dados para exibir")
                else:
                    left1, center1, right1 = st.columns([1, 1, 1])

                    with left1:
                        #center_left, center_center, center_right = st.columns([1, 1, 1])

                        st.metric(label="CLIENTES DE DANONE NO MÊS", value=st.session_state['dn_danone_vendedor'], delta=f"100%", delta_color="off")
                        
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)     
                        
                    st.divider()
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    resultado_lista = mix_ideal_listaCli_listaSku(vendedorCod)

                    resultado_lista = resultado_lista.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]].rename(columns={
                        0: "RCA",
                        1: "VENDEDOR",
                        2: "CODCLI",
                        3: "CLIENTE",
                        4: "FANTASIA",
                        5: "MUNICIPIO",
                        6: "MIX ATENDIDO",
                        7: "ACTIVIA 150G AMEIXA - 17528 - 50%",
                        8: "POLPA KIDS MORANGO - 18157 - 50%",
                        9: "DHO P/ LEVAR MORANGO - 17507 - 70%",
                        10: "DANONINHO 80G MORANGO - 17506 - 50%",
                        11: "ACTIVIA 800G AMEIXA E MORANGO - 18446 / 18447 - 50%",
                        12: "DANONINHO MULTI 320G - 17462 - 50%",
                        13: "DANONINHO P/ BEBER 100G MORANGO - 17507 - 50%",
                        14: "DANONE VD 170G MORANGO - 17517 - 50%",
                        15: "DANETTE SOBREMESA CHOC 90G - 18035 - 50%",
                        16: "YOPRO UHT CHOCOLATE - 17885 - 50%",
                        17: "YOPRO LIQ 250G MORANGO - 17932 - 50%",
                        18: "DANONE MORANGO 850G - 18079 - 50%",
                        19: "DANONE CORPUS 800G MORANGO - 18448 - 50%"
                    })

                    # -------------------------------- METRIC PRODUTOS -------------------------------- #
                    
                    activia_150g_ameixa_17528 = resultado_lista["ACTIVIA 150G AMEIXA - 17528 - 50%"].value_counts().get(1, 0)
                    porcent_activia_150g_ameixa_17528 = round((activia_150g_ameixa_17528 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    polpa_kids_morango_18157 = resultado_lista["POLPA KIDS MORANGO - 18157 - 50%"].value_counts().get(1, 0)
                    porcent_polpa_kids_morango_18157 = round((polpa_kids_morango_18157 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    dho_p_levar_morango_17507 = resultado_lista["DHO P/ LEVAR MORANGO - 17507 - 70%"].value_counts().get(1, 0)
                    porcent_dho_p_levar_morango_17507 = round((dho_p_levar_morango_17507 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    danoninho_80g_morango_17506 = resultado_lista["DANONINHO 80G MORANGO - 17506 - 50%"].value_counts().get(1, 0)
                    porcent_danoninho_80g_morango_17506 = round((danoninho_80g_morango_17506 / st.session_state['dn_danone_vendedor']) * 100, 1)
#
                    activia_800g_ameixa_morango_18446_18447 = resultado_lista["ACTIVIA 800G AMEIXA E MORANGO - 18446 / 18447 - 50%"].value_counts().get(1, 0)
                    porcent_activia_800g_ameixa_morango_18446_18447 = round((activia_800g_ameixa_morango_18446_18447 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    danoninho_multi_320g_17462 = resultado_lista["DANONINHO MULTI 320G - 17462 - 50%"].value_counts().get(1, 0)
                    porcent_danoninho_multi_320g_17462 = round((danoninho_multi_320g_17462 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    danoninho_p_beber_100g_morango_17507 = resultado_lista["DANONINHO P/ BEBER 100G MORANGO - 17507 - 50%"].value_counts().get(1, 0)
                    porcent_danoninho_p_beber_100g_morango_17507 = round((danoninho_p_beber_100g_morango_17507 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    danone_vd_170g_morango_17517 = resultado_lista["DANONE VD 170G MORANGO - 17517 - 50%"].value_counts().get(1, 0)
                    porcent_danone_vd_170g_morango_17517 = round((danone_vd_170g_morango_17517 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    danette_sobremesa_choc_90g_18035 = resultado_lista["DANETTE SOBREMESA CHOC 90G - 18035 - 50%"].value_counts().get(1, 0)
                    porcent_danette_sobremesa_choc_90g_18035 = round((danette_sobremesa_choc_90g_18035 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    yopro_uht_chocolate_17885 = resultado_lista["YOPRO UHT CHOCOLATE - 17885 - 50%"].value_counts().get(1, 0)
                    porcent_yopro_uht_chocolate_17885 = round((yopro_uht_chocolate_17885 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    yopro_liq_250g_morango_17932 = resultado_lista["YOPRO LIQ 250G MORANGO - 17932 - 50%"].value_counts().get(1, 0)
                    porcent_yopro_liq_250g_morango_17932 = round((yopro_liq_250g_morango_17932 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    danone_morango_850g_18079 = resultado_lista["DANONE MORANGO 850G - 18079 - 50%"].value_counts().get(1, 0)
                    porcent_danone_morango_850g_18079 = round((danone_morango_850g_18079 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    danone_corpus_800g_morango_18448 = resultado_lista["DANONE CORPUS 800G MORANGO - 18448 - 50%"].value_counts().get(1, 0)
                    porcent_danone_corpus_800g_morango_18448 = round((danone_corpus_800g_morango_18448 / st.session_state['dn_danone_vendedor']) * 100, 1)

                    color_delta_normal = "normal"
                    color_delta_inverse = "inverse"

                    left2, center2, right2 = st.columns([1, 1, 1])

                    if porcent_activia_150g_ameixa_17528 >= 50:
                        left2.metric(label="ACTIVIA 150G AMEIXA - 17528", value=f"{porcent_activia_150g_ameixa_17528}%", delta=f"{activia_150g_ameixa_17528} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:    
                        left2.metric(label="ACTIVIA 150G AMEIXA - 17528", value=f"{porcent_activia_150g_ameixa_17528}%", delta=f"{activia_150g_ameixa_17528} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_polpa_kids_morango_18157 >= 50:
                        center2.metric(label="POLPA KIDS MORANGO - 18157", value=f"{porcent_polpa_kids_morango_18157}%", delta=f"{polpa_kids_morango_18157} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        center2.metric(label="POLPA KIDS MORANGO - 18157", value=f"{porcent_polpa_kids_morango_18157}%", delta=f"{polpa_kids_morango_18157} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_dho_p_levar_morango_17507 >= 70:
                        right2.metric(label="DHO P/ LEVAR MORANGO - 17507", value=f"{porcent_dho_p_levar_morango_17507}%", delta=f"{dho_p_levar_morango_17507} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        right2.metric(label="DHO P/ LEVAR MORANGO - 17507", value=f"{porcent_dho_p_levar_morango_17507}%", delta=f"{dho_p_levar_morango_17507} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_danoninho_80g_morango_17506 >= 50:
                        left2.metric(label="DANONINHO 80G MORANGO - 17506", value=f"{porcent_danoninho_80g_morango_17506}%", delta=f"{danoninho_80g_morango_17506} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        left2.metric(label="DANONINHO 80G MORANGO - 17506", value=f"{porcent_danoninho_80g_morango_17506}%", delta=f"{danoninho_80g_morango_17506} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True) 

                    if porcent_activia_800g_ameixa_morango_18446_18447 >= 50:
                        center2.metric(label="ACTIVIA 800G AMEIXA E MORANGO - 18446 / 18447", value=f"{porcent_activia_800g_ameixa_morango_18446_18447}%", delta=f"{activia_800g_ameixa_morango_18446_18447} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        center2.metric(label="ACTIVIA 800G AMEIXA E MORANGO - 18446 / 18447", value=f"{porcent_activia_800g_ameixa_morango_18446_18447}%", delta=f"{activia_800g_ameixa_morango_18446_18447} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_danoninho_multi_320g_17462 >= 50:
                        right2.metric(label="DANONINHO MULTI 320G - 17462", value=f"{porcent_danoninho_multi_320g_17462}%", delta=f"{danoninho_multi_320g_17462} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        right2.metric(label="DANONINHO MULTI 320G - 17462", value=f"{porcent_danoninho_multi_320g_17462}%", delta=f"{danoninho_multi_320g_17462} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_danoninho_p_beber_100g_morango_17507 >= 50:
                        left2.metric(label="DANONINHO P/ BEBER 100G MORANGO - 17507", value=f"{porcent_danoninho_p_beber_100g_morango_17507}%", delta=f"{danoninho_p_beber_100g_morango_17507} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        left2.metric(label="DANONINHO P/ BEBER 100G MORANGO - 17507", value=f"{porcent_danoninho_p_beber_100g_morango_17507}%", delta=f"{danoninho_p_beber_100g_morango_17507} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_danone_vd_170g_morango_17517 >= 50:
                        center2.metric(label="DANONE VD 170G MORANGO - 17517", value=f"{porcent_danone_vd_170g_morango_17517}%", delta=f"{danone_vd_170g_morango_17517} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        center2.metric(label="DANONE VD 170G MORANGO - 17517", value=f"{porcent_danone_vd_170g_morango_17517}%", delta=f"{danone_vd_170g_morango_17517} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_danette_sobremesa_choc_90g_18035 >= 50:
                        right2.metric(label="DANETTE SOBREMESA CHOC 90G - 18035", value=f"{porcent_danette_sobremesa_choc_90g_18035}%", delta=f"{danette_sobremesa_choc_90g_18035} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        right2.metric(label="DANETTE SOBREMESA CHOC 90G - 18035", value=f"{porcent_danette_sobremesa_choc_90g_18035}%", delta=f"{danette_sobremesa_choc_90g_18035} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_yopro_uht_chocolate_17885 >= 50:
                        left2.metric(label="YOPRO UHT CHOCOLATE - 17885", value=f"{porcent_yopro_uht_chocolate_17885}%", delta=f"{yopro_uht_chocolate_17885} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        left2.metric(label="YOPRO UHT CHOCOLATE - 17885", value=f"{porcent_yopro_uht_chocolate_17885}%", delta=f"{yopro_uht_chocolate_17885} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_yopro_liq_250g_morango_17932 >= 50:
                        center2.metric(label="YOPRO LIQ 250G MORANGO - 17932", value=f"{porcent_yopro_liq_250g_morango_17932}%", delta=f"{yopro_liq_250g_morango_17932} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        center2.metric(label="YOPRO LIQ 250G MORANGO - 17932", value=f"{porcent_yopro_liq_250g_morango_17932}%", delta=f"{yopro_liq_250g_morango_17932} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_danone_morango_850g_18079 >= 50:
                        right2.metric(label="DANONE MORANGO 850G - 18079", value=f"{porcent_danone_morango_850g_18079}%", delta=f"{danone_morango_850g_18079} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        right2.metric(label="DANONE MORANGO 850G - 18079", value=f"{porcent_danone_morango_850g_18079}%", delta=f"{danone_morango_850g_18079} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    if porcent_danone_corpus_800g_morango_18448 >= 50:
                        center2.metric(label="DANONE CORPUS 800G MORANGO - 18448", value=f"{porcent_danone_corpus_800g_morango_18448}%", delta=f"{danone_corpus_800g_morango_18448} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_normal)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)
                    else:
                        center2.metric(label="DANONE CORPUS 800G MORANGO - 18448", value=f"{porcent_danone_corpus_800g_morango_18448}%", delta=f"{danone_corpus_800g_morango_18448} de {st.session_state['dn_danone_vendedor']} CLIENTES", delta_color=color_delta_inverse)
                        style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)

                    # --------------------------------------- # --------------------------------------- # 
                    st.divider()
                    st.markdown("<br>", unsafe_allow_html=True)

                    mix_posit = resultado_lista["MIX ATENDIDO"].value_counts().get(1, 0)

                    st.session_state['mix_posit_vendedor'] = mix_posit

                    st.session_state['GAP'] = st.session_state['dn_danone_vendedor'] - st.session_state['mix_posit_vendedor']

                    if st.session_state['GAP'] <= 0:
                        color_delta = "normal"
                    else:
                        color_delta = "inverse"

                    right1.metric(label="MIX IDEAL POSITIVADO NO MÊS", value=st.session_state['mix_posit_vendedor'], delta=f"RESTAM {st.session_state['GAP']}", delta_color=color_delta)
                            
                    style_metric_cards(background_color="#252d3d", border_size_px=2, border_color="#FFF", border_radius_px=3, border_left_color="#FFF", box_shadow=True)     
 
                    resultado_lista = resultado_lista.drop(columns=["RCA", "VENDEDOR", "CLIENTE", "MIX ATENDIDO"])

                    st.dataframe(resultado_lista, hide_index=True)

        # -------------------------------- GERENCIAL -------------------------------- # -------------------------------- #
        with aba2_1:
            st.title(":building_construction: :red[Painel em construção]", anchor = False)
        # -------------------------------- SUPERVISOR -------------------------------- # -------------------------------- #
        with aba2_2:
            col1, col2, col3, col4 = st.columns([1.1, 1, 1, 1.60])
            du = diasUteis().values[0][0]
            dd = diasDecorridos().values[0][0]
            velocidade = dd / du
            velStr = str(math.floor(velocidade * 100)) 
            # ------ Estilos CSS personalizados
            with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/flash.css', "r") as file:
                flash_css = file.read()
            css = f"""
                <style>
                    {flash_css}
                </style>
            """
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(dias_uteis_result + " DIAS ÚTEIS", unsafe_allow_html=False, help="Quantidade de dias úteis para serem realizadas suas vendas.")
                st.markdown(dias_decor_result + " DECORRIDOS", unsafe_allow_html=False, help="Quantidade de dias úteis decorridos no mês.")
                st.markdown(velStr + "% - VELOCIDADE", unsafe_allow_html=False, help="Velocidade de vendas realizadas no mês.")
            with col1:
                if (velocidade == 0):
                    st.image(path + 'Imagens/0porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0 and velocidade <= 0.10):
                    st.image(path + 'Imagens/10porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.10 and velocidade <= 0.20):
                    st.image(path + 'Imagens/20porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.20 and velocidade <= 0.30):
                    st.image(path + 'Imagens/30porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.30 and velocidade <= 0.40):
                    st.image(path + 'Imagens/40porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.40 and velocidade <= 0.50):
                    st.image(path + 'Imagens/50porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.50 and velocidade <= 0.60):
                    st.image(path + 'Imagens/60porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.60 and velocidade <= 0.70):
                    st.image(path + 'Imagens/70porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.70 and velocidade <= 0.80):
                    st.image(path + 'Imagens/80porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.80 and velocidade <= 0.90):
                    st.image(path + 'Imagens/90porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.90 and velocidade <= 1):
                    st.image(path + 'Imagens/100porcent.png', width=200, caption='VELOCIDADE')

            with col3:
                supName = st.selectbox(":male-office-worker: SUPERVISOR", ("MARCELO", "VILMAR JR"), index=0, key='sup', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
                if supName == "MARCELO":
                    supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (2,),index=0, key='MARCELO', help="Código de Supervisor preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif supName == "VILMAR JR":
                    supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (8,),index=0, key='vilmar', help="Código de Supervisor preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                else:
                    supCod = st.selectbox("ERRO", (999,),index=0, key='erro', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
            with col4:
                with st.container(height=220, border=False):
                    with st.expander("O que é o Flash?"): 
                        st.write('''
                        O FLASH é um relatório primordial para o acompanhamento de vendas e remuneração.
                        Ele foi criado com objetivo de facilitar o acompanhamento do Vendedor. 
                        Em seu modelo antigo, era necessário atualizar uma planilha Excel de forma manual
                        por alguém apto. 
                        ''')
                        st.image("/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/oldFlash.png")
            
            # ------------------ Faturado Apenas ------------------
            if notFatOn == False:
                col1, col2 = st.columns([1, 0.12])
                with col2:
                    st.caption("Faturado", help="Apenas pedidos faturados. Essa opção trás um resultados real das vendas. Sempre abatendo devoluções.")
                with col1:
                    if st.button("CARREGAR", key="flash1464SUP"):
                        with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                            # --------------- FAT -----------------------
                            flash_result = flash1464SUP(supCod)
                            # --------------- DN  -----------------------
                            formatarPorcent = ['ATINGIDO']
                            # --- DANONE
                            dnFlashDanone = flashDN1464SUP(supCod, 588)
                            if dnFlashDanone.empty:
                                dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- NESTLE
                            dnFlashNestle = flashDN1464SUP(supCod, 1841)
                            if dnFlashNestle.empty:
                                dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DANILLA
                            dnFlashDanilla = flashDN1464SUP(supCod, 1658)
                            if dnFlashDanilla.empty:
                                dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SANTA MASSA
                            dnFlashSantaMassa = flashDN1464SUP(supCod, 1623)
                            if dnFlashSantaMassa.empty:
                                dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FINI
                            dnFlashFini =flashDN1464SUP(supCod, 1488)
                            if dnFlashFini.empty:
                                dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SULMINAS
                            dnFlashSulMinas = flashDN1464SUP(supCod, 1321)
                            if dnFlashSulMinas.empty:
                                dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- GULOZITOS
                            dnFlashGulozitos = flashDN1464SUP(supCod, 1719)
                            if dnFlashGulozitos.empty:
                                dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- HYTS
                            dnFlashHyts = flashDN1464SUP(supCod, 1607)
                            if dnFlashHyts.empty:
                                dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FRUTAP
                            dnFlashFrutap = flashDN1464SUP(supCod, 1728)
                            if dnFlashFrutap.empty:
                                dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])   
                            else:
                                dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DAFRUTA
                            dnFlashDaFruta = flashDN1464SUP(supCod, 1225)
                            if dnFlashDaFruta.empty:
                                dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Seara
                            dnFlashSeara = flashDN1464SUP(supCod, 1541)
                            if dnFlashSeara.empty:
                                dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Eco fresh
                            dnFlashEcofresh = flashDN1464SUP(supCod, 1894)
                            if dnFlashEcofresh.empty:
                                dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            
                            dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh]
                            if any(df.empty for df in dataframes):
                                st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                            else:
                                with st.container(border=False):
                                    # ----------------- Formatação da tabela -----------------
                                    flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                        1: "SEÇÃO",
                                        2: "OBJETIVO",
                                        3: "REALIZADO",
                                        4: "ATINGIDO",
                                        5: "TENDÊNCIA",
                                        6: " R. A. F. ",
                                        7: "NECESS. DIA",
                                        8: "MÉDIA DIA",
                                        9: "STATUS"
                                    })

                                    formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                    for coluna in formatarMoeda:
                                        flash_result[coluna] = flash_result[coluna].apply(format_number)

                                    formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                    for coluna in formatarPorcent:
                                        flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                    # ------ DataFrame para HTML 
                                    table_html = flash_result.to_html(classes='table-style', index=False)
                                    table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>') # Difinindo a classe positivo para aplicar estilos
                                    table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>') # Difinindo a classe negativo para aplicar estilos
                                    table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                    # --- DN
                                    dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                    dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                    dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                    dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                    dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                    dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                    dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                    dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                    dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                    dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                    dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                    dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                    # ----------------- Exibição da tabela -----------------
                                    st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS
                                    st.markdown("<h3 class='dnH3'>TABELA FLASH SUPERVISOR</h3>", unsafe_allow_html=True) # Título da seção
                                    st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit 

                                    # ------------- Tabela Distribuição Numérica ----------
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    st.markdown("<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA SUPERVISOR</h3>", unsafe_allow_html=True)

                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFini, unsafe_allow_html=True)

                                    with col2:
                                        st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                    with col3:
                                        st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFrutap, unsafe_allow_html=True) 


            
            # ------------------ Não Faturado ABATENDO DEVOLUÇÃO ------------------
            else:
                col1, col2 = st.columns([1, 0.12])
                with col2:
                    st.caption("Não Faturado", help="Pedidos digitados que não foram faturados. Abatendo devoluções.")
                with col1:
                    if st.button("CARREGAR", key="flash1464SUPnotFat"):
                        with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                            # --------------- FAT -----------------------
                            flash_result = flash322SUP(supCod)
                            # --------------- DN  -----------------------
                            formatarPorcent = ['ATINGIDO']
                            # --- DANONE
                            dnFlashDanone = flashDN322SUP(supCod, 588)
                            if dnFlashDanone.empty:
                                dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100)) 
                            # --- NESTLE
                            dnFlashNestle = flashDN322SUP(supCod, 1841)
                            if dnFlashNestle.empty:
                                dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DANILLA
                            dnFlashDanilla = flashDN322SUP(supCod, 1658)
                            if dnFlashDanilla.empty:
                                dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SANTA MASSA
                            dnFlashSantaMassa = flashDN322SUP(supCod, 1623)
                            if dnFlashSantaMassa.empty:
                                dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FINI
                            dnFlashFini = flashDN322SUP(supCod, 1488)
                            if dnFlashFini.empty:
                                dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SULMINAS
                            dnFlashSulMinas = flashDN322SUP(supCod, 1321)
                            if dnFlashSulMinas.empty:
                                dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- GULOZITOS
                            dnFlashGulozitos = flashDN322SUP(supCod, 1719)
                            if dnFlashGulozitos.empty:
                                dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- HYTS
                            dnFlashHyts = flashDN322SUP(supCod, 1607)
                            if dnFlashHyts.empty:
                                dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FRUTAP
                            dnFlashFrutap = flashDN322SUP(supCod, 1728)
                            if dnFlashFrutap.empty:
                                dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DAFRUTA
                            dnFlashDaFruta = flashDN322SUP(supCod, 1225)
                            if dnFlashDaFruta.empty:
                                dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Seara
                            dnFlashSeara = flashDN322SUP(supCod, 1541)
                            if dnFlashSeara.empty:
                                dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Eco fresh
                            dnFlashEcofresh = flashDN322SUP(supCod, 1894)
                            if dnFlashEcofresh.empty:
                                dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))



                            dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh]
                            if any(df.empty for df in dataframes):
                                st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                            else:
                                with st.container(border=False):
                                    # ----------------- Formatação da tabela -----------------
                                    flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                        1: "SEÇÃO",
                                        2: "OBJETIVO",
                                        3: "REALIZADO",
                                        4: "ATINGIDO",
                                        5: "TENDÊNCIA",
                                        6: " R. A. F. ",
                                        7: "NECESS. DIA",
                                        8: "MÉDIA DIA",
                                        9: "STATUS"
                                    })

                                    formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                    for coluna in formatarMoeda:
                                        flash_result[coluna] = flash_result[coluna].apply(format_number)

                                    formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                    for coluna in formatarPorcent:
                                        flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                    # ------ DataFrame para HTML 
                                    table_html = flash_result.to_html(classes='table-style', index=False)
                                    table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>') # Difinindo a classe positivo para aplicar estilos
                                    table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>') # Difinindo a classe negativo para aplicar estilos
                                    table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                    # --- DN
                                    dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                    dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                    dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                    dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                    dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                    dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                    dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                    dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                    dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                    dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                    dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                    dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                    # ----------------- Exibição da tabela -----------------
                                    st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS
                                    st.markdown("<h3 class='dnH3'>TABELA FLASH SUPERVISOR</h3>", unsafe_allow_html=True) # Título da seção
                                    st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit 

                                    # ------------- Tabela Distribuição Numérica ----------
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    st.markdown("<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA SUPERVISOR</h3>", unsafe_allow_html=True)

                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFini, unsafe_allow_html=True)

                                    with col2:
                                        st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                    with col3:
                                        st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFrutap, unsafe_allow_html=True) 
                        



        # -------------------------------- VENDEDOR -------------------------------- # -------------------------------- #
        with aba2_3:
            col1, col2, col3, col4 = st.columns([1.1, 1, 1, 1.60])
            du = diasUteis().values[0][0]
            dd = diasDecorridos().values[0][0]
            velocidade = dd / du
            velStr = str(math.floor(velocidade * 100)) 
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(dias_uteis_result + " DIAS ÚTEIS", unsafe_allow_html=False, help="Quantidade de dias úteis para serem realizadas suas vendas.")
                st.markdown(dias_decor_result + " DECORRIDOS", unsafe_allow_html=False, help="Quantidade de dias úteis decorridos no mês.")
                st.markdown(velStr + "% - VELOCIDADE", unsafe_allow_html=False, help="Velocidade de vendas realizadas no mês.")
            with col1:
                if (velocidade == 0):
                    st.image(path + 'Imagens/0porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0 and velocidade <= 0.10):
                    st.image(path + 'Imagens/10porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.10 and velocidade <= 0.20):
                    st.image(path + 'Imagens/20porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.20 and velocidade <= 0.30):
                    st.image(path + 'Imagens/30porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.30 and velocidade <= 0.40):
                    st.image(path + 'Imagens/40porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.40 and velocidade <= 0.50):
                    st.image(path + 'Imagens/50porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.50 and velocidade <= 0.60):
                    st.image(path + 'Imagens/60porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.60 and velocidade <= 0.70):
                    st.image(path + 'Imagens/70porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.70 and velocidade <= 0.80):
                    st.image(path + 'Imagens/80porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.80 and velocidade <= 0.90):
                    st.image(path + 'Imagens/90porcent.png', width=200, caption='VELOCIDADE')
                elif (velocidade > 0.90 and velocidade <= 1):
                    st.image(path + 'Imagens/100porcent.png', width=200, caption='VELOCIDADE')

            with col3:
                vendedorName = st.selectbox(":man: VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
                if vendedorName == "LEONARDO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (140,),index=0, key='140', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "EDNALDO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (141,),index=0, key='141', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "VAGNER":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (142,),index=0, key='142', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "DEIVID":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (143,),index=0, key='143', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "BISMARCK":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (145,),index=0, key='145', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LUCIANA":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (147,),index=0, key='147', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MATHEUS":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (148,),index=0, key='148', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MARCIO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (150,),index=0, key='150', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LEANDRO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (151,),index=0, key='151', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "REGINALDO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (152,),index=0, key='152', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ROBSON":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (153,),index=0, key='153', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "JOAO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (154,),index=0, key='154', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "TAYANE":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (155,),index=0, key='155', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "MURILO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (156,),index=0, key='156', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "LUCAS":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (157,),index=0, key='157', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "DEYVISON":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (158,),index=0, key='158', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ZEFERINO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (161,),index=0, key='161', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "EPAMINONDAS":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (164,),index=0, key='164', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "GLAUBER":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (167,),index=0, key='167', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "TARCISIO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (168,),index=0, key='168', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "THIAGO":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (169,),index=0, key='169', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "FILIPE":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (170,),index=0, key='170', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "ROMILSON":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (172,),index=0, key='172', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                elif vendedorName == "VALDEME":
                    vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (174,),index=0, key='174', help="Código RCA preenchido com base no nome selecionado acima", placeholder="", disabled=True, label_visibility="visible")
                else:
                    vendedorCod = st.selectbox("ERRO", (999,),index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
            with col4:
                with st.container(height=220, border=False):
                    with st.expander("O que é o Flash?"): 
                        st.write('''
                        O FLASH é um relatório primordial para o acompanhamento de vendas e remuneração.
                        Ele foi criado com objetivo de facilitar o acompanhamento do Vendedor. 
                        Em seu modelo antigo, era necessário atualizar uma planilha Excel de forma manual
                        por alguém apto. ''')
#1000                        
                        st.image("/home/ti_premium/PyDashboards/PremiumDashboards/Imagens/oldFlash.png")
            # -------------------------------- Faturado Apenas ----------------------------------------------
            if notFatOn == False:
                col1, col2 = st.columns([1, 0.12])
                with col2:
                    st.caption("Faturado", help="Apenas pedidos faturados. Essa opção trás um resultados real das vendas. Sempre abatendo devoluções.")
                with col1:
                    col_Carregar, col_gerar_pdf = st.columns([0.15, 1])
                    with col_Carregar:
                        with stylable_container(key="ACESSAR", css_styles=cssButton2):
                            _Carregar = st.button("CARREGAR")
                    with col_gerar_pdf:
                        with stylable_container(key="ACESSAR", css_styles=cssButton2):
                            gerar_pdf = st.button('GERAR PDF', key="flash_pdf")
                    if gerar_pdf:
                        flash_result = flash1464RCA(vendedorCod)
                        flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                            1: "SEÇÃO",
                            2: "OBJETIVO",
                            3: "REALIZADO",
                            4: "ATINGIDO",
                            5: "TENDÊNCIA",
                            6: " R. A. F. ",
                            7: "NECESS. DIA",
                            8: "MÉDIA DIA",
                            9: "STATUS"
                        })

                        formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                        for coluna in formatarMoeda:
                            flash_result[coluna] = flash_result[coluna].apply(format_number)

                        formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                        for coluna in formatarPorcent:
                            flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                        
                        st.markdown(flash_pdf(flash_result), unsafe_allow_html=True)

                    if _Carregar:
                        with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                            # --------------- FAT -----------------------
                            flash_result = flash1464RCA(vendedorCod)
                            # --------------- Troca ---------------------
                            troca_result = trocaRCA(vendedorCod)
                            # --------------- DN  -----------------------
                            formatarPorcent = ['ATINGIDO']
                            # --- DANONE
                            dnFlashDanone = flashDN1464RCA(vendedorCod, 588)
                            if dnFlashDanone.empty:
                                dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- NESTLÉ
                            dnFlashNestle = flashDN1464RCA(vendedorCod, 1841)
                            if dnFlashNestle.empty:
                                dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DANILLA
                            dnFlashDanilla = flashDN1464RCA(vendedorCod, 1658) # Problema com indústrias com mais de 1 CNPJ
                            if dnFlashDanilla.empty:
                                dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SANTA MASSA
                            dnFlashSantaMassa = flashDN1464RCA(vendedorCod, 1623)
                            if dnFlashSantaMassa.empty:
                                dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FINI
                            dnFlashFini = flashDN1464RCA(vendedorCod, 1488)
                            if dnFlashFini.empty:
                                dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SULMINAS
                            dnFlashSulMinas = flashDN1464RCA(vendedorCod, 1321)
                            if dnFlashSulMinas.empty:
                                dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- GULOZITOS
                            dnFlashGulozitos = flashDN1464RCA(vendedorCod, 1719)
                            if dnFlashGulozitos.empty:
                                dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- HYTS
                            dnFlashHyts = flashDN1464RCA(vendedorCod, 1607)
                            if dnFlashHyts.empty:
                                dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FRUTAP
                            dnFlashFrutap = flashDN1464RCA(vendedorCod, 1728)
                            if dnFlashFrutap.empty:
                                dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])   
                            else:
                                dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DAFRUTA
                            dnFlashDaFruta = flashDN1464RCA(vendedorCod, 1225)
                            if dnFlashDaFruta.empty:
                                dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Seara
                            dnFlashSeara = flashDN1464RCA(vendedorCod, 1541)
                            if dnFlashSeara.empty:
                                dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Eco fresh
                            dnFlashEcofresh = flashDN1464RCA(vendedorCod, 1894)
                            if dnFlashEcofresh.empty:
                                dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            
                            dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh, troca_result]
                            if any(df.empty for df in dataframes):
                                st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                            else:
                                with st.container(border=False):
                                    # ----------------- Formatação da tabela -----------------
                                    flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                        1: "SEÇÃO",
                                        2: "OBJETIVO",
                                        3: "REALIZADO",
                                        4: "ATINGIDO",
                                        5: "TENDÊNCIA",
                                        6: " R. A. F. ",
                                        7: "NECESS. DIA",
                                        8: "MÉDIA DIA",
                                        9: "STATUS"
                                    })

                                    formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                    for coluna in formatarMoeda:
                                        flash_result[coluna] = flash_result[coluna].apply(format_number)

                                    formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                    for coluna in formatarPorcent:
                                        flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                    # ------ Troca
                                    troca_result = troca_result.iloc[:, [1, 2,]].rename(columns={
                                        1: " ",
                                        2: "↓"
                                    })

                                    

                                    # ------ DataFrame para HTML 
                                    table_html = flash_result.to_html(classes='table-style', index=False)
                                    table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>') # Difinindo a classe positivo para aplicar estilos
                                    table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>') # Difinindo a classe negativo para aplicar estilos
                                    table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                    # --- TROCA
                                    troca_result = troca_result.to_html(classes='table-dn', index=False)
                                    # --- DN
                                    dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                    dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                    dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                    dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                    dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                    dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                    dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                    dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                    dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                    dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                    dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                    dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                    # ------ Estilos CSS personalizados
                                    with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/flash.css', "r") as file:
                                        flash_css = file.read()
                                    css = f"""
                                    <style>
                                        {flash_css}
                                    </style>
                                    """

                                    # ----------------- Exibição da tabela -----------------
                                    st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS

                                    st.markdown(f"<h3 class='dnH3'>TABELA FLASH VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True) # Título da seção

                                    st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit  

                                    # ------------- Tabela Distribuição Numérica ----------
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    st.markdown(f"<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True)

                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFini, unsafe_allow_html=True)

                                    with col2:
                                        st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                    with col3:
                                        st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFrutap, unsafe_allow_html=True)


                                    # ------------- ITENS DE PERFORMANCE ----------
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    st.markdown(f"<h3 class='dnH3'>ITENS DE PERFORMANCE VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True)
                                    col4, col5, col6 = st.columns(3)
                                    with col5:
                                        st.markdown(f"<p class='dn'>ÍNDICE TROCA {vendedorName}</p>", unsafe_allow_html=True)
                                        st.markdown(troca_result, unsafe_allow_html=True)
                                     


            # -------------------------------- Não Faturado incluso ABATENDO DEVOLUÇÃO ----------------------------------
            elif notFatOn == True and devOn == True:
                col1, col2 = st.columns([1, 0.12])
                with col2:
                    st.caption("Todos", help="Todos os pedidos digitados abatendo devolução (se houver). Essa opção apresenta um resultados mais completo das vendas, mas com sofrerá alterações caso algum pedido não seja faturado, cancelado, ou sofra algum corte.")
                with col1:
                    if st.button("CARREGAR"):
                        with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                            # --------------- NOTFAT -----------------------
                            flash_result = flash322RCA_semDev(vendedorCod)
                            # --------------- Troca ---------------------
                            troca_result = trocaRCA(vendedorCod)
                            # --------------- DN ---------------------------
                            formatarPorcent = ['ATINGIDO']
                            # --- DANONE
                            dnFlashDanone = flashDN322RCA(vendedorCod, 588)
                            if dnFlashDanone.empty:
                                dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- NESTLÉ
                            dnFlashNestle = flashDN322RCA(vendedorCod, 1841)
                            if dnFlashNestle.empty:
                                dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DANILLA
                            dnFlashDanilla = flashDN322RCA(vendedorCod, 1658) # Problema com indústrias com mais de 1 CNPJ
                            if dnFlashDanilla.empty:
                                dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SANTA MASSA
                            dnFlashSantaMassa = flashDN322RCA(vendedorCod, 1623)
                            if dnFlashSantaMassa.empty:
                                dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FINI
                            dnFlashFini = flashDN322RCA(vendedorCod, 1488)
                            if dnFlashFini.empty:
                                dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SULMINAS
                            dnFlashSulMinas = flashDN322RCA(vendedorCod, 1321)
                            if dnFlashSulMinas.empty:
                                dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- GULOZITOS
                            dnFlashGulozitos = flashDN322RCA(vendedorCod, 1719)
                            if dnFlashGulozitos.empty:
                                dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- HYTS
                            dnFlashHyts = flashDN322RCA(vendedorCod, 1607)
                            if dnFlashHyts.empty:
                                dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FRUTAP
                            dnFlashFrutap = flashDN322RCA(vendedorCod, 1728)
                            if dnFlashFrutap.empty:
                                dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])   
                            else:
                                dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DAFRUTA
                            dnFlashDaFruta = flashDN322RCA(vendedorCod, 1225)
                            if dnFlashDaFruta.empty:
                                dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Seara
                            dnFlashSeara = flashDN322RCA(vendedorCod, 1541)
                            if dnFlashSeara.empty:
                                dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Eco fresh
                            dnFlashEcofresh = flashDN322RCA(vendedorCod, 1894)
                            if dnFlashEcofresh.empty:
                                dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            
                            dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh, troca_result]
                            if any(df.empty for df in dataframes):
                                st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                            else:
                                with st.container(border=False):
                                    # ----------------- Formatação da tabela -----------------
                                    flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                        1: "SEÇÃO",
                                        2: "OBJETIVO",
                                        3: "REALIZADO",
                                        4: "ATINGIDO",
                                        5: "TENDÊNCIA",
                                        6: " R. A. F. ",
                                        7: "NECESS. DIA",
                                        8: "MÉDIA DIA",
                                        9: "STATUS"
                                    })

                                    formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                    for coluna in formatarMoeda:
                                        flash_result[coluna] = flash_result[coluna].apply(format_number)

                                    formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                    for coluna in formatarPorcent:
                                        flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                    # ------ Troca
                                    troca_result = troca_result.iloc[:, [1, 2,]].rename(columns={
                                        1: " ",
                                        2: "↓"
                                    })


                                    # ------ DataFrame para HTML 
                                    table_html = flash_result.to_html(classes='table-style', index=False)
                                    table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>') # Difinindo a classe positivo para aplicar estilos
                                    table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>') # Difinindo a classe negativo para aplicar estilos
                                    table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                    # --- TROCA
                                    troca_result = troca_result.to_html(classes='table-dn', index=False)
                                    # --- DN
                                    dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                    dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                    dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                    dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                    dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                    dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                    dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                    dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                    dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                    dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                    dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                    dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                    # ------ Estilos CSS personalizados
                                    with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/flash.css', "r") as file:
                                        flash_css = file.read()
                                    css = f"""
                                    <style>
                                        {flash_css}
                                    </style>
                                    """

                                    # ----------------- Exibição da tabela -----------------
                                    st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS

                                    st.markdown(f"<h3 class='dnH3'>TABELA FLASH VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True) # Título da seção

                                    st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit  

                                    # ------------- Tabela Distribuição Numérica ----------
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    st.markdown(f"<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True)

                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFini, unsafe_allow_html=True)

                                    with col2:
                                        st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                    with col3:
                                        st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFrutap, unsafe_allow_html=True)


                                    # ------------- ITENS DE PERFORMANCE ----------
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    st.markdown(f"<h3 class='dnH3'>ITENS DE PERFORMANCE VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True)
                                    col4, col5, col6 = st.columns(3)
                                    with col5:
                                        st.markdown(f"<p class='dn'>ÍNDICE TROCA {vendedorName}</p>", unsafe_allow_html=True)
                                        st.markdown(troca_result, unsafe_allow_html=True)                                    


            # -------------------------------- Não Faturado incluso COM DEVOLUÇÃO ----------------------------------
            else:
                col1, col2 = st.columns([1, 0.12])
                with col2:
                    st.caption("Irreal", help="Todos os pedidos digitados sem abater devolução. Essa opção apresenta um resultados mais completo das vendas, mas com sofrerá alterações caso algum pedido não seja faturado, cancelado, ou sofra algum corte.")
                with col1:
                    if st.button("CARREGAR"):
                        with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                            # --------------- NOTFAT -----------------------
                            flash_result = flash322RCA(vendedorCod)
                            # --------------- DN ---------------------------
                            formatarPorcent = ['ATINGIDO']
                            # --- DANONE
                            dnFlashDanone = flashDN322RCA(vendedorCod, 588)
                            if dnFlashDanone.empty:
                                dnFlashDanone = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanone = dnFlashDanone.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanone[coluna] = dnFlashDanone[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- NESTLÉ
                            dnFlashNestle = flashDN322RCA(vendedorCod, 1841)
                            if dnFlashNestle.empty:
                                dnFlashNestle = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashNestle = dnFlashNestle.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashNestle[coluna] = dnFlashNestle[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DANILLA
                            dnFlashDanilla = flashDN322RCA(vendedorCod, 1658) # Problema com indústrias com mais de 1 CNPJ
                            if dnFlashDanilla.empty:
                                dnFlashDanilla = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDanilla = dnFlashDanilla.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDanilla[coluna] = dnFlashDanilla[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SANTA MASSA
                            dnFlashSantaMassa = flashDN322RCA(vendedorCod, 1623)
                            if dnFlashSantaMassa.empty:
                                dnFlashSantaMassa = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSantaMassa = dnFlashSantaMassa.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSantaMassa[coluna] = dnFlashSantaMassa[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FINI
                            dnFlashFini = flashDN322RCA(vendedorCod, 1488)
                            if dnFlashFini.empty:
                                dnFlashFini = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashFini = dnFlashFini.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFini[coluna] = dnFlashFini[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- SULMINAS
                            dnFlashSulMinas = flashDN322RCA(vendedorCod, 1321)
                            if dnFlashSulMinas.empty:
                                dnFlashSulMinas = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSulMinas = dnFlashSulMinas.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSulMinas[coluna] = dnFlashSulMinas[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- GULOZITOS
                            dnFlashGulozitos = flashDN322RCA(vendedorCod, 1719)
                            if dnFlashGulozitos.empty:
                                dnFlashGulozitos = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashGulozitos = dnFlashGulozitos.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashGulozitos[coluna] = dnFlashGulozitos[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- HYTS
                            dnFlashHyts = flashDN322RCA(vendedorCod, 1607)
                            if dnFlashHyts.empty:
                                dnFlashHyts = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashHyts = dnFlashHyts.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashHyts[coluna] = dnFlashHyts[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- FRUTAP
                            dnFlashFrutap = flashDN322RCA(vendedorCod, 1728)
                            if dnFlashFrutap.empty:
                                dnFlashFrutap = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])   
                            else:
                                dnFlashFrutap = dnFlashFrutap.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashFrutap[coluna] = dnFlashFrutap[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- DAFRUTA
                            dnFlashDaFruta = flashDN322RCA(vendedorCod, 1225)
                            if dnFlashDaFruta.empty:
                                dnFlashDaFruta = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashDaFruta = dnFlashDaFruta.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashDaFruta[coluna] = dnFlashDaFruta[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Seara
                            dnFlashSeara = flashDN322RCA(vendedorCod, 1541)
                            if dnFlashSeara.empty:
                                dnFlashSeara = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashSeara = dnFlashSeara.rename(columns={ 0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashSeara[coluna] = dnFlashSeara[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            # --- Eco fresh
                            dnFlashEcofresh = flashDN322RCA(vendedorCod, 1894)
                            if dnFlashEcofresh.empty:
                                dnFlashEcofresh = pd.DataFrame([[0, 0, 0, 0]], columns=['OBJETIVO', 'REALIZADO', 'R.A.F.', 'ATINGIDO'])
                            else:
                                dnFlashEcofresh = dnFlashEcofresh.rename(columns={0: 'OBJETIVO', 1: 'REALIZADO', 2: 'R.A.F.', 3: 'ATINGIDO'})
                                for coluna in formatarPorcent:
                                    dnFlashEcofresh[coluna] = dnFlashEcofresh[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))
                            
                            dataframes = [flash_result, dnFlashDanone, dnFlashDanilla, dnFlashSantaMassa, dnFlashFini, dnFlashSulMinas, dnFlashGulozitos, dnFlashHyts, dnFlashFrutap, dnFlashDaFruta, dnFlashSeara, dnFlashEcofresh]
                            if any(df.empty for df in dataframes):
                                st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                            else:
                                with st.container(border=False):
                                    # ----------------- Formatação da tabela -----------------
                                    flash_result = flash_result.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                                        1: "SEÇÃO",
                                        2: "OBJETIVO",
                                        3: "REALIZADO",
                                        4: "ATINGIDO",
                                        5: "TENDÊNCIA",
                                        6: " R. A. F. ",
                                        7: "NECESS. DIA",
                                        8: "MÉDIA DIA",
                                        9: "STATUS"
                                    })

                                    formatarMoeda = ["OBJETIVO", "REALIZADO", " R. A. F. ", "NECESS. DIA", "MÉDIA DIA"]
                                    for coluna in formatarMoeda:
                                        flash_result[coluna] = flash_result[coluna].apply(format_number)

                                    formatarPorcent = ["ATINGIDO", "TENDÊNCIA"]
                                    for coluna in formatarPorcent:
                                        flash_result[coluna] = flash_result[coluna].apply(lambda x: '{:.1f}%'.format(x * 100))

                                    # ------ DataFrame para HTML 
                                    table_html = flash_result.to_html(classes='table-style', index=False)
                                    table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>')
                                    table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>')
                                    table_html = table_html.replace('<td>', '<td class="linha-table">') # Difinindo a classe linha-table para aplicar estilos
                                    # --- DN
                                    dnFlashDanone = dnFlashDanone.to_html(classes='table-dn', index=False)
                                    dnFlashNestle = dnFlashNestle.to_html(classes='table-dn', index=False)
                                    dnFlashDanilla = dnFlashDanilla.to_html(classes='table-dn', index=False)
                                    dnFlashSantaMassa = dnFlashSantaMassa.to_html(classes='table-dn', index=False)
                                    dnFlashFini = dnFlashFini.to_html(classes='table-dn', index=False)
                                    dnFlashSulMinas = dnFlashSulMinas.to_html(classes='table-dn', index=False)
                                    dnFlashGulozitos = dnFlashGulozitos.to_html(classes='table-dn', index=False)
                                    dnFlashHyts = dnFlashHyts.to_html(classes='table-dn', index=False)
                                    dnFlashFrutap = dnFlashFrutap.to_html(classes='table-dn', index=False)
                                    dnFlashDaFruta = dnFlashDaFruta.to_html(classes='table-dn', index=False)
                                    dnFlashSeara = dnFlashSeara.to_html(classes='table-dn', index=False)
                                    dnFlashEcofresh = dnFlashEcofresh.to_html(classes='table-dn', index=False)

                                    # ------ Estilos CSS personalizados
                                    with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/flash.css', "r") as file:
                                        flash_css = file.read()
                                    css = f"""
                                    <style>
                                        {flash_css}
                                    </style>
                                    """

                                    # ----------------- Exibição da tabela -----------------
                                    st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS

                                    st.markdown("<h3 class='dnH3'>TABELA FLASH</h3>", unsafe_allow_html=True) # Título da seção

                                    st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit  

                                    # ------------- Tabela Distribuição Numérica ----------
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    st.markdown("<h3 class='dnH3'>DISTRIBUIÇÃO NUMÉRICA</h3>", unsafe_allow_html=True)

                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.markdown("<p class='dn' id='Danone'>DANONE</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanone, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='danilla'>DANILLA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDanilla, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='santa'>SANTA MASSA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSantaMassa, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='fini'>FINI</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFini, unsafe_allow_html=True)

                                    with col2:
                                        st.markdown("<p class='dn' id='sul'>SULMINAS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSulMinas, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='gulozitos'>GULOZITOS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashGulozitos, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='hyts'>HYTS</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashHyts, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='nestle'>NESTLÉ</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashNestle, unsafe_allow_html=True)

                                    with col3:
                                        st.markdown("<p class='dn' id='dafruta'>DAFRUTA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashDaFruta, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='massa'>SEARA</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashSeara, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='eco'>ECO FRESH</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashEcofresh, unsafe_allow_html=True)

                                        st.markdown("<p class='dn' id='frutap'>FRUTAP</p>", unsafe_allow_html=True)
                                        st.markdown(dnFlashFrutap, unsafe_allow_html=True)



# --------------------------- Vendas ------------------- # ------------------- # ------------------- # ------------------- # ------------------- # 
elif st.session_state['active_tab'] == ':dollar: VENDA':
    with tabs[1]:
        with st.spinner('Carregando dados...'): 
            tm.sleep(1)
        st.divider()
        st.markdown("<br>", unsafe_allow_html=True)
        aba1_1, aba1_2 = st.tabs([":dollar: Resumo", ":money_with_wings: Campanhas"])

    # -------------------------------- # -------------------------------- # -------------------------------- # -------------------------------- #     
        with aba1_2: # Campanhas
            st.markdown("    ")
            with st.expander(":money_with_wings: CAMPANHA GULOZITOS", expanded=True):
                c1g, c2g, c3g = st.columns([0.32, 1.5, 0.001])

                with c1g:
                    campanhaGulao_result = campanhaGulao()
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption(f':blue[Campanha Gulozitos válida até dia 31/ago/2024]')

                with c2g:
                    st.write("Desempenho na Campanha Gulozitos")

                    if campanhaGulao_result.empty:
                        st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos.")
                    else:
                        # Certifique-se de que todas as colunas necessárias estão sendo selecionadas
                        campanhaGulao_result = campanhaGulao_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]].rename(columns={
                            0: "SUP",
                            1: "COD",
                            2: "RCA",
                            3: "BASE",
                            4: "DN",
                            5: "%",
                            6: "TICKET",
                            7: "DN SKU",
                            8: "VOL. SKU",
                            9: "R$"
                        })

                        supervisor_map = {
                            2: "MARCELO",
                            8: "VILMAR JR"
                        }
                        
                        campanhaGulao_result['TICKET'] = campanhaGulao_result['TICKET'].apply(format_number)
                        
                        campanhaGulaoSup_result = campanhaGulao_result.groupby("SUP").sum().sort_values(by="DN", ascending=False).reset_index()

                        campanhaGulao_result = campanhaGulao_result.drop(columns=["SUP"])

                        campanhaGulaoSup_result["Supervisor"] = campanhaGulaoSup_result["SUP"].map(supervisor_map)
                        campanhaGulaoSup_result = campanhaGulaoSup_result.drop(columns=["RCA", "R$", "COD", "SUP", "%", "TICKET", "DN SKU", "VOL. SKU"])
                        cols = ["Supervisor"] + [col for col in campanhaGulaoSup_result.columns if col != "Supervisor"]
                        campanhaGulaoSup_result = campanhaGulaoSup_result[cols]

                        campanhaGulaoSup_result["%"] = campanhaGulaoSup_result.apply(
                            lambda row: f"{int((row['DN'] / row['BASE']) * 100)}%" if row['BASE'] != 0 else "0%", axis=1
                        )

                        campanhaGulaoSup_result["R$"] = campanhaGulaoSup_result.apply(
                            lambda row: (
                                325 if row['BASE'] != 0 and int((row['DN'] / row['BASE']) * 100) >= 55 else
                                300 if row['BASE'] != 0 and int((row['DN'] / row['BASE']) * 100) >= 50 else
                                275 if row['BASE'] != 0 and int((row['DN'] / row['BASE']) * 100) >= 45 else
                                250 if row['BASE'] != 0 and int((row['DN'] / row['BASE']) * 100) >= 40 else
                                225 if row['BASE'] != 0 and int((row['DN'] / row['BASE']) * 100) >= 35 else
                                200 if row['BASE'] != 0 and int((row['DN'] / row['BASE']) * 100) >= 30 else
                                0
                            ), axis=1
                        )
                        
                        container_superior1 = st.container(border=True)
                        colg1, colg2, colg3 = container_superior1.columns([1, 1, 1])   
                                            
                        colg1.metric(label="PREMIAÇÃO TOTAL", help="Valor total somado das premiações dos vendedores", value=format_number((campanhaGulao_result['R$'].sum()+campanhaGulaoSup_result['R$'].sum())))

                        dn_total = campanhaGulao_result["DN"].sum()
                        colg2.metric(label="POSITIVAÇÃO TOTAL", help="Positivações válidas totais da campanha", value=f"{dn_total} PDV's")

                        top_rca = campanhaGulao_result["RCA"].iloc[0]
                        colg3.metric(label="MELHOR DESEMPENHO", help="O melhor desempenho na campanha", value=f'{top_rca}')

                        campanhaGulao_result["R$"] = campanhaGulao_result["R$"].apply(format_number)
                        campanhaGulaoSup_result["R$"] = campanhaGulaoSup_result["R$"].apply(format_number)

                        campanhaGulaoSup_result["BASE"] = campanhaGulaoSup_result["BASE"].astype(str)


                        data_col1, data_col2 = st.columns([1, 0.6])
                        with data_col1:
                            campanhaGulao_result = pd.DataFrame(campanhaGulao_result)
                            st.dataframe(campanhaGulao_result, width=None, use_container_width=True, hide_index=True)

                        with data_col2:
                            campanhaGulaoSup_result.index = campanhaGulaoSup_result.index + 1
                            st.dataframe(campanhaGulaoSup_result, width=None, use_container_width=True)


                with c3g:
                    pass


    
        # -------------------------------- # -------------------------------- # -------------------------------- #
        with aba1_1: # Resumo vendas em Gráficos e tabelas
            st.markdown("<br>", unsafe_allow_html=True)
            containerMain = st.container(border=True)

            with containerMain:
                st.header(":dollar: RESUMO DE VENDAS")
                st.subheader("Legenda:")
                st.markdown("  1. Escolha o período desejado para visualizar os dados.")
                st.markdown("  2. Se atente aos filtros de Supervisor e RCA para visualizar os dados corretamente.")
                st.markdown("  3. Os dados incluem os pedidos não faturados.")

            with containerMain:
                st.divider()
                subcoluna1, subcoluna2, subcoluna3, subcoluna4 = st.columns([0.5, 0.5, 1, 1])
                with subcoluna1:
                    dataIni = st.date_input(":date: Data inicial", value=pd.to_datetime('today') - pd.offsets.MonthBegin(1), format='DD-MM-YYYY', key='DEV3')
                with subcoluna2:
                    dataFim = st.date_input(":date: Data final", value=pd.to_datetime('today'), format='DD-MM-YYYY', key='DEV4')
                
                with subcoluna3:
                    df2_result = df2(dataIni, dataFim)
                    df2_result = df2_result.iloc[:, [0, 1, 2, 3, 4, 5]].rename(columns={
                        0: "CODSUP",
                        1: "SUP",
                        2: "RCA",
                        3: "VALOR",
                        4: "DN",
                        5: "BASE"
                    })

                    sup_list = df2_result.drop(columns=["RCA", "VALOR", "DN", "BASE"])

                    # Adiciona a linha com CODSUP 99 e SUP "TODOS"
                    new_row = pd.DataFrame({"CODSUP": [99], "SUP": ["TODOS"]})
                    sup_list = pd.concat([sup_list, new_row], ignore_index=True)

                    selected_sup = st.selectbox(":male-office-worker: Filtrar Supervisor nos Gráficos", options = sup_list['SUP'].unique().tolist(), index=3, placeholder="Filtro de Supervisor", help="Selecione o supervisor")
                    sup_list_selected = sup_list[sup_list['SUP'].isin([selected_sup])]

                with subcoluna4:
                    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
                    # btn_load = st.button("Carregar Gráficos", key='grafico1', use_container_width=True)
                

                # if btn_load:
                grafico_vend_sup, grafico_top_rca2, grafico_top_rca8, grafico_top_rca9 = gerar_graficoVendas(dataIni, dataFim)

                if sup_list_selected.empty:
                    st.error(":x: Erro ao carregar o gráfico por falta de seleção de supervisor. Por favor, escolha um supervisor. ")
                else:
                    if sup_list_selected["CODSUP"].iloc[0] == 2:
                        st.plotly_chart(grafico_top_rca2, use_container_width=True)
                        df2_result_selected = df2_result[df2_result["CODSUP"] == sup_list_selected["CODSUP"].iloc[0]] # Filtra o dataframe com o supervisor selecionado

                    elif sup_list_selected["CODSUP"].iloc[0] == 8:
                        st.plotly_chart(grafico_top_rca8, use_container_width=True)
                        df2_result_selected = df2_result[df2_result["CODSUP"] == sup_list_selected["CODSUP"].iloc[0]]

                    elif sup_list_selected["CODSUP"].iloc[0] == 9:
                        st.plotly_chart(grafico_top_rca9, use_container_width=True)
                        df2_result_selected = df2_result[df2_result["CODSUP"] == sup_list_selected["CODSUP"].iloc[0]]

                    elif sup_list_selected["CODSUP"].iloc[0] == 99:
                        st.plotly_chart(grafico_vend_sup, use_container_width=True)
                        df2_result_selected = df2_result

                    else: # Aviso de erro
                        st.error(":x: Erro ao carregar o gráfico. Por favor, contate a TI.")

                    qtd_rca = int(df2_result_selected["RCA"].count()) # Quantidade de RCA's

                    containerMetric = st.container(border=True)
                    metric_col1, metric_col2, metric_col3, metric_col4 = containerMetric.columns(4)
                    with metric_col1:
                        total_venda = format_number(df2_result_selected["VALOR"].sum())
                        sup_name = sup_list_selected["SUP"].iloc[0]
                        st.metric(label = "TOTAL EM VENDAS", value = total_venda, delta=f"Sup. {sup_name}", delta_color="off")
                    with metric_col2:
                        media_venda = format_number(df2_result_selected["VALOR"].mean())
                        st.metric(label = "MÉDIA DE VENDAS", value = media_venda, delta="(Linha branca tracejada)", delta_color="off")
                    with metric_col3: 
                        st.metric(label = "MELHOR DESEMPENHO", value = df2_result_selected["RCA"].head(1).iloc[0][6:], delta = "1º")
                    with metric_col4:
                        st.metric(label = "PIOR DESEMPENHO", value = df2_result_selected["RCA"].tail(1).iloc[0][6:], delta = f"{qtd_rca}º", delta_color="inverse")


                # ----------------------------------- # ----------------------------------- # ----------------------------------- #
                st.markdown("<br> <br>", unsafe_allow_html=True)


                # if st.button("Carregar Tabelas", key='tabelas1', use_container_width=True):
                containerTabela = st.container(border=True)

                with containerTabela:
                    
                    subcoluna1 = st.columns([1])[0]
                    with subcoluna1:
                        vendasRca_result = df2(dataIni, dataFim)

                        vendasRca_result = vendasRca_result.iloc[:, [0, 1, 2, 3, 4, 5]].rename(columns={
                        0: "CODSUP",
                        1: "SUP",
                        2: "RCA",
                        3: "VALOR",
                        4: "DN",
                        5: "BASE"
                        })
                        
                        selected_sup = st.multiselect(":male-office-worker: Filtrar Supervisor na Tabela", options = vendasRca_result['SUP'].unique().tolist(), default = None, placeholder="Filtro de Supervisor", help="Selecione o supervisor")
                        filtrado_vendasRca_result = vendasRca_result[vendasRca_result['SUP'].isin(selected_sup)]
                    
                    st.divider()
                    
                    c1, c2 = st.columns([0.6, 1.4])
                    with c1:
                        vendasSup_result = filtrado_vendasRca_result.groupby(["CODSUP", "SUP"])[["VALOR", "DN", "BASE"]].sum().reset_index().sort_values(by='VALOR', ascending=False)
                        vendasSup_result = vendasSup_result.drop(columns=["CODSUP", "BASE"])
                        
                        st.write("Resumo de Vendas por Supervisor")
                        st.dataframe(vendasSup_result, hide_index=True, use_container_width=True, column_config={
                            "VALOR": st.column_config.NumberColumn(
                                "VALOR",
                                format ="R$%d", 
                                help="Total de vendas"
                            ),
                            "DN": st.column_config.NumberColumn(
                                "DN",
                                format ="%.0f", 
                                help="Positivação de PDV's (clientes)"
                            )
                        })
                        st.divider()

                    with c2:
                        filtrado_vendasRca_result = filtrado_vendasRca_result.drop(columns=["CODSUP", "SUP", "BASE"])

                        left, right = st.columns([0.75, 1.25])
                        with left:
                            st.write("Resumo de Vendas por Vendedor")
                            st.dataframe(filtrado_vendasRca_result, hide_index=True, use_container_width=True, column_config={
                                "VALOR": st.column_config.NumberColumn(
                                    "VALOR",
                                    format ="R$%d", # formartar para moeda com 0 casas decimais
                                    help="Total de vendas"
                                ),
                                "DN": st.column_config.NumberColumn(
                                    "DN",
                                    format ="%.0f", 
                                    help="Positivação de PDV's (clientes)"
                                )
                            })
                            st.divider()

                        with right:
                            vendasCli_result = df3(dataIni, dataFim)
                            vendasCli_result = vendasCli_result.iloc[:, [0, 1, 2, 3]].rename(columns={
                                0: "CLIENTE",
                                1: "CODSUP",
                                2: "RCA",
                                3: "VALOR"
                            })

                            selected_rca = st.selectbox(":man: Escolha um RCA", filtrado_vendasRca_result['RCA'].unique(), index=0)
                            filtrado_vendasCli_result = vendasCli_result[vendasCli_result['RCA'].isin([selected_rca])]

                            st.divider()

                            filtrado_vendasCli_result = filtrado_vendasCli_result.drop(columns=["CODSUP", "RCA"])
                            st.write(f"Vendas dos Clientes do RCA {selected_rca}")
                            st.dataframe(filtrado_vendasCli_result, hide_index=True, use_container_width=True, column_config={
                            "VALOR": st.column_config.NumberColumn(
                                "VALOR",                               
                                format ="R$%d", # formartar para moeda com 0 casas decimais
                                help="Total de valor em vendas dos pedidos dos clientes"
                            )
                            })
#2000
                            vendaFornec_result = df4(dataIni, dataFim)
                            vendaFornec_result = vendaFornec_result.iloc[:, [0, 1, 2, 3, 4, 5, 6]].rename(columns={
                                0: "CODFORNEC",
                                1: "FORNECEDOR",
                                2: "CODSUP",
                                3: "SUP",
                                4: "RCA",
                                5: "POSITIVAÇÃO",
                                6: "VALOR"
                            })

                            st.divider()

                            filtrado_vendaFornec_result = vendaFornec_result[vendaFornec_result['RCA'].isin([selected_rca])]

                            filtrado_vendaFornec_result = filtrado_vendaFornec_result.drop(columns=["CODFORNEC", "CODSUP", "SUP", "RCA"])

                            st.write(f"Vendas por Fornecedor do RCA {selected_rca}")
                            st.dataframe(filtrado_vendaFornec_result, hide_index=True, use_container_width=True, column_config={
                                "VALOR": st.column_config.NumberColumn(
                                    "VALOR",
                                    format ="R$%d", # formartar para moeda com 0 casas decimais
                                    help="Total de valor em vendas dos pedidos dos clientes"
                                ),
                                "POSITIVAÇÃO": st.column_config.NumberColumn(
                                    "DN",
                                    format ="%.0f", 
                                    help="Positivação de PDV's (clientes) dos fornecedores"
                                )
                            })

                            st.divider()
                    

    #                st.divider()
    #                ceps_result = ceps()
                    
    #                ceps_list = {'cep': []}
    #                cep_coordenadas = {'lat': [], 'lon': []}

    #                for cep in ceps_result[0]:  
    #                    ceps_list['cep'].append(str(cep)) 

    #                for cep in ceps_list['cep']:
    #                    coordenadas = get_coords_from_cep(cep)
    #                    if coordenadas:
    #                        cep_coordenadas['lat'].append(float(coordenadas[0]))  
    #                        cep_coordenadas['lon'].append(float(coordenadas[1])) 
    #                    else:
    #                        pass

                    # Visualizar no mapa Streamlit
    #                st.map(cep_coordenadas)



# --------------------------- CLIENTES ----------------------------------- # ------------------- # ------------------- # ------------------- # ------------------- # 
elif st.session_state['active_tab'] == ':department_store: CLIENTES':
    with tabs[4]:
        aba4_1, aba4_2 = st.tabs([':convenience_store: GERAL', ':man: POR VENDEDOR'])
        # --------------------------------- GERAL --------------------------------- #
        with aba4_1:
            st.header(":top: 100 CLIENTES", anchor=False)
            dtIni = datetime.today() - timedelta(days=60)
            dtIni = dtIni.strftime("%d/%m/%Y")
            st.caption(" - " + ":blue[60] DIAS CORRIDOS:" + f" :blue[{dtIni}] ATÉ HOJE")
            st.markdown("    ")

            # --------------------------------- RANK TOP 100 --------------------------------- #
            with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR RANK TOP 100", expanded=True):
                # --------------------- Cabeçalho de itens ---------------------
                col1, col2, col3, col4 = st.columns([1, 1, 2, 0.55])
                with col1:
                    supName = st.selectbox(":male-office-worker: SUPERVISOR", ("TODOS", "MARCELO", "VILMAR JR"), index=0, key='sup_3', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
                    if supName == "MARCELO":
                        with col2:
                            supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (2,), index=0, key='MARCELO_3', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                            supOffOn = "IN"     # -- Está em 2
                    elif supName == "VILMAR JR":
                        with col2:
                            supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (8,), index=0, key='vilmar_3', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                            supOffOn = "IN"     # -- Está em 8
                    elif supName == "TODOS":
                        with col2:
                            supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (0,), index=0, key='todos_3', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                            supOffOn = "NOT IN" # -- Não está em 0
                    else:
                        with col2:
                            supCod = st.selectbox("ERRO", (999,), index=0, key='3', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
                
                with col3:
                    st.write("   ")
                    st.write("   ")
                    sorveteOn = st.toggle(":blue[CONSIDERAR PEDIDOS DE SORVETES NO RESULTADO]", help="Selecione para EXIBIR Sorvete e Açaí no resultado", key='sorveteOn')
                st.divider()

                # --------------- Dados Top CLI -----------------------
                with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                    if sorveteOn == False:
                        topCli_result = top100Cli(supCod, 0, 0, 0, supOffOn) #-- Sorvete NÃO Incluso
                    else:
                        topCli_result = top100Cli(supCod, 120430, 120432, 120427, supOffOn) #-- Sorvete Incluso

                # ----------------- Formatação da tabela -----------------
                topCli_result = topCli_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7]].rename(columns={
                    0: "RANK",
                    1: "CODCLI",
                    2: "CLIENTE",
                    3: "VENDEDOR",
                    4: "FATURADO",
                    5: "MÉDIA",
                    6: "BONIFICADO",
                    7: "% BNF"
                })

                formatarMoeda = ["FATURADO", "BONIFICADO", "MÉDIA"]
                for coluna in formatarMoeda:
                    topCli_result[coluna] = topCli_result[coluna].apply(format_number)

                formatarPorcent = ["% BNF"]
                for coluna in formatarPorcent:
                    topCli_result[coluna] = topCli_result[coluna].apply(lambda x: '{:.1f}%'.format(x))
                
                # ------ DataFrame para HTML 
                table_html = topCli_result.to_html(classes='table-styleCli', index=False)

                for i in range(1, 4): # Definindo a classe rank para aplicar estilos
                    table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank{i}">{i}</td>')
                for i in range(4, 11):
                    table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank">{i}</td>')
                

                # ------ Estilos CSS personalizados
                with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                    cli_css = file.read()
                css = f"""
                <style>
                    {cli_css}
                </style>
                """

                # ----------------- Exibição da tabela -----------------
                st.markdown("<h3 class='dnH3'>RANK TOP 100 CLIENTES</h3>", unsafe_allow_html=True) # Título da seção

                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit

                st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS



            # --------------------------------- COMPARATIVO --------------------------------- #
            with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR RANK TOP 100 - COMPARATIVO", expanded=True):
                # --------------------- Cabeçalho de itens ---------------------
                col1, col2, col3, col4 = st.columns([1, 1, 2, 0.55])
                with col1:
                    supName = st.selectbox(":male-office-worker: SUPERVISOR", ("TODOS", "MARCELO", "VILMAR JR"), index=0, key='sup_4', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
                    if supName == "MARCELO":
                        with col2:
                            supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (2,), index=0, key='MARCELO_4', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                            supOffOn = "IN"     # -- Está em 2
                    elif supName == "VILMAR JR":
                        with col2:
                            supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (8,), index=0, key='vilmar_4', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                            supOffOn = "IN"     # -- Está em 8
                    elif supName == "TODOS":
                        with col2:
                            supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (0,), index=0, key='todos_4', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                            supOffOn = "NOT IN" # -- Não está em 0
                    else:
                        with col2:
                            supCod = st.selectbox("ERRO", (999,), index=0, key='3', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
                
                with col3:
                    st.write("   ")
                    st.write("   ")
                    sorveteOn = st.toggle(":blue[CONSIDERAR PEDIDOS DE SORVETES NO RESULTADO]", help="Selecione para EXIBIR Sorvete e Açaí no resultado", key='sorveteOn2')
                st.divider()

                # --------------- Dados Top CLI -----------------------
                with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                    if sorveteOn == False:
                        topCli_result = top100Cli(supCod, 0, 0, 0, supOffOn) #-- Sorvete NÃO Incluso
                        topCliOld_result = top100Cli_comparativo(supCod, 0, 0, 0, supOffOn)
                    else:
                        topCli_result = top100Cli(supCod, 120430, 120432, 120427, supOffOn) #-- Sorvete Incluso
                        topCliOld_result = top100Cli_comparativo(supCod, 120430, 120432, 120427, supOffOn)
                    

                # ----------------- Formatação da tabela -----------------
                topCli_result = topCli_result.iloc[:, [0, 1, 2, 3, 4, 5, 6,]].rename(columns={
                    0: "RANK",
                    1: "CODCLI",
                    2: "CLIENTE",
                    3: "VENDEDOR",
                    4: "ANO ATUAL",
                    5: "INVESTIDO",
                    6: "% INVESTIDA"
                })

                topCliOld_result = topCliOld_result.rename(columns={1: "CODCLI", 4: "ANO ANTERIOR"})

                # Seleção das colunas desejadas de cada dataframe para unir
                topCli_result_selected = topCli_result.iloc[:, [0, 1, 2, 3, 4]]
                topCliOld_result_selected = topCliOld_result.iloc[:, [1, 4]]

                # Une os dois dataframes
                merge_result = pd.merge(topCli_result_selected, topCliOld_result_selected, on="CODCLI")

                # Adiciona uma nova coluna 'GAP' que calcula a diferença entre as colunas 'ANO ATUAL' e 'ANO ANTERIOR'
                merge_result['GAP'] = merge_result['ANO ATUAL'] - merge_result['ANO ANTERIOR']
                # Adiciona uma nova coluna 'TENDENCIA' que compara as colunas 'ANO ATUAL' e 'ANO ANTERIOR'
                merge_result['TENDENCIA'] = np.where(merge_result['ANO ATUAL'] > merge_result['ANO ANTERIOR'], '↑↑↑', '↓↓↓')

                # ------ Formatar Linha
                formatarMoeda = ["ANO ATUAL", "ANO ANTERIOR", 'GAP']
                for coluna in formatarMoeda:
                    merge_result[coluna] = merge_result[coluna].apply(format_number)
                
                # ------ DataFrame para HTML 
                table_html = merge_result.to_html(classes='table-style', index=False)

                for i in range(1, 4): # Definindo a classe rank para aplicar estilos
                    table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank{i}">{i}</td>')
                for i in range(4, 11):
                    table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank">{i}</td>')

                table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivoCli">↑↑↑</td>')
                table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativoCli">↓↓↓</td>')
                

                # ------ Estilos CSS personalizados
                with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                    cli_css = file.read()
                css = f"""
                <style>
                    {cli_css}
                </style>
                """

                # ----------------- Exibição da tabela -----------------
                st.markdown("<h3 class='dnH3'>RANK TOP 100 CLIENTES - COMPARATIVO</h3>", unsafe_allow_html=True) # Título da seção

                st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit

                st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS



        # ------------------------------- POR VENDEDOR ------------------------------ #
        with aba4_2:
            # --------------------------- RANK TOP 10 RCA --------------------------- #
            col1, col2, col3, col4 = st.columns([1.90, 0.75, 0.75, 2.10])
            with col2:
                    vendedorName = st.selectbox(":man: VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca_3', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
                    if vendedorName == "LEONARDO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (140,),index=0, key='140_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "EDNALDO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (141,),index=0, key='141_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "VAGNER":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (142,),index=0, key='142_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "DEIVID":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (143,),index=0, key='143_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "BISMARCK":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (145,),index=0, key='145_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LUCIANA":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (147,),index=0, key='147_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MATHEUS":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (148,),index=0, key='148_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MARCIO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (150,),index=0, key='150_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LEANDRO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (151,),index=0, key='151_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "REGINALDO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (152,),index=0, key='152_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ROBSON":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (153,),index=0, key='153_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "JOAO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (154,),index=0, key='154_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "TAYANE":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (155,),index=0, key='155_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MURILO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (156,),index=0, key='156_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LUCAS":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (157,),index=0, key='157_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "DEYVISON":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (158,),index=0, key='158_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ZEFERINO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (161,),index=0, key='161_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "EPAMINONDAS":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (164,),index=0, key='164_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "GLAUBER":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (167,),index=0, key='167_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "TARCISIO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (168,),index=0, key='168_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "THIAGO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (169,),index=0, key='169_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "FILIPE":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (170,),index=0, key='170_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ROMILSON":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (172,),index=0, key='172_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "VALDEME":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (174,),index=0, key='174_3', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    else:
                        vendedorCod = st.selectbox("ERRO", (999,),index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible") 
            with col1:
                st.markdown("<br>", unsafe_allow_html=True)
            # --------------- Dados Top CLI -----------------------
            with st.expander(f"RANK TOP 10 - {vendedorName}", expanded=True):
                with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                    # ------------- RANK TOP 10 ------------ #
                    topCli2_result = top10CliRCA(vendedorCod)

                    # ------------- Formatação da tabela --- #
                    topCli2_result = topCli2_result.iloc[:, [0, 1, 2, 3, 4, 5, ]].rename(columns={
                        0: "RANK",
                        1: "CODCLI",
                        2: "CLIENTE",
                        3: "FATURADO 60 DIAS",
                        4: "BONIFICADO",
                        5: "% BONIFICADO"
                    })

                    # ------ Formatar REAL e %
                    formatarMoeda = ["FATURADO 60 DIAS", "BONIFICADO"]
                    for coluna in formatarMoeda:
                        topCli2_result[coluna] = topCli2_result[coluna].apply(format_number)

                    formatarPorcent = ["% BONIFICADO"]
                    for coluna in formatarPorcent:
                        topCli2_result[coluna] = topCli2_result[coluna].apply(lambda x: '{:.1f}%'.format(x))

                    # ------ DataFrame para HTML 
                    table_html = topCli2_result.to_html(classes='table-style', index=False)

                    for i in range(1, 4): # Definindo a classe rank para aplicar estilos
                        table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank{i}">{i}</td>')
                    for i in range(4, 11):
                        table_html = table_html.replace(f'<td>{i}</td>', f'<td class="rank">{i}</td>')

                    table_html = table_html.replace('<td>↑↑↑</td>', '<td class="positivo">↑↑↑</td>')
                    table_html = table_html.replace('<td>↓↓↓</td>', '<td class="negativo">↓↓↓</td>')

                    # ------ Estilos CSS personalizados
                    with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                        cli_css = file.read()
                    css = f"""
                    <style>
                        {cli_css}
                    </style>
                    """

                    # ----------------- Exibição da tabela -----------------
                    st.markdown(f"<h3 class='dnH3'>RANK TOP 10 CLIENTES - VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True) # Título da seção
                    
                    st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit
                    
                    st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS

# --------------------------- VERBAS -------------------------------------- # ------------------- # ------------------- # ------------------- # ------------------- # 
elif st.session_state['active_tab'] == ':bank: VERBAS':
    with tabs[5]:
        st.divider()
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([0.5, 1, 3.75])
        with col1:
            btn1 = st.button("CARREGAR", key=4, type="primary")
        with col2:
            senhaSemTratamento = st.text_input("Senha", "", max_chars = 6, type = "password", label_visibility="collapsed", help="Digite a senha numérica para acessar as informações")
        
        senha = bleach.clean(senhaSemTratamento) # Limpa a senha para evitar injeção de código
        
        with col3:
            if senha == "" or len(senha) < 6:
                st.warning("Sem dados para exibir. Verifique a senha inserida.")
            else:
                pass
        if btn1:
            with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                # ------------ Execução da Consulta -----------------
                verbas_result = verbas(senha)

                # ------------ Formatação da tabela -----------------
                verbas_result = verbas_result.iloc[:, [0, 1, 2,]].rename(columns={
                    0: "COD",
                    1: "VENDEDOR",
                    2: "VERBA"
                }).reset_index(drop=True)
                
                formatarMoeda = ["VERBA"]
                for coluna in formatarMoeda:
                    verbas_result[coluna] = verbas_result[coluna].apply(format_number)

                verbas_result = pd.DataFrame(verbas_result.to_dict())

                if verbas_result.empty:
                    with col3:
                        st.warning("Sem dados para exibir. Verifique a senha inserida.")
                else:
                    col1, col2, col3 = st.columns([0.5, 2, 2])
                    with col2:
                        st.dataframe(verbas_result, hide_index=True)
                tm.sleep(1.5)

# --------------------------- DEDO DURO ----------------------------------- # ------------------- # ------------------- # ------------------- # ------------------- # 
elif st.session_state['active_tab'] == ':point_up: DEDO DURO':
    with tabs[6]:

        aba6_1, aba6_2, aba6_3, aba6_4, aba6_5, aba6_6 = st.tabs([":warning: Erros", ":pencil: Pedidos", ":small_red_triangle_down: Devoluções", ":rotating_light: Inadimplência", ":package: Estoque", ":x: Sem Compra"])
        # ---------- ERROS ---------- #
        with aba6_1:
            st.header(":warning: Erros Diversos", anchor=False)
            st.markdown("    ")
            with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:", expanded=True):
                st.divider()
                c1,c2,c3 = st.columns([0.7,1.3,1])
                with c3:
                    pedErro_result = pedErro()
                    pedErro_result = pedErro_result.iloc[:, [0, 1, 2, 3, 4]].rename(columns={
                        0: "CODCLI",
                        1: "COD",
                        2: "NOME",
                        3: "TIPO ERRO",
                        4: "POSIÇÃO"
                    })
                    st.markdown("    ")
                    selected_errors = st.multiselect(label="Filtro de Erros", options = pedErro_result['TIPO ERRO'].unique().tolist(), default = pedErro_result['TIPO ERRO'].unique().tolist(), placeholder="Filtro de erros", help="Selecione o tipo de erro para filtrar na tabela")
                
                filtrado_pedErro_result = pedErro_result[pedErro_result['TIPO ERRO'].isin(selected_errors)]
                with c3:
                
                    st.divider()
                    if st.button('GERAR EXCEL', key="excel_pedErro"): # ---- Convertendo para Excel
                        st.markdown(getTableXls(filtrado_pedErro_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download
                        st.toast('Gerando arquivo Excel...')
                        tm.sleep(.5)


                with c1:
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption(":red[Possível Duplicidade] significa que existe 1 ou mais pedidos do cliente com 1 ou mais itens repetidos.")
                    container2 = st.container(border=True)
                    container2.caption(":red[BNF SEM PEDIDO] se refere a bonificações enviadas, mas sem pedidos de venda no sistema.")
                    container3 = st.container(border=True)
                    container3.caption(":red[PEDIDO ABAIXO DO MÍNIMO] são pedidos que sofreram corte e ficaram com seu valor abaixo de R$100 e por isso não serão enviados ao cliente.")
                    container4 = st.container(border=True)
                    container4.caption(":red[CODCOB != CODPLPAG] significa que a cobrança do cliente está Boleto a Vista.")
                    container5 = st.container(border=True)
                    container5.caption(":red[X Liberado(s), Y BLOQUEADO(s)] se refere a pedidos bloqueados e liberados do mesmo cliente. Onde X é a quantidade de pedidos liberados e Y a quantidade de pedidos bloqueados.")

                with c2:
                    st.write("Tabela de Erros:")
                    if filtrado_pedErro_result.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados.")
                    else:
                        st.dataframe(filtrado_pedErro_result, hide_index=True)


        # ---------- Pedidos -------- #
        with aba6_2:
            st.header(":pencil: Supervisão de Pedidos", anchor=False)
            st.markdown("    ")
            with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:", expanded=True):
                pedCont_result = pedCont()
                st.markdown(f"<h3 class='dnH3'>QUANTIDADE DE PEDIDOS BLOQUEADOS</h3>", unsafe_allow_html=True)
                subcoluna1, subcoluna2, subcoluna3= st.columns([1, 1.5, 1])
                with subcoluna2:
                    # ----------------- Formatação da tabela -----------------
                    pedCont_result = pedCont_result.iloc[:, [0, 1, 2,]].rename(columns={
                        0: "BLOQUEADOS",
                        1: "PENDENTES",
                        2: "BLOQ. + PEND."
                    })    

                    # ------ Exibindo DataFrame para HTML 
                    table_html = pedCont_result.to_html(classes='table-style-bloq', index=False)
                    table_html = table_html.replace('<td>', '<td class="linha-table-bloq">')
                    st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit
                st.divider()
                c1,c2,c3 = st.columns([0.7,1.75,0.7])
                with c3:

                    pedVsEst_result = pedidoVsEstoque()
                    if pedVsEst_result.empty:
                        pass
                    else:
                        pedVsEst_result = pedVsEst_result.iloc[:, [0, 1, 2, 3, 4]].rename(columns={
                            0: "CODPROD",
                            1: "DESCRIÇÃO",
                            2: "PEDIDO",
                            3: "ESTOQUE",
                            4: "CORTE"
                        })
                        minCorte = int(st.number_input("Filtro quantidade mínima considerada", value=1, placeholder="Digite um número mínimo de cortes", step = 1))
                if pedVsEst_result.empty:
                    pass
                else:
                    filtrado_pedVsEst_result = pedVsEst_result[pedVsEst_result["CORTE"].astype(int) >= minCorte]
                    filtrado_pedVsEst_result['CORTE'] = filtrado_pedVsEst_result['CORTE'].astype(str)

                with c1:
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption('A coluna "PEDIDO" mostra as quantidades de itens nos pedidos que estão no sistema.')
                    container2 = st.container(border=True)
                    container2.caption('A coluna "CORTE" é a quantidade de corte após abater o estoque.')
                
                with c2:
                    st.write("TABELA PEDIDO VS ESTOQUE:")
                    if pedVsEst_result.empty:
                        pass
                    else:
                        if filtrado_pedVsEst_result.empty:
                            st.warning("Sem dados para exibir. Verifique os filtros selecionados.")
                        else:
                            st.dataframe(filtrado_pedVsEst_result, hide_index=True)

                with c3:
                    st.divider()
                    if st.button('GERAR EXCEL', key="excel_pedVsEst"): # ---- Convertendo para Excel
                        st.markdown(getTableXls(filtrado_pedVsEst_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download
                        st.toast('Gerando arquivo Excel...')
                        tm.sleep(.5)

        # ---------- Devoluções ----- #
        with aba6_3:
            st.header(":small_red_triangle_down: Devoluções por período", anchor=False)
            st.markdown("    ")
            with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:", expanded=True):
                subcoluna1, subcoluna2, subcoluna3, subcoluna4 = st.columns([0.5, 0.5, 1.1, 0.9])
                with subcoluna1:
                    dataIni = st.date_input(":date: Data inicial", value=pd.to_datetime('today') - pd.offsets.MonthBegin(1), format='DD-MM-YYYY', key='DEV1')
                with subcoluna2:
                    dataFim = st.date_input(":date: Data final", value=pd.to_datetime('today'), format='DD-MM-YYYY', key='DEV2')
                st.divider()
                c1,c2,c3 = st.columns([0.7,2,0.7])
                with c3:
                    devolucao_result = devolucao(dataIni, dataFim)
                    devolucao_result = devolucao_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]].rename(columns={
                        0: "NUMNOTA",
                        1: "NUMCAR",
                        2: "SUP",
                        3: "RCA",
                        4: "CLIENTE",
                        5: "MOTORISTA",
                        6: "VALOR",
                        7: "DEBITO RCA",
                        8: "BNF?",
                        9: "MOTIVO",
                        10: "TIPO",
                        11: "OBSERVAÇÃO"
                    })
                
                with subcoluna3:
                    sup_option = st.multiselect(label=":male-office-worker: Filtro de Supervisor", key="selected_sup", options = nomesSup_result[1].unique().tolist(), default = nomesSup_result[1].unique(), placeholder="Filtro de Supervisor", help="Selecione o supervisor para filtrar na tabela")
                    selected_sup = nomesSup_result[nomesSup_result[1].isin(sup_option)]
                
                with subcoluna4:
                    selected_errors = st.multiselect(label=":small_orange_diamond: Filtro de Tipo", key="selected_errors", options = devolucao_result['TIPO'].unique().tolist(), default = devolucao_result['TIPO'].unique().tolist(), placeholder="Filtro de Tipo", help="Selecione o tipo de devolução para filtrar na tabela")
                    
                    filtrado_devolucao_result = devolucao_result[
                        devolucao_result['TIPO'].isin(selected_errors) & 
                        devolucao_result['SUP'].isin(selected_sup[0])
                    ]

                if filtrado_devolucao_result.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados.")
                else:
                    rca_maior_qtd = filtrado_devolucao_result['RCA'].str[6:].value_counts().idxmax() # RCA que mais aparece na tabela - Retirando os 6 primeiros caracteres

                    mot_maior_qtd = filtrado_devolucao_result['MOTORISTA'].value_counts().idxmax()

                    soma_sup = format_number(filtrado_devolucao_result['VALOR'].sum())
                    soma_total = format_number(devolucao_result['VALOR'].sum())
                    porcent = round((filtrado_devolucao_result['VALOR'].sum() / devolucao_result['VALOR'].sum()) * 100, 1)

                    quantidade_total = devolucao_result['NUMNOTA'].shape[0]
                    quantidade_sup = filtrado_devolucao_result['NUMNOTA'].shape[0]

                    maior_qtd_tipo = filtrado_devolucao_result['MOTIVO'].value_counts().idxmax()

                    formatarMoeda = ["VALOR", "DEBITO RCA"]
                    for coluna in formatarMoeda:
                        filtrado_devolucao_result[coluna] = filtrado_devolucao_result[coluna].apply(format_number)

                st.markdown("    ")

                with c3:
                    st.divider()
                    if st.button('GERAR EXCEL', key="excel_devolucao"): # ---- Convertendo para Excel
                        st.markdown(getTableXls(filtrado_devolucao_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download
                        st.toast('Gerando arquivo Excel...')
                        tm.sleep(.5)

                with c1:
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption("Os valores 'QTD.' são referentes ao total de devoluções por tipo.")
                    container2 = st.container(border=True)
                    container2.caption(":red[Tipo C] significa devoluções por desacordos ou erros :red[Comerciais].")
                    container3 = st.container(border=True)
                    container3.caption(":blue[Tipo L] são devoluções por :blue[Logística].")
                    container5 = st.container(border=True)
                    container5.caption(":orange[Tipo A] se refere a erros :orange[Administrativos].")
                    container6 = st.container(border=True)
                    container6.caption("Tipo O :grey[são devoluções por] Outros Motivos.")
                
                with c2:
                    st.write("DEVOLUÇÕES")
                    container_superior1 = st.container(border=True)
                    
                    if filtrado_devolucao_result.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados.")
                    else:
                        cs1_col1, cs1_col2, cs1_col3, cs1_col4 = container_superior1.columns([1, 1, 1, 1])
                        
                        qtd_dev_com = filtrado_devolucao_result[filtrado_devolucao_result['TIPO'] == 'C'].shape[0]
                        cs1_col1.metric(label=":red[QTD. COMERCIAL]", help="Quantidade total de devoluções por motivos comerciais", value=f"{qtd_dev_com}")

                        qtd_dev_log = filtrado_devolucao_result[filtrado_devolucao_result['TIPO'] == 'L'].shape[0]
                        cs1_col2.metric(label=":blue[QTD. LOGÍSTICO]", help="Quantidade total de devoluções por motivos logísticos", value=f"{qtd_dev_log}")

                        qtd_dev_adm = filtrado_devolucao_result[filtrado_devolucao_result['TIPO'] == 'A'].shape[0]
                        cs1_col3.metric(label=":orange[QTD. ADMINISTRATIVO]", help="Quantidade total de devoluções por motivos administrativos", value=f"{qtd_dev_adm}")

                        qtd_dev_out = filtrado_devolucao_result[filtrado_devolucao_result['TIPO'] == 'O'].shape[0]
                        cs1_col4.metric(label="QTD. OUTROS", help="Quantidade total de devoluções por outros motivos", value=f"{qtd_dev_out}")

                        filtrado_devolucao_result = filtrado_devolucao_result.drop(columns=['SUP'])
                        st.dataframe(filtrado_devolucao_result, hide_index=True, use_container_width=True)

                        container_superior2 = st.container(border=True)
                        cs2_col1, cs2_col2, cs2_col3, cs2_col4 = container_superior2.columns([0.7, 1.1, 1.1, 1.1])

                        cs2_col1.metric(label="QTD. TOTAL", help="Quantidade total de devoluções", value=f"{quantidade_sup}", delta=f"{quantidade_sup} de {quantidade_total}", delta_color="inverse")
                        
                        cs2_col2.metric(label="VALOR TOTAL R$", help="Valor total de devoluções", value=f"{soma_sup}", delta=f"{porcent}% do Total", delta_color="inverse")

                        cs2_col3.metric(label="RCA MAIOR QTD.", help="Vendedor com mais devoluções", value=f"{rca_maior_qtd}")

                        cs2_col4.metric(label="MOT. MAIOR QTD.", help="Motorista com mais devoluções", value=f"{mot_maior_qtd}")

                        left = container_superior2.columns(1)
                        left[0].metric(label="MOTIVO COM MAIS OCORRÊNCIAS", help="Motivo de devolução que mais ocorreu", value=f"{maior_qtd_tipo}")
                        


                        


        # ---------------------------- Inadimplência ---------------------------- #
        with aba6_4:
            st.header(":rotating_light: Inadimplência por Cliente", anchor=False)
            st.markdown("    ")
            with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:", expanded=True):

                st.divider()
                sup_col1, sup_col3 = st.columns([1, 4])
                inad_sup_result = inadimplenciaSup()
                inad_sup_result = inad_sup_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]].rename(columns={
                    0: "SUP",
                    1: "COD",
                    2: "NOME",
                    3: "CLIENTE",
                    4: "PED. NO SISTEMA?",
                    5: "TÍTULO R$",
                    6: "JUROS APROX.",
                    7: "TOTAL R$",
                    8: "COBRANÇA",
                    9: "DIAS EM VENCI.",
                    10: "EMISSAO",
                    11: "VENCIMENTO"
                })

                formatarData = ["EMISSAO", "VENCIMENTO"]
                for coluna in formatarData:
                    inad_sup_result[coluna] = pd.to_datetime(inad_sup_result[coluna]).dt.strftime('%d/%m/%Y')

                sup_maior_inad = inad_sup_result["SUP"].value_counts().idxmax()
                if sup_maior_inad == 2:
                    sup_maior_inad = "MARCELO"
                elif sup_maior_inad == 8:
                    sup_maior_inad = "VILMAR JR"
                else:
                    sup_maior_inad = "JOSEAN"

                with sup_col1:
                    sup_option = st.multiselect(label=":male-office-worker: Filtro de Supervisor", key="selected_sup_inad", options = nomesSup_result[1].unique().tolist(), default = nomesSup_result[1].unique(), placeholder="Filtro de Supervisor", help="Selecione o supervisor para filtrar na tabela")
                    selected_sup = nomesSup_result[nomesSup_result[1].isin(sup_option)]
                    filtrado_inad_sup_result = inad_sup_result[inad_sup_result['SUP'].isin(selected_sup[0])]

                            

                sup_c1, sup_c2 = st.columns([0.5,2])
                with sup_c1:
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption("Selecione o Supervisor acima para visualizar os clientes com débitos na empresa.")

                with sup_col3:
                    container_superior1 = st.container(border=True)
                    cs1_col1, cs1_col2, cs1_col3, cs1_col4 = container_superior1.columns([1, 0.7, 1.1, 1.1])


                with sup_c2:
                    st.write("Tabela de Inadimplentes por Supervisor:")
                    if filtrado_inad_sup_result.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados.")
                    else:
                        vlTotal = filtrado_inad_sup_result["TÍTULO R$"].sum()
                        cs1_col1.metric(label="VALOR TOTAL", help="Valor total da inadimplência listada", value=format_number(vlTotal))

                        qtd_inadimplentes = filtrado_inad_sup_result["CLIENTE"].nunique()
                        cs1_col2.metric(label="QTD. INAD.", help="Quantidade total de clientes inadimplentes", value=qtd_inadimplentes)
                        
                        rca_maior_inad = filtrado_inad_sup_result["NOME"].value_counts().idxmax()
                        cs1_col3.metric(label="MAIOR QTD. INAD.", help="Vendedor com a maior quantidade de inadimplencia", value=rca_maior_inad, delta="1º", delta_color="inverse")
                        
                        soma_por_nome = filtrado_inad_sup_result.groupby("NOME")["TÍTULO R$"].sum()
                        soma_por_nome_ordenado = soma_por_nome.sort_values(ascending=False)
                        nome_maior_valor = soma_por_nome_ordenado.index[0]
                        cs1_col4.metric(label="MAIOR VALOR INAD. R$", help="Vendedor com a maior valor de inadimplencia", value=nome_maior_valor, delta="1º", delta_color="inverse")
                        
                        filtrado_inad_sup_result = filtrado_inad_sup_result.drop(columns=["SUP", "COD"])

                        formatarMoeda = ["TÍTULO R$", "JUROS APROX.", "TOTAL R$"]
                        for coluna in formatarMoeda:
                            filtrado_inad_sup_result[coluna] = filtrado_inad_sup_result[coluna].apply(format_number)
                        
                        st.dataframe(filtrado_inad_sup_result, hide_index=True)





                with stylable_container(key="divider1",css_styles = cssDivider):
                    divider = st.divider() # ---------------------------- Por VENDEDOR ---------------------------- #
                    st.markdown("<br>", unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns([1, 1, 0.55, 2])
                with col1:
                    vendedorName = st.selectbox(":man: VENDEDOR", ("LEONARDO", "JEAN", "DANILO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca_4', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
                    if vendedorName == "LEONARDO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (140,),index=0, key='140_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "JEAN":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (149,),index=0, key='149_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "DANILO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (159,),index=0, key='159_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "EDNALDO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (141,),index=0, key='141_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "VAGNER":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (142,),index=0, key='142_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "DEIVID":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (143,),index=0, key='143_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "BISMARCK":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (145,),index=0, key='145_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LUCIANA":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (147,),index=0, key='147_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MATHEUS":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (148,),index=0, key='148_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MARCIO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (150,),index=0, key='150_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LEANDRO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (151,),index=0, key='151_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "REGINALDO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (152,),index=0, key='152_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ROBSON":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (153,),index=0, key='153_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "JOAO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (154,),index=0, key='154_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "TAYANE":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (155,),index=0, key='155_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MURILO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (156,),index=0, key='156_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LUCAS":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (157,),index=0, key='157_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "DEYVISON":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (158,),index=0, key='158_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ZEFERINO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (161,),index=0, key='161_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "EPAMINONDAS":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (164,),index=0, key='164_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "GLAUBER":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (167,),index=0, key='167_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "TARCISIO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (168,),index=0, key='168_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "THIAGO":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (169,),index=0, key='169_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "FILIPE":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (170,),index=0, key='170_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ROMILSON":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (172,),index=0, key='172_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "VALDEME":
                        with col2:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (174,),index=0, key='174_4', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    else:
                        vendedorCod = st.selectbox("ERRO", (999,),index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible") 

                c1, c2 = st.columns([0.5,2])
                inad_result = inad(vendedorCod)
                inad_result = inad_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]].rename(columns={
                    0: "SUP",
                    1: "RCA",
                    2: "CLIENTE",
                    3: "PED. NO SISTEMA?",
                    4: "TÍTULO R$",
                    5: "JUROS APROX.",
                    6: "TOTAL R$",
                    7: "COBRANÇA",
                    8: "DIAS EM VENCI.",
                    9: "EMISSAO",
                    10: "VENCIMENTO"
                })
                formatarMoeda = ["TÍTULO R$", "JUROS APROX.", "TOTAL R$"]
                for coluna in formatarMoeda:
                    inad_result[coluna] = inad_result[coluna].apply(format_number)

                formatarData = ["EMISSAO", "VENCIMENTO"]
                for coluna in formatarData:
                    inad_result[coluna] = pd.to_datetime(inad_result[coluna]).dt.strftime('%d/%m/%Y')

                inad_result = inad_result.drop(columns=["RCA", "SUP"])

                with c1:
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption("Selecione o vendedor acima para visualizar os clientes com débitos na empresa.")

                with c2:
                    st.write("Tabela de Inadimplentes por Vendedor:")
                    if inad_result.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados.")
                    else:
                        st.dataframe(inad_result, hide_index=True)



        # -------------------- Estoque Gerencial & Cortes de produtos -------------------- #
        with aba6_5:
            st.header(":package: Estoque Gerencial", anchor=False)
            st.markdown("    ")
            containerEstoque = st.container(border=True)

#            with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO SOBRE ESTOQUE :point_down:", expanded=True):
            with containerEstoque:
                # Data atual
                now = datetime.now() - timedelta(days=1) # Data atual menos um dia
                # Mês 0 - Mês Atual
                dtIniMesAtual = now.replace(day=1)
                dtFimMesAtual = now
                # Mês 1 - 1 Mês Antes
                dtIniMes1 = dtIniMesAtual - relativedelta(months=1)
                dtFimMes1 = dtIniMesAtual - relativedelta(days=1)
                # Mês 2 - 2 Meses Antes
                dtIniMes2 = dtIniMes1 - relativedelta(months=1)
                dtFimMes2 = dtIniMes1 - relativedelta(days=1)
                # Mês 3 - 3 Meses Antes
                dtIniMes3 = dtIniMes2 - relativedelta(months=1)
                dtFimMes3 = dtIniMes2 - relativedelta(days=1)
                
                # Converter as datas para strings no formato desejado
                dtIniMesAtual = dtIniMesAtual.strftime('%d-%m-%Y')
                dtFimMesAtual = dtFimMesAtual.strftime('%d-%m-%Y')
                dtIniMes1 = dtIniMes1.strftime('%d-%m-%Y')
                dtFimMes1 = dtFimMes1.strftime('%d-%m-%Y')
                dtIniMes2 = dtIniMes2.strftime('%d-%m-%Y')
                dtFimMes2 = dtFimMes2.strftime('%d-%m-%Y')
                dtIniMes3 = dtIniMes3.strftime('%d-%m-%Y')
                dtFimMes3 = dtFimMes3.strftime('%d-%m-%Y')         

                c2, c3 = st.columns([1.0, 0.4])
                with c3:
                    qtdVendaMes0_result = qtdVendaProd(dtIniMesAtual, dtFimMesAtual)
                    qtdVendaMes0_result = qtdVendaMes0_result.iloc[:, [0, 1,]].rename(columns={
                        0: "CODPROD",
                        1: "MÊS ATUAL",
                    })

                    qtdVendaMes1_result = qtdVendaProd(dtIniMes1, dtFimMes1)
                    qtdVendaMes1_result = qtdVendaMes1_result.iloc[:, [0, 1,]].rename(columns={
                        0: "CODPROD",
                        1: "MÊS 1",
                    })

                    qtdVendaMes2_result = qtdVendaProd(dtIniMes2, dtFimMes2)
                    qtdVendaMes2_result = qtdVendaMes2_result.iloc[:, [0, 1,]].rename(columns={
                        0: "CODPROD",
                        1: "MÊS 2",
                    })

                    qtdVendaMes3_result = qtdVendaProd(dtIniMes3, dtFimMes3)
                    qtdVendaMes3_result = qtdVendaMes3_result.iloc[:, [0, 1,]].rename(columns={
                        0: "CODPROD",
                        1: "MÊS 3",
                    })

                    estoque266_result = estoque266()
                    estoque266_result = estoque266_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]].rename(columns={
                        0: "CODPROD",
                        1: "DTULTENT",
                        2: "DESCRICAO",
                        3: "CODFORNEC",
                        4: "FORNECEDOR",
                        5: "EMBALAGEM",
                        6: "QTDULTENT",
                        7: "UN MASTER",
                        8: "QTEST",
                        9: "QTD EST",
                        10: "CUSTO EST.",
                        11: "R$ EST.",
                        12: "QTBLOQMENOSAVARIA",
                        13: "QTD EST CX", # QTD ESTOQUE / UN. MASTER = QTD CAIXA
                    })

                    estoque266_result = estoque266_result.drop(columns=["QTBLOQMENOSAVARIA", "QTEST", "UN MASTER"])

                    formatarData = ["DTULTENT"]
                    for coluna in formatarData:
                        estoque266_result[coluna] = pd.to_datetime(estoque266_result[coluna]).dt.strftime('%d/%m/%Y')

                    #formatarMoeda = ["CUSTO EST.", "R$ EST."]  ### Formatação alterada para st.column_config.NumberColumn 
                    #for coluna in formatarMoeda:
                        #estoque266_result[coluna] = estoque266_result[coluna].apply(format_number)                        
                    

                    estoque266_result = estoque266_result.merge(qtdVendaMes3_result, on='CODPROD', how='left').fillna('0')
                    estoque266_result = estoque266_result.merge(qtdVendaMes2_result, on='CODPROD', how='left').fillna('0')
                    estoque266_result = estoque266_result.merge(qtdVendaMes1_result, on='CODPROD', how='left').fillna('0')
                    estoque266_result = estoque266_result.merge(qtdVendaMes0_result, on='CODPROD', how='left').fillna('0')

                    estoque266_result = estoque266_result.assign(QTDVENDDIA = lambda x: ((((x['MÊS ATUAL'].astype(float)) + 
                                                                        (x['MÊS 1'].astype(float)) + 
                                                                        (x['MÊS 2'].astype(float)) + 
                                                                        (x['MÊS 3'].astype(float))) / 4) / 30).round(0).astype(int))

                    estoque266_result = estoque266_result.assign(QTDESTDIA = lambda x: ((x["QTD EST"].astype(float) / 
                                                                                        x["QTDVENDDIA"].astype(float)).fillna(0).replace([np.inf, -np.inf], 0).round(0).astype(int)))
                    
                    estoque266_result['QTDVENDDIA'] = estoque266_result['QTDVENDDIA'].astype(float).round(0).astype(int)
                    
                    estoque266_result['QTDESTDIA'] = estoque266_result['QTDESTDIA'].astype(float).round(0).astype(int)
                    
                    st.markdown("    ")
                    fornecedores = nomesFornec_result # '0': Código | '1': Fantasia | '2': Razão Social 
                    selected_fornec = st.selectbox(label=":factory: Filtro de Fornecedor", options=fornecedores[1].unique().tolist(), index=0, placeholder="Filtro de Fornecedor", help="Selecione para filtrar na tabela")
                    fonecedor_selected = fornecedores[fornecedores[1].isin([selected_fornec])]
                    codFornec = fonecedor_selected[0].iloc[0]
                    nomeFornec = fonecedor_selected[2].iloc[0]

                    filtrado_estoque266_result = estoque266_result[estoque266_result['FORNECEDOR'].isin([nomeFornec])]
                    filtrado_estoque266_result = filtrado_estoque266_result.drop(columns=["FORNECEDOR", "CODFORNEC"])
                    filtrado_estoque266_result = filtrado_estoque266_result.sort_values(by='QTDESTDIA', ascending=False)
                    filtrado_estoque266_result[['QTDULTENT']] = filtrado_estoque266_result[['QTDULTENT']].fillna(0).replace([np.inf, -np.inf], 0)
                    filtrado_estoque266_result[['QTDULTENT']] = filtrado_estoque266_result[['QTDULTENT']].astype(float).round(0).astype(int).astype(str)
                    
                    percent_sem_venda = filtrado_estoque266_result.shape[0] # Coleta do DF para usar mais a frente


                    min_QTDESTDIA = int(filtrado_estoque266_result["QTDESTDIA"].min())
                    max_QTDESTDIA = int(filtrado_estoque266_result["QTDESTDIA"].max())
                    faixa = st.slider(":package: Faixa de Quantidade de Estoque Dia.", value=[min_QTDESTDIA, max_QTDESTDIA], min_value=0, max_value=max_QTDESTDIA, step=1, key="slider_estoque", help="Selecione o valor do estoque dia para filtrar na tabela")
                    if faixa:
                        with st.spinner(':package: Carregando...'):
                            filtrado_estoque266_result = filtrado_estoque266_result[(filtrado_estoque266_result['QTDESTDIA'] >= faixa[0]) & (filtrado_estoque266_result['QTDESTDIA'] <= faixa[1])]
                            tm.sleep(3)

#3000                
                with c3:
                    st.divider()
                    colunaExcel, colunaPdf = st.columns([1, 1])
                    with colunaExcel:
                        if st.button('GERAR EXCEL', key="excel_estoque"): # ---- Convertendo para Excel
                            st.toast('Gerando arquivo Excel...')
                            tm.sleep(.5)
                            st.markdown(getTableXls(filtrado_estoque266_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download
                    with colunaPdf:
                        if st.button('GERAR PDF', key="pdf_estoque"):
                            st.toast('Gerando arquivo PDF...')
                            tm.sleep(.5)
                            # Formatando a tabela para impressão em PDF
                            filtrado_estoque266_result_pdf = filtrado_estoque266_result
                            filtrado_estoque266_result_pdf = filtrado_estoque266_result_pdf.drop(columns=["QTD EST CX", "EMBALAGEM"])
                            filtrado_estoque266_result_pdf['DESCRICAO'] = filtrado_estoque266_result_pdf['DESCRICAO'].apply(lambda x: x[:12] if isinstance(x, str) else x)

                            st.markdown(getTablePdf(filtrado_estoque266_result_pdf), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download em PDF
                
                with c2:   
                    st.write("Estoque Gerencial:")
                    container_superior2 = st.container(border=True)
                    cs1_col1, cs1_col2, cs1_col3, cs2_col4 = container_superior2.columns([0.5, 0.5, 1, 1])
                    
                    if filtrado_estoque266_result.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados")
                    else:
                        cs1_col1.metric(label="QTD. SKU's", help="Quantidade total de produtos diferentes", value=(filtrado_estoque266_result.shape[0]))

                        media_estDia = filtrado_estoque266_result["QTDESTDIA"].mean()
                        media_estDia = f"{media_estDia:.0f}"
                        cs1_col2.metric(label="MÉD. EST. DIA", help="Média de estoque dia dos itens do fornecedor", value=media_estDia)

                        custo_tot = filtrado_estoque266_result["CUSTO EST."].sum()
                        cs1_col3.metric(label="CUSTO TOTAL", help="Custo total dos produtos em estoque", value=format_number(custo_tot))
                        
                        valor_tot = filtrado_estoque266_result["R$ EST."].sum()
                        cs2_col4.metric(label="VALOR TOTAL", help="Valor total de venda dos produtos em estoque", value=format_number(valor_tot))

                        filtrado_estoque266_result = filtrado_estoque266_result.drop(columns=["QTD EST CX"])
                        st.dataframe(filtrado_estoque266_result, hide_index=True, use_container_width=True, column_config={
                            "CODPROD": st.column_config.NumberColumn(
                                help="CÓDIGO DO PRODUTO",
                                format="%d"
                            ),
                            "DTULTENT": st.column_config.TextColumn(
                                help="DATA DO PRODUTO"
                            ),
                            "DESCRICAO": st.column_config.TextColumn(
                                help="NOME DO PRODUTO E SUA DESCRIÇÃO"
                            ),
                            "QTDULTENT": st.column_config.NumberColumn(
                                help="QUANTIDADE DA ÚLTIMA ENTRADA",
                                format="%d"
                            ),
                            "QTD EST": st.column_config.NumberColumn(
                                help="QUANTIDADE EM ESTOQUE DO PRODUTO",
                                format="%d"
                            ),
                            "CUSTO EST.": st.column_config.NumberColumn(
                                help="CUSTO TOTAL DOS PRODUTOS EM ESTOQUE",
                                format="R$%d"
                            ),
                            "R$ EST.": st.column_config.NumberColumn(
                                "VALOR EST.",
                                help="VALOR DE TABELA TOTAL DOS PRODUTOS EM ESTOQUE",
                                format="R$%d"
                            ),
                            "MÊS 3": st.column_config.NumberColumn(
                                help="VENDAS DO PRODUTO NO MÊS 3 (3º MÊS ANTERIOR AO ATUAL)",
                                format="%d"
                            ),
                            "MÊS 2": st.column_config.NumberColumn(
                                help="VENDAS DO PRODUTO NO MÊS 2 (2º MÊS ANTERIOR AO ATUAL)",
                                format="%d"
                            ),
                            "MÊS 1": st.column_config.NumberColumn(
                                help="VENDAS DO PRODUTO NO MÊS 1 (1º MÊS ANTERIOR AO ATUAL)",
                                format="%d"
                            ),
                            "MÊS ATUAL": st.column_config.NumberColumn(
                                help="VENDAS DO PRODUTO NO MÊS ATUAL",
                                format="%d"
                            ),
                            "QTDVENDDIA": st.column_config.NumberColumn(
                                help="QUANTIDADE VENDIDA POR DIA DESSE PRODUTO COM BASE NO HISTÓRICO",
                                format="%d"
                            ),
                            "QTDESTDIA": st.column_config.NumberColumn(
                                help="DIAS DE ESTOQUE COM BASE NA VENDA DIA DO PRODUTO E NO ESTOQUE ATUAL",
                                format="%d"
                            )
                        })

                st.divider() # ----------- Produtos sem venda
                c1_2, c2_2, c3_2 = st.columns([0.6,1.5,1])
                with c3_2:
                    prodSemVenda_result = prodSemVenda(codFornec)
                    if prodSemVenda_result.empty:
                        pass
                    else:
                        prodSemVenda_result = prodSemVenda_result.iloc[:, [0, 1, 2, 3, 4, 5]].rename(columns={
                            0: "CODPROD",
                            1: "DESCRICAO",
                            2: "DTULTENT",
                            3: "QTDULTENT",
                            4: "ESTOQUE",
                            5: "DIAS SEM VENDA"
                        })
                        # Extraindo os valores numéricos dos primeiros caracteres da coluna "DIAS SEM VENDA"
                        prodSemVenda_result["ORDER"] = prodSemVenda_result["DIAS SEM VENDA"].str.extract(r'(\d+)').astype(int)
                        
                        # Ordenando o DataFrame pelo valor numérico extraído em ordem decrescente
                        prodSemVenda_result = prodSemVenda_result.sort_values(by="ORDER", ascending=False)
                    
                    st.divider()
                    colunaExcel, colunaPdf = st.columns([0.6, 1])
                    with colunaExcel:
                        if st.button('GERAR EXCEL', key="excel_prodSemVenda"): # ---- Convertendo para Excel
                            st.toast('Gerando arquivo Excel...')
                            tm.sleep(.5)
                            st.markdown(getTableXls(prodSemVenda_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download
                    with colunaPdf:
                        if st.button('GERAR PDF', key="pdf_prodSemVenda"):
                            st.toast('Gerando arquivo PDF...')
                            tm.sleep(.5)
                            prodSemVenda_result_pdf = prodSemVenda_result
                            # Formatando a tabela para impressão em PDF
                            prodSemVenda_result_pdf['DESCRICAO'] = prodSemVenda_result_pdf['DESCRICAO'].apply(lambda x: x[:20] if isinstance(x, str) else x)

                            st.markdown(getTablePdf(prodSemVenda_result_pdf), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download em PDF
                
                with c2_2:
                    st.write("Produtos Sem Venda:")
                    container_superior2 = st.container(border=True)
                    cs2_col1, cs2_col2, cs2_col3 = container_superior2.columns([1, 1, 1])
                    
                    if prodSemVenda_result.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados")
                    else:
                        cs2_col1.metric(label="ITENS SEM VENDA", help="Quantidade total de produtos sem venda", value=(prodSemVenda_result.shape[0]))

                        percent_sem_venda = (prodSemVenda_result.shape[0] / percent_sem_venda) * 100
                        percent_sem_venda_formatado = f"{percent_sem_venda:.0f}%"
                        cs2_col2.metric(label="% SEM VENDA", help="Porcentagem de itens sem venda", value=percent_sem_venda_formatado)

                        qtdtotal = prodSemVenda_result["ESTOQUE"].astype(int).sum()
                        cs2_col3.metric(label="QTD. ESTOQUE", help="Quantidade total de itens parados no estoque", value=qtdtotal)

                        # Nova ordem das colunas

                        ordem_col = ["CODPROD", "DESCRICAO", "DIAS SEM VENDA", "DTULTENT", "QTDULTENT", "ESTOQUE"]
                        prodSemVenda_result = prodSemVenda_result[ordem_col]

                        st.dataframe(prodSemVenda_result, hide_index=True)

                with c1_2:
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption(f'Produtos sem venda a mais de 7 dias do Fornecedor {codFornec}')

            st.markdown("<br>", unsafe_allow_html=True)
            with stylable_container(key="divider1",css_styles = cssDivider):
                divider = st.divider() # ---------------------------------------- Cortes Por Fornecedor (indústria)
                st.markdown("<br>", unsafe_allow_html=True)
            st.header(":x: Painel de Cortes", anchor=False)
            st.markdown("    ")
            containerCorte = st.container(border=True)

            

#            with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO SOBRE CORTES :point_down:", expanded=True):
            with containerCorte:
                c1_3, c2_3, c3_3 = st.columns([0.6,1.5,1])

                with c3_3:
                    st.write("   ")
                    hoje = datetime.now() 
                    dtIniMesAtual = hoje.replace(day=1) 
                    dia1 = dtIniMesAtual - relativedelta(months=6) 

                    selected_data = st.date_input(
                        ":date: Data Inicial e Final",
                        (dtIniMesAtual, hoje),
                        dia1,
                        hoje,
                        format="DD/MM/YYYY",
                        help='Digite a data inicial e final separados por um traço - ',
                        key='selected_data1'
                    )
                     # Formatar as datas para o formato esperado
                    data_inicial = selected_data[0].strftime('%d-%m-%Y')
                    data_final = selected_data[1].strftime('%d-%m-%Y')
                    
                    sup_colum1, sup_colum2 = st.columns([1, 1])
                    with sup_colum1:
                        supName = st.selectbox(":male-office-worker: SUPERVISOR", ("TODOS", "MARCELO", "VILMAR JR", "JOSEAN"), index=0, key='sup_7', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
                        if supName == "MARCELO":
                            with sup_colum2:
                                supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (2,), index=0, key='MARCELO_7', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                supOnOff = "IN"     # -- Está em 2
                        elif supName == "VILMAR JR":
                            with sup_colum2:
                                supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (8,), index=0, key='vilmar_7', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                supOnOff = "IN"     # -- Está em 8
                        elif supName == "JOSEAN":
                            with sup_colum2:
                                supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (9,), index=0, key='josean_7', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                supOnOff = "IN"     # -- Está em 8
                        elif supName == "TODOS":
                            with sup_colum2:
                                supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (0,), index=0, key='todos_7', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                supOnOff = "NOT IN" # -- Não está em 0
                        else:
                            with sup_colum2:
                                supCod = st.selectbox("ERRO", (999,), index=0, key='3', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
                                supOnOff = "IN" 
                    cortes_Fornec = cortesFornec(data_inicial, data_final, supOnOff, supCod)
                    st.divider()

                
                with c2_3:
                    if cortes_Fornec.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados")
                    else:
                        st.write("Corte por Equipes e Fornecedores:")
                        cortes_Fornec = cortes_Fornec.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8]].rename(columns={
                            0: "CODSUPERVISOR", # CÓDIGO SUPERVISOR
                            1: "CODFORNEC", # CÓDIGO FORNECEDOR
                            2: "FORNECEDOR", # NOME FORNECEDOR
                            3: "CODPROD", # CÓDIGO PRODUTO
                            4: "DESCRICAO", # DESCRICAO DO PRODUTO
                            5: "QTD. PEDIDO", # QUANTIDADE SOMADO DO PRODUTO EM TODOS PEDIDOS
                            6: "QTD. CORTE", # QUANTIDADE SOMADO DOS CORTES DO PRODUTO
                            7: "%", # PORCENTAGEM DE CORTE
                            8: "R$" # QUANTIDADE DE CORTES VEZES O VALOR DO PRODUTO
                        })

                        # cortesfornec_result = "CODFORNEC", "FORNECEDOR", "CORTE TOTAL" QUE É A SOMA DE TODOS OS CORTES DE TODOS PRODUTOS, "TOTAL R$" QUE É A SOMA DA COLUNA "R$" DO cortes_Fornec
                        cortesFornec_result = cortes_Fornec.groupby(["CODFORNEC", "FORNECEDOR"]).agg({"QTD. CORTE": "sum", "R$": "sum"}).reset_index()
                        cortesFornec_result = cortesFornec_result.rename(columns={
                            "CODFORNEC": "CODFORNEC", # CÓDIGO FORNECEDOR
                            "FORNECEDOR": "FORNECEDOR", # NOME FORNECEDOR
                            "QTD. CORTE": "CORTE TOTAL", # QUANTIDADE SOMADO DOS CORTES DO PRODUTO DE CADA FORNECEDOR
                            "R$": "R$" # QUANTIDADE DE CORTES VEZES O VALOR DO PRODUTO
                        }).sort_values(by="R$", ascending=False)


                        container_superior3 = st.container(border=True)
                        cs3_col1, cs3_col2, cs3_col3 = container_superior3.columns([1, 1, 1])
                        
                        cs3_col1.metric(label="VALOR MEDIANO", help="A mediana é o valor central de um conjunto de dados ordenados", value=format_number(cortesFornec_result["R$"].median()))
                        
                        qtdtotal_corte = cortesFornec_result["CORTE TOTAL"].sum()

                        cs3_col2.metric(label="QTD. CORTES", help="Quantidade total somada em unidades", value=qtdtotal_corte)
                        
                        vltotal_corte = format_number(cortesFornec_result['R$'].sum())
                        cs3_col3.metric(label="VALOR EM CORTES", help="Valor total somado dos fornecedores", value=vltotal_corte)
                        
                        # Aplicar format_number a cada valor da coluna "R$"
                        cortesFornec_result["R$"] = cortesFornec_result["R$"].apply(format_number)
                        cortesFornec_result["CODFORNEC"] = cortesFornec_result["CODFORNEC"].astype(str)
                        cortesFornec_result["CORTE TOTAL"] = cortesFornec_result["CORTE TOTAL"].astype(str)

                        st.dataframe(cortesFornec_result, hide_index=True)



                with c1_3:
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption(f'Quantidades de Cortes por Fornecedor')

                
                st.divider() # ----------- Cortes Por supervisor (equipe)

                c1_3, c2_3, c3_3 = st.columns([0.6,1.5,1])

                with c3_3:
                    st.write("   ")
                    fornecedores = nomesFornec_result # '0': Código | '1': Fantasia | '2': Razão Social 
                    selected_fornec = st.selectbox(label=":factory: Filtro de Fornecedor", key="selected_fornec2", options=fornecedores[1].unique().tolist(), index=0, placeholder="Filtro de Fornecedor", help="Selecione para filtrar na tabela")
                    fonecedor_selected = fornecedores[fornecedores[1].isin([selected_fornec])]
                    codFornec = fonecedor_selected[0].iloc[0]
                    nomeFornec = fonecedor_selected[2].iloc[0]

                    filtrado_estoque266_result = estoque266_result[estoque266_result['FORNECEDOR'].isin([nomeFornec])]
                    codFornec = filtrado_estoque266_result["CODFORNEC"].iloc[0]
                    nomeFornec = filtrado_estoque266_result["FORNECEDOR"].iloc[0]

                    selected_data = st.date_input(
                        ":date: Data Inicial e Final",
                        (dtIniMesAtual, hoje),
                        dia1,
                        hoje,
                        format="DD/MM/YYYY",
                        help='Digite a data inicial e final separados por um traço - ',
                        key='selected_data2'
                    )
                     # Formatar as datas para o formato esperado
                    data_inicial = selected_data[0].strftime('%d-%m-%Y')
                    data_final = selected_data[1].strftime('%d-%m-%Y')
                    cortesEquipe_result = cortesEquipe(codFornec, data_inicial, data_final)

                    if cortesEquipe_result.empty:
                        pass
                    else:
                        cortesEquipe_result = cortesEquipe_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7]].rename(columns={
                            0: "CODPROD",
                            1: "DESCRICAO",
                            2: "QTD. PEDIDO",
                            3: "QTD. CORTE",
                            4: "%",
                            5: "R$",
                            6: "CODSUPERVISOR",
                            7: "CODFORNEC",
                        })

                    sup_colum1, sup_colum2 = st.columns([1, 1])
                    with sup_colum1:
                        supName = st.selectbox(":male-office-worker: SUPERVISOR", ("MARCELO", "VILMAR JR", "JOSEAN"), index=0, key='sup_6', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
                        if supName == "MARCELO":
                            with sup_colum2:
                                supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (2,), index=0, key='MARCELO_6', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                supOnOff = "IN"     # -- Está em 2
                        elif supName == "VILMAR JR":
                            with sup_colum2:
                                supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (8,), index=0, key='vilmar_6', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                supOnOff = "IN"     # -- Está em 8
                        elif supName == "JOSEAN":
                            with sup_colum2:
                                supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (9,), index=0, key='josean_6', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                supOnOff = "IN"     # -- Está em 9
                        else:
                            with sup_colum2:
                                supCod = st.selectbox("ERRO", (999,), index=0, key='3', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")


                    st.divider()

                with c1_3:
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption(f'Quantidades de Cortes por Produto')

                with c2_3:
                    if cortesEquipe_result.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados")
                    else:
                        valor_total_corte_fornec = format_number(cortesEquipe_result['R$'].sum())

                        filtrado_cortesEquipe_result = cortesEquipe_result[(cortesEquipe_result["CODSUPERVISOR"] == supCod)]
                        filtrado_cortesEquipe_result = filtrado_cortesEquipe_result.drop(columns=["CODSUPERVISOR", "CODFORNEC"]).sort_values(by="R$", ascending=False)
                        
                        # Formatar a coluna R$ para a moeda brasileira
                        filtrado_cortesEquipe_result['R$'] = filtrado_cortesEquipe_result['R$'].apply(lambda x: format_currency(x, 'BRL', locale='pt_BR.UTF-8'))
                        # Converter a coluna R$ para float 
                        filtrado_cortesEquipe_result['R$'] = filtrado_cortesEquipe_result['R$'].apply(lambda x: float(x.replace('R$', '').replace('.', '').replace(',', '.')))
                        # Converter a coluna QTD. CORTE para inteiro
                        filtrado_cortesEquipe_result['QTD. CORTE'] = filtrado_cortesEquipe_result['QTD. CORTE'].astype(int)

                        st.write(f"Corte por Equipe e Produtos - {supName}:")
                        container_superior4 = st.container(border=True)
                        cs4_col1, cs4_col2, cs4_col3 = container_superior4.columns([1, 1, 1])
                        cs4_col1.metric(label="VALOR MEDIANO", help="A mediana é o valor central de um conjunto de dados ordenados", value=format_number(filtrado_cortesEquipe_result['R$'].median()))
                        cs4_col2.metric(label="QTD. CORTES EQUIPE", help="Quantidade total somada", value=filtrado_cortesEquipe_result["QTD. CORTE"].sum())
                        cs4_col3.metric(label="VALOR CORTADO EQUIPE", help="Valor total somado", value=format_number(filtrado_cortesEquipe_result['R$'].sum()))
                        
                        # Aplicar format_number a cada valor da coluna "R$"
                        filtrado_cortesEquipe_result["R$"] = filtrado_cortesEquipe_result["R$"].apply(format_number)
                        filtrado_cortesEquipe_result["CODPROD"] = filtrado_cortesEquipe_result["CODPROD"].astype(str)
                        filtrado_cortesEquipe_result["QTD. PEDIDO"] = filtrado_cortesEquipe_result["QTD. PEDIDO"].astype(str)
                        filtrado_cortesEquipe_result["QTD. CORTE"] = filtrado_cortesEquipe_result["QTD. CORTE"].astype(str)
                        filtrado_cortesEquipe_result = filtrado_cortesEquipe_result.drop(columns=["QTD. PEDIDO"])

                        st.dataframe(filtrado_cortesEquipe_result, hide_index=True)



        # ---------- SEM COMPRA ---------- #
        with aba6_6:
            st.header(":x: Clientes Sem Compra", anchor=False)
            st.markdown("    ")
            with st.expander(":red[CLIQUE AQUI] PARA VISUALIZAR O RELATÓRIO DO DEDO DURO :point_down:", expanded=True):
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1.1, 1, 1])
                with col1:
                        vendedorName = st.selectbox(":man: VENDEDOR", ("TODOS", "LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca_6', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
                        if vendedorName == "TODOS":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (0,),index=0, key='0_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "NOT IN"
                        elif vendedorName == "LEONARDO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (140,),index=0, key='140_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "EDNALDO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (141,),index=0, key='141_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "VAGNER":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (142,),index=0, key='142_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "DEIVID":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (143,),index=0, key='143_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "BISMARCK":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (145,),index=0, key='145_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "LUCIANA":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (147,),index=0, key='147_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "MATHEUS":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (148,),index=0, key='148_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "MARCIO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (150,),index=0, key='150_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "LEANDRO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (151,),index=0, key='151_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "REGINALDO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (152,),index=0, key='152_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "ROBSON":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (153,),index=0, key='153_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "JOAO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (154,),index=0, key='154_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "TAYANE":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (155,),index=0, key='155_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "MURILO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (156,),index=0, key='156_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "LUCAS":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (157,),index=0, key='157_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "DEYVISON":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (158,),index=0, key='158_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "ZEFERINO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (161,),index=0, key='161_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "EPAMINONDAS":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (164,),index=0, key='164_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "GLAUBER":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (167,),index=0, key='167_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "TARCISIO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (168,),index=0, key='168_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "THIAGO":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (169,),index=0, key='169_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "FILIPE":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (170,),index=0, key='170_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "ROMILSON":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (172,),index=0, key='172_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        elif vendedorName == "VALDEME":
                            with col2:
                                vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (174,),index=0, key='174_6', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                rcaOnOff = "IN"
                        else:
                            vendedorCod = st.selectbox("ERRO", (999,),index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible") 
                        
                        if vendedorCod == 0:
                            with col4:
                                supName = st.selectbox(":male-office-worker: SUPERVISOR", ("TODOS", "MARCELO", "VILMAR JR"), index=0, key='sup_5', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
                                if supName == "MARCELO":
                                    with col5:
                                        supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (2,), index=0, key='MARCELO_5', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                        supOnOff = "IN"     # -- Está em 2
                                elif supName == "VILMAR JR":
                                    with col5:
                                        supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (8,), index=0, key='vilmar_5', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                        supOnOff = "IN"     # -- Está em 8
                                elif supName == "TODOS":
                                    with col5:
                                        supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (0,), index=0, key='todos_5', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                                        supOnOff = "NOT IN" # -- Não está em 0
                                else:
                                    with col5:
                                        supCod = st.selectbox("ERRO", (999,), index=0, key='3', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
                        else:
                            with col4:
                                supCod = 0
                                supOnOff = "NOT IN"

                        with col3: 
                            inputFornec = st.text_input(label="Digite o Código Fornecedor",value="1841",key="selected_codFornec",max_chars=4,)
                            selected_codFornec = bleach.clean(inputFornec)
                st.divider()
                c1,c2,c3 = st.columns([0.6,1.5,0.8])

                with c1:
                    st.write("Legenda:")
                    container1 = st.container(border=True)
                    container1.caption(f'vendedorCod = {vendedorCod} supCod= {supCod} supOnOff = {supOnOff} rcaOnOff = {rcaOnOff} selected_codFornec = {selected_codFornec}')

                with c3:
                    cliente_semVenda_result = cliente_semVenda(vendedorCod, supCod, supOnOff, rcaOnOff, selected_codFornec) # (sup, rca, supOnOff, rcaOnOff, fornec)
                    cliente_semVenda_result = cliente_semVenda_result.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]].rename(columns={
                        0: "CLIENTE",
                        1: "COD",
                        2: "RCA",
                        3: "SUP",
                        4: "FANTASIA",
                        5: "ULT. COMPRA",
                        6: "BLOQUEIO",
                        7: "INAD.",
                        8: "FREEZER",
                        9: "CADASTRO",
                        10: "1ª COMPRA"
                    })
                    st.divider()
                    if st.button('GERAR EXCEL', key="excel_semVenda"): # ---- Convertendo para Excel
                        st.markdown(getTableXls(cliente_semVenda_result), unsafe_allow_html=True) # ---- Disponibilizando o arquivo para Download
                        st.toast('Gerando arquivo excel... Clique em :blue[Baixar]')
                        tm.sleep(.5)
                    

                with c2:
                    st.write("Tabela de Clientes :red[Sem Venda:]")
                    if cliente_semVenda_result.empty:
                        st.warning("Sem dados para exibir. Verifique os filtros selecionados acima :point_up:")
                    else:
                        st.dataframe(cliente_semVenda_result, hide_index=True)




        # ----------------- Botão de Recarregar dados Dedo Duro -----------------
        with colum2:
            recarregarDados = st.button("RECARREGAR", key=5, type="primary")
        if recarregarDados:
            st.toast("Informações sendo recarregadas no banco de dados. Favor aguardar...")
            pedErro_result = pedErro()
            pedCont_result = pedCont()
            pedVsEst_result = pedidoVsEstoque()
            inad_result = inad(vendedorCod)
            devolucao_result = devolucao(dataIni, dataFim)
            cliente_semVenda_result = cliente_semVenda(vendedorCod, supCod, supOnOff, rcaOnOff, selected_codFornec)
            cortesFornec_result = cortesFornec(data_inicial, data_final, supOnOff, supCod)
            cortesEquipe_result = cortesEquipe(codFornec, data_inicial, data_final)
            estoque266_result = estoque266()



# --------------------------- META --------------------------------------- # ------------------- # ------------------- # ------------------- # ------------------- # 
elif st.session_state['active_tab'] == ':dart: META':
    with tabs[3]:
        st.divider()
        st.markdown("<br>", unsafe_allow_html=True)
        aba3_1, aba3_2 = st.tabs(["VENDEDOR", "SUPERVISOR"])
        # ------------------------------- VENDEDOR --------------------------------------- #
        with aba3_1:
            col1, col2, col3, col4 = st.columns([0.55, 1, 1, 2])
            with col1:
                    dias_decor_result = str(diasDecorridos()).split()[-1]
                    dias_uteis_result = str(diasUteis()).split()[-1]
                    st.markdown(dias_uteis_result + " DIAS ÚTEIS", unsafe_allow_html=False, help="Quantidade de dias úteis para serem realizadas suas vendas.")
                    st.markdown(dias_decor_result + " DECORRIDOS", unsafe_allow_html=False, help="Quantidade de dias úteis decorridos no mês.")
            with col2:
                    vendedorName = st.selectbox(":man: VENDEDOR", ("LEONARDO", "EDNALDO", "VAGNER", "DEIVID", "BISMARCK", "LUCIANA", "MATHEUS", "MARCIO", "LEANDRO", "REGINALDO", "ROBSON", "JOAO", "TAYANE", "MURILO", "LUCAS", "DEYVISON", "ZEFERINO", "EPAMINONDAS", "GLAUBER", "TARCISIO", "THIAGO", "FILIPE", "ROMILSON", "VALDEME"), index=0, key='rca_2', help="Selecione o vendedor", placeholder=":man: Escolha um Vendedor", label_visibility="visible")
                    if vendedorName == "LEONARDO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (140,),index=0, key='140_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "EDNALDO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (141,),index=0, key='141_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "VAGNER":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (142,),index=0, key='142_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "DEIVID":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (143,),index=0, key='143_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "BISMARCK":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (145,),index=0, key='145_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LUCIANA":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (147,),index=0, key='147_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MATHEUS":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (148,),index=0, key='148_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MARCIO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (150,),index=0, key='150_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LEANDRO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (151,),index=0, key='151_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "REGINALDO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (152,),index=0, key='152_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ROBSON":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (153,),index=0, key='153_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "JOAO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (154,),index=0, key='154_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "TAYANE":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (155,),index=0, key='155_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "MURILO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (156,),index=0, key='156_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "LUCAS":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (157,),index=0, key='157_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "DEYVISON":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (158,),index=0, key='158_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ZEFERINO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (161,),index=0, key='161_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "EPAMINONDAS":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (164,),index=0, key='164_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "GLAUBER":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (167,),index=0, key='167_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "TARCISIO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (168,),index=0, key='168_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "THIAGO":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (169,),index=0, key='169_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "FILIPE":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (170,),index=0, key='170_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "ROMILSON":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (172,),index=0, key='172_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    elif vendedorName == "VALDEME":
                        with col3:
                            vendedorCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (174,),index=0, key='174_2', help="Código RCA preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                    else:
                        vendedorCod = st.selectbox("ERRO", (999,),index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible") 
            with col4:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("Como é calculada a meta?", expanded=False):
                    st.markdown("A meta é calculada com base no histórico de vendas do vendedor dos ultimos 2 meses e considerando a quantidade de dias úteis desses meses.")
            if st.button("CARREGAR", key=2):
                with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                    # --------------------------- DADOS META --------------------------- #
                    meta_result = metaCalc(vendedorCod)
                    if meta_result.empty:
                        st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                    else:
                        with st.container(border=False):
                            # ----------------- Formatação da tabela -----------------
                            meta_result = meta_result.iloc[:, [0, 1, 2, 3, 4, 5, 6]].rename(columns={
                                0: "CODSEC",
                                1: "SECAO",
                                2: "CODSUPERVISOR",
                                3: "RCA",
                                4: "TOTAL VENDIDO",
                                5: "META MÊS",
                                6: "META DIA"
                            })

                            # -------- Formatação para Metric
                            meta_mes_total = format_number(meta_result["META MÊS"].sum())
                            meta_dia_total = format_number(meta_result["META DIA"].sum())

                            formatarMoeda = ["TOTAL VENDIDO", "META MÊS", "META DIA"]
                            for coluna in formatarMoeda:
                                meta_result[coluna] = meta_result[coluna].apply(format_number)

                            meta_result = meta_result.drop(columns=["CODSUPERVISOR","RCA"]) # Removendo colunas desnecessárias

                            # ------ DataFrame para HTML 
                            table_html = meta_result.to_html(classes='table-style', index=False)
                            table_html = table_html.replace('<td>', '<td class="linha-table">')

                            # ------ Estilos CSS personalizados
                            with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                                cli_css = file.read()
                            css = f"""
                            <style>
                                {cli_css}
                            </style>
                            """       
                            # ----------------- Exibição da tabela -----------------
                            mes_atual = datetime.now().month # Obtém o mês atual
                            mes = meses[mes_atual] # Obtém o nome do mês atual
                            st.markdown(f"<h3 class='dnH3'>META {mes} VENDEDOR {vendedorName}</h3>", unsafe_allow_html=True) # Título da seção

                            st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit

                            st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS
                            
                            # Cria a tabela HTML
                            html_table = f"""
                            <table class='table-style'>
                                <tr>
                                    <th>META TOTAL</th>
                                    <th>META DIA TOTAL</th>
                                </tr>
                                <tr>
                                    <td class="linha-table">{meta_mes_total}</td>
                                    <td class="linha-table">{meta_dia_total}</td>
                                </tr>
                            </table>
                            """
                            # Exibe a tabela HTML
                            st.markdown(html_table, unsafe_allow_html=True)

        with aba3_2:
            col1, col2, col3, col4 = st.columns([0.55, 1, 1, 2])
            with col1:
                dias_decor_result = str(diasDecorridos()).split()[-1]
                dias_uteis_result = str(diasUteis()).split()[-1]
                st.markdown(dias_uteis_result + " DIAS ÚTEIS", unsafe_allow_html=False, help="Quantidade de dias úteis para serem realizadas suas vendas.")
                st.markdown(dias_decor_result + " DECORRIDOS", unsafe_allow_html=False, help="Quantidade de dias úteis decorridos no mês.")
            with col2:
                supName = st.selectbox(":male-office-worker: SUPERVISOR", ("MARCELO", "VILMAR JR"), index=0, key='sup_2', help="Selecione o Supervisor", placeholder=":male-office-worker: Escolha o Supervisor", label_visibility="visible")
                if supName == "MARCELO":
                    with col3:
                        supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (2,), index=0, key='MARCELO_2', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                elif supName == "VILMAR JR":
                    with col3:
                        supCod = st.selectbox(":desktop_computer: CÓDIGO WINTHOR", (8,), index=0, key='vilmar_2', help="Código Supervisor preenchido com base no nome selecionado", placeholder="", disabled=True, label_visibility="visible")
                else:
                    with col3:
                        supCod = st.selectbox("ERRO", (999,), index=0, key='0', help="ERRO: CONTATO O SUPORTE DE TI", placeholder="", disabled=True, label_visibility="visible")
            with col4:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("Como é calculada a meta?", expanded=False):
                    st.markdown("A meta é calculada com base no histórico de vendas do vendedor dos ultimos 2 meses e considerando a quantidade de dias úteis desses meses.")
            if st.button("CARREGAR", key=3):
                with st.spinner('Carregando dados...'):  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.  # Pode gerar erro de recarregar todos os elemntos novamente. Usar em tabelas ou gráificos apenas.
                    # --------------------------- DADOS META --------------------------- #
                    meta_result = metaSupCalc(supCod)
                    if meta_result.empty:
                        st.markdown("Sem dados para exibir", help="Não há dados para exibir, verifique os filtros escolhidos ou contate o suporte.")
                    else:
                        with st.container(border=False):
                            # ----------------- Formatação da tabela -----------------
                            meta_result = meta_result.iloc[:, [0, 1, 2, 3, 4, 5]].rename(columns={
                                0: "CODSEC",
                                1: "SECAO",
                                2: "CODSUPERVISOR",
                                3: "TOTAL VENDIDO",
                                4: "META MÊS",
                                5: "META DIA"
                            })

                            # -------- Formatação para Metric
                            meta_mes_total = format_number(meta_result["META MÊS"].sum())
                            meta_dia_total = format_number(meta_result["META DIA"].sum())

                            formatarMoeda = ["TOTAL VENDIDO", "META MÊS", "META DIA"]
                            for coluna in formatarMoeda:
                                meta_result[coluna] = meta_result[coluna].apply(format_number)

                            meta_result = meta_result.drop(columns=["CODSUPERVISOR"]) # Removendo colunas desnecessárias

                            # ------ DataFrame para HTML 
                            table_html = meta_result.to_html(classes='table-style', index=False)
                            table_html = table_html.replace('<td>', '<td class="linha-table">')

                            # ------ Estilos CSS personalizados
                            with open('/home/ti_premium/PyDashboards/PremiumDashboards/css/clientes.css', "r") as file:
                                cli_css = file.read()
                            css = f"""
                            <style>
                                {cli_css}
                            </style>
                            """       
                            # ----------------- Exibição da tabela -----------------
                            mes_atual = datetime.now().month # Obtém o mês atual
                            mes = meses[mes_atual] # Obtém o nome do mês atual
                            st.markdown(f"<h3 class='dnH3'>META {mes} SUPERVISOR {supName}</h3>", unsafe_allow_html=True) # Título da seção

                            st.markdown(table_html, unsafe_allow_html=True) # Exibindo a tabela no Streamlit

                            st.markdown(css, unsafe_allow_html=True) # Aplicando os estilos CSS
                            
                            # Cria a tabela HTML
                            html_table = f"""
                            <table class='table-style'>
                                <tr>
                                    <th>META TOTAL</th>
                                    <th>META DIA TOTAL</th>
                                </tr>
                                <tr>
                                    <td class="linha-table">{meta_mes_total}</td>
                                    <td class="linha-table">{meta_dia_total}</td>
                                </tr>
                            </table>
                            """
                            # Exibe a tabela HTML
                            st.markdown(html_table, unsafe_allow_html=True)

# --------------------------- Outros ----------------------------------- # ------------------- # ------------------- # ------------------- # ------------------- # 
elif st.session_state['active_tab'] == ':notebook:':
    with tabs[7]:
        with st.spinner('Carregando dados...'): 
            st.divider()


st.markdown("<br> <br> <br> <br>", unsafe_allow_html=True)
st.divider()
col1, col2, col3 = st.columns([2.5,1,2.5])
with col2:
    st.image('https://cdn-icons-png.flaticon.com/512/8556/8556430.png', width=200, caption="Plataforma BI - Versão 2.18")
    c1, c2 = st.columns([0.4, 1.6])
    with c2:
        with st.spinner('Carregando...'):
            tm.sleep(3)

#4000 