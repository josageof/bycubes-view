# -*- coding: utf-8 -*-
"""
Created on Sun Oct 01 19:08:32 2023

@author: Josa -- josageof@gmail.com
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st
import pydeck as pdk
import plotly.express as px

from utils.components import page_config, sidebar_vspace, sidebar_click_rside
from utils.filters import st_selectbox_filter, st_multiselect_filter, st_slider_vfilter


# %%===========================================================================
# !!! DATA

## Carrega as localizações das usinas nucleares ao redor do mundo
oil_field_file = "data/campos_de_producao_jan2023/CAMPOS_DE_PRODUCAO_08082023.shp"
gdf_oil_field = gpd.read_file(oil_field_file)
# df_oil_field = gdf_oil_field.drop('geometry', axis=1)

## Produção em terra, mar e presal
on_prod_072023_df = pd.read_csv('data/producao_oeg-07-2023/2023_07_producao_Terra.csv', sep=';')
off_prod_072023_df = pd.read_csv('data/producao_oeg-07-2023/2023_07_producao_Mar.csv', sep=';')
pre_prod_072023_df = pd.read_csv('data/producao_oeg-07-2023/2023_07_producao_Presal.csv', sep=';')
df_prod_072023 = pd.concat([on_prod_072023_df, 
                            off_prod_072023_df, 
                            pre_prod_072023_df], ignore_index=True)

## Separa apenas os dados da produção de Petróle, Gás e Água por campo
df_prod_072023 = df_prod_072023[['Campo', 
                                 'Petróleo (bbl/dia)',
                                 'Gás Natural (Mm³/dia) Total',
                                 'Água (bbl/dia)']].groupby('Campo').sum().reset_index()


## Removendo espeços desnecessários
gdf_oil_field['NOM_CAMPO'] = gdf_oil_field['NOM_CAMPO'].str.strip()
df_prod_072023['Campo'] = df_prod_072023['Campo'].str.strip()


## Mesclando
gdf_oil_field = gdf_oil_field.merge(df_prod_072023, 
                                  left_on='NOM_CAMPO', 
                                  right_on='Campo', 
                                  how='inner')



# %%===========================================================================
# !!! HEADER

APP_TITLE = "Produção Atual de Óleo e Gás por Campo"
APP_SUBTITLE = """
    O volume de petróleo e gás natural produzido em cada campo deve ser determinado periódica e regularmente pelos 
    concessionários ou contratados, que entregam à ANP, até o 15º dia de cada mês, um Boletim Mensal de Produção (BMP).
    Para garantir que os sistemas de medição das unidades de produção de petróleo e gás natural apresentem resultados acurados e completos,
    a ANP fiscaliza _in loco_ (`www.gov.br/anp`).
    """

page_config("wide")

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

# st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)



# %%===========================================================================
# !!! SIDEBAR

# st.write(len(gdf_oil_field))
# st.write(gdf_oil_field.drop('geometry', axis=1))


sidebar_vspace(10)

sidebar_click_rside()

sidebar_vspace(10)

## Filtro por bacia sedimentar
gdf_oil_field = st_selectbox_filter(gdf_oil_field, 
                                    "NOM_BACIA", 
                                    "Selecione uma bacia sedimentar:")

sidebar_vspace(10)

## Filtro por Operador
gdf_oil_field = st_selectbox_filter(gdf_oil_field, 
                                    "OPERADOR_C", 
                                    "Selecione a responsável pelos poços:")

sidebar_vspace(10)

# Filtro por Campo
gdf_oil_field = st_multiselect_filter(gdf_oil_field, 
                                   'NOM_CAMPO', 
                                   'Selecione os campos desejados:')



# %%===========================================================================
#!!! MAIN PAGE

fig = px.choropleth_mapbox(gdf_oil_field, geojson=gdf_oil_field.geometry, locations=gdf_oil_field.index, 
                           color="Petróleo (bbl/dia)",
                           color_continuous_scale="reds",
                           center = {"lat": -15, "lon": -55},
                           height=635,
                           opacity=0.5,
                           zoom=3,
                           hover_name="NOM_CAMPO",
                           hover_data=["OPERADOR_C", "Petróleo (bbl/dia)"],
                           )

fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "Brazil Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
    ])

fig.update_layout(title_text='')

fig.update_geos(fitbounds="locations", visible=True)

fig.update(layout = dict(title=dict(x=0.4)))

st.plotly_chart(fig, theme="streamlit", use_container_width=True)



# %%===========================================================================
#!!! FOOTER

st.subheader("🦉 Confira a linha do tempo da produção de petróleo e gás natural no Brasil:")

st.markdown(
"""
    <span style="color: #FFC83D"><strong>1919:</strong></span>  Foi realizada a primeira perfuração pelo Serviço Geológico e Mineralógico do 
    Brasil (SGMB), no município de Mallet (PR). O poço chegou aos 84 metros, mas foi abandonado no ano seguinte;<br>
    <span style="color: #FFC83D"><strong>1939:</strong></span>  Primeira descoberta de petróleo no Brasil, realizada pela Divisão de Fomento 
    da Produção Mineral, órgão do Departamento Nacional da Produção Mineral (DNPM), no poço nº 163, localizado em Lobato, no Recôncavo Baiano.
    A descoberta foi considerada sub-comercial;<br>
    <span style="color: #FFC83D"><strong>1941:</strong></span>  Descoberto em Candeias (BA) o primeiro campo comercial de petróleo do país. 
    Nesta época foram descobertos campos de gás natural em Aratu e de petróleo em Itaparica, ambos no Recôncavo Baiano;<br>
    <span style="color: #FFC83D"><strong>1947:</strong></span>  Início da campanha “O petróleo é nosso”. Entre 1947 a 1953, o País esteve dividido
    entre aqueles que achavam que o petróleo deveria ser explorado exclusivamente por uma empresa estatal e os defendiam a livre concorrência;<br>
    <span style="color: #FFC83D"><strong>1953:</strong></span>  Em 3 de outubro, Getúlio Vargas assina a Lei 2004, que cria a Petrobras;<br>
    <span style="color: #FFC83D"><strong>1954:</strong></span>  Em 10 de maio seguinte a Petrobras entrou em operação, avançou com novas descobertas,
    perfurações, produção e expansão do monopólio para petroquímica, importação/exportação;<br>
    <span style="color: #FFC83D"><strong>1968:</strong></span>  Foi perfurado o primeiro poço submarino na Bacia de Campos - RJ e, em seguida, 
    realizada a primeira descoberta de petróleo no mar, no campo de Guaricema - SE;<br>
    <span style="color: #FFC83D"><strong>1975:</strong></span>  A exploração de petróleo no território nacional foi aberta à iniciativa privada,
    por meio dos contratos de risco;<br>
    <span style="color: #FFC83D"><strong>1984:</strong></span>  Descoberto o Albacora, primeiro campo gigante do país (bacia de Campos - RJ);<br>
    <span style="color: #FFC83D"><strong>1985:</strong></span>  Descoberta do campo de Marlim, o segundo campo gigante do país, também na bacia de Campos;<br>
    <span style="color: #FFC83D"><strong>1997:</strong></span>  Foi aprovada a Lei do Petróleo, Lei nº 9.478, criando a ANP, o CNPE e introduzindo 
    as regras para a execução das atividades integrantes do monopólio da União sobre o petróleo;<br>
    <span style="color: #FFC83D"><strong>2000:</strong></span>  A Shell é a primeira empresa privada a começar a exploração de petróleo na Bacia de Campos;<br>
    <span style="color: #FFC83D"><strong>2005:</strong></span>  Encontrados os primeiros indícios de petróleo no pré-sal na Bacia de Santos, 
    no bloco BM-S-10 (Parati), no litoral do estado do Rio de Janeiro;<br>
    <span style="color: #FFC83D"><strong>2007:</strong></span>  Encontrada jazida de óleo leve na seção pré-sal que deu origem ao campo de Caxaréu, 
    no norte da Bacia de Campos;<br>
    ... desse ano em diante ocorreram, principalmente, mais avanços relacionados ao desenvolvimento de novas tecnologias, mais perfurações e 
    aumento da produção.
""", unsafe_allow_html=True
)

st.info(
"""
    "
    Brasil teve recorde na produção de petróleo e gás natural em julho/23. O Total chegou a 4,482 milhões de barris de óleo equivalente por dia.
    O Campo de Tupi, no pré-sal da Bacia de Santos, foi o maior produtor, registrando 865,71 mil bbl/d de petróleo e 41,63 milhões
    de m³/d de gás natural (`Fonte: agenciabrasil.ebc.com.br`).
    "
"""
)