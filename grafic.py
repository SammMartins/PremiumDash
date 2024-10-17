from turtle import color
import plotly.express as px
import pandas as pd
from dataset import df1, df2
from utils import data_semana_ini, data_semana_fim, format_number

def gerar_graficoVendas(start_of_week, end_of_week):
    df = df2(start_of_week, end_of_week)

    if df.empty:
        print("DataFrame está vazio. Não é possível criar o gráfico.")
    else:
        alvo = df[3].mean() # Média de vendas
        # ------------------------- GRÁFICO VENDA POR RCA -------------------------
        grafico_vend_sup = px.bar(
            df,
            x = df.columns[2],
            y = df.columns[3], 
            title = "RANKING DE VENDAS POR RCA",
            range_y = (0, df[3].max()),
            color = df.columns[3],
            color_continuous_scale = [(0, "#e63d42"), (0.5, "#f6d272"), (1, "#008000")]
        )

        grafico_vend_sup.update_traces(
            text = df[df.columns[3]].apply(lambda x: format_number(x)),
            textposition = 'inside',
            textfont = dict(color='black', family='Verdana', size=12),
            name = 'Linha tracejada é a média de vendas dos RCA'
        )

        grafico_vend_sup.add_shape(
            type='line',
            line=dict(dash='dash', color='white'),
            y0=alvo,
            y1=alvo,
            x0=0,
            x1=1,
            xref='paper',
            yref='y'
        )


        # ------------------------- GRÁFICO VENDA POR RCA TIME SUL -------------------------    
        df_2 = df[df[df.columns[0]] == 2]
        grafico_top_rca2 = px.bar(
            df_2,
            x = df.columns[2],
            y = df.columns[3], 
            title = "RANKING DE VENDAS POR RCA - SUL",
            range_y = (0, df[3].max()),
            color = df.columns[3],
            color_continuous_scale = [(0, "#e63d42"), (0.5, "#f6d272"), (1, "#008000")]
        )

        grafico_top_rca2.update_traces(
            text = df_2[df_2.columns[3]].apply(lambda x: format_number(x)),
            textposition = 'inside',
            textfont = dict(color='black', family='Verdana', size=12)
        )

        grafico_top_rca2.add_shape(
            type='line',
            line=dict(dash='dash', color='white'),
            y0=alvo,
            y1=alvo,
            x0=0,
            x1=1,
            xref='paper',
            yref='y'
        )

        # ------------------------- GRÁFICO VENDA POR RCA TIME VCA -------------------------
        df_8 = df[df[df.columns[0]] == 8]
        grafico_top_rca8 = px.bar(
            df_8,
            x = df.columns[2],
            y = df.columns[3], 
            title = "RANKING DE VENDAS POR RCA - VCA",
            range_y = (0, df[3].max()),
            color = df.columns[3],
            color_continuous_scale = [(0, "#e63d42"), (0.5, "#f6d272"), (1, "#008000")]
        )

        grafico_top_rca8.update_traces(
            text = df_8[df_8.columns[3]].apply(lambda x: format_number(x)),
            textposition = 'inside',
            textfont = dict(color='black', family='Verdana', size=12)
        )

        grafico_top_rca8.add_shape(
            type='line',
            line=dict(dash='dash', color='white'),
            y0=alvo,
            y1=alvo,
            x0=0,
            x1=1,
            xref='paper',
            yref='y'
        )

        # ------------------------- GRÁFICO VENDA POR RCA TIME SERTÃO -------------------------
        df_9 = df[df[df.columns[0]] == 9]
        grafico_top_rca9 = px.bar(
            df_9,
            x = df.columns[2],
            y = df.columns[3], 
            title = "RANKING DE VENDAS POR RCA - SERTÃO",
            range_y = (0, df[3].max()),
            color = df.columns[3],
            color_continuous_scale = [(0, "#e63d42"), (0.5, "#f6d272"), (1, "#008000")]
        )

        grafico_top_rca9.update_traces(
            text = df_9[df_9.columns[3]].apply(lambda x: format_number(x)),
            textposition = 'inside',
            textfont = dict(color='black', family='Verdana', size=12)
        )

        grafico_top_rca9.add_shape(
            type='line',
            line=dict(dash='dash', color='white'),
            y0=alvo,
            y1=alvo,
            x0=0,
            x1=1,
            xref='paper',
            yref='y'
        )

        return grafico_vend_sup, grafico_top_rca2, grafico_top_rca8, grafico_top_rca9
    
