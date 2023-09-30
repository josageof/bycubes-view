# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 19:08:32 2023

@author: Josa -- josageof@gmail.com
"""

import pandas as pd
import geopandas as gpd
import streamlit as st
import pydeck as pdk

from utils.components import sidebar_vspace, sidebar_click_rside, map_rgb_from_col
from utils.filters import st_selectbox_filter, st_checkbox_filter


# %%===========================================================================
# !!! DATA

## Carregar os dados de bacias sedimentares brasileiras a partir de um arquivo GeoJSON
br_bacias_geojson_file = "data/bacias_sedimentares_brasileiras.geojson"

## Ler o arquivo geojson como geopandas
gdf_bacias = gpd.read_file(br_bacias_geojson_file)

## Importa os dados dos poços no formato pickle
df_pocos = pd.read_pickle("data/pocos_ANP_atualizado_09-08-2023.pkl")

## Ajusta os dados de interesse
df_pocos['OPERADOR'] = df_pocos['OPERADOR'].replace('', 'Desconhecido')
df_pocos['SITUACAO'] = df_pocos['SITUACAO'].replace('', 'OUTRO')
df_pocos['TERRA_MAR'] = df_pocos['TERRA_MAR'].replace('T', 'Terra')
df_pocos['TERRA_MAR'] = df_pocos['TERRA_MAR'].replace('M', 'Mar')
df_pocos['PROF_SOND'] = pd.to_numeric(df_pocos['PROF_SOND'], errors='coerce').fillna(0).astype(int)
df_pocos['latitude'] = df_pocos["LAT_DD"].astype(float)
df_pocos['longitude'] = df_pocos["LONG_DD"].astype(float)



# %%===========================================================================
# !!! PAGE TITLE

APP_TITLE = "Poços de O&G cadastrados na ANP até 09/08/2023"
APP_SUBTITLE = """
    Agência Nacional do Petróleo, Gás Natural e Biocombustíveis (ANP), foi criada em 1997 pela lei n º 9.478. 
    É o órgão regulador das atividades que integram as indústrias de petróleo e gás natural e de biocombustíveis 
    no Brasil (`www.gov.br/anp`).
    """

st.set_page_config(
    layout="wide",
    page_title="byCubes View",
    page_icon="👋",
)

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)



# %%===========================================================================
# !!! SIDEBAR

sidebar_vspace(10)

sidebar_click_rside()

sidebar_vspace(10)

## Filtro por bacia sedimentar
filt_df_pocos = st_selectbox_filter(df_pocos, 
                                    "BACIA", 
                                    "Selecione uma bacia sedimentar:")

sidebar_vspace(10)

## Filtro por Ambiente (Onshore/Offshore)
filt_df_pocos = st_checkbox_filter(filt_df_pocos, 
                                    "TERRA_MAR")

sidebar_vspace(10)

## Filtro por Situação
filt_df_pocos = st_selectbox_filter(filt_df_pocos, 
                                    "SITUACAO", 
                                    "Selecione a situação atual dos poços:")

sidebar_vspace(10)

## Filtro por Categoria
filt_df_pocos = st_selectbox_filter(filt_df_pocos, 
                                    "CATEGORIA", 
                                    "Selecione a categoria dos poços:")

sidebar_vspace(10)

## Filtro por Direção (Vertical/Direcional)
filt_df_pocos = st_selectbox_filter(filt_df_pocos, 
                                    "DIRECAO",
                                    "Selecione a direção dos poços:")

sidebar_vspace(10)

## Filtro por Operador
filt_df_pocos = st_selectbox_filter(filt_df_pocos, 
                                    "OPERADOR", 
                                    "Selecione a responsável pelos poços:")




# %%===========================================================================
#!!! MAIN PAGE

# st.map(filt_df_pocos)

initial_view_state = pdk.ViewState(
    latitude=-20, 
    longitude=-50, 
    zoom=4, 
    max_zoom=16, 
    pitch=60, 
    bearing=0)


bacias = pdk.Layer(
    "GeoJsonLayer",
    gdf_bacias,
    opacity=0.5,
    # stroked=False,
    filled=False,
    extruded=False,
    wireframe=False,
    line_width_min_pixels=1,
    # get_fill_color="[210, 180, 140]",
    get_line_color="[210, 180, 140]",
)


## Aplica a função para mapear os valores da coluna 'PROF_SOND' como cores, criando 'RGB'
filt_df_pocos = map_rgb_from_col(filt_df_pocos, "PROF_SOND")


pocos = pdk.Layer(
    "ColumnLayer",
    data=filt_df_pocos,
    get_position='[longitude, latitude]',
    get_elevation="PROF_SOND",
    elevation_scale=20,
    radius=3000,
    get_fill_color="RGB",
    pickable=True,
    auto_highlight=True,
)

m = pdk.Deck(
             map_style="mapbox://styles/mapbox/satellite-v9", 
             layers=[bacias, pocos], 
             initial_view_state=initial_view_state,
             tooltip={"text": """{POCO}
                      Prof: {PROF_SOND} m
                      {OPERADOR}"""}
             )

st.pydeck_chart(m, use_container_width=True)



# %%===========================================================================
#!!! FOOTER

st.subheader("Distribuição dos poços por Bacia Sedimentar")

st.markdown(
"""
    Em meio ao cenário de valorização do gás natural, agravado pela Guerra da Ucrânia, o Brasil tem deixado
    de aproveitar sua disponibilidade do recurso por falta de infraestrutura de exploração. 
    Por _Stéfano Salles_ - CNN.
"""
)

st.info(
"""
    "Em oitenta anos, o Brasil já perfurou um total de 30.516 poços para explorar petróleo e gás natural, 
    sendo 23.503 em terra e 7.013 no mar. Para efeito de comparação, a Argentina já perfurou 60 mil poços 
    e os EUA, 4 milhões. Do nosso total de pouco mais de 30 mil poços de petróleo e gás, atualmente temos 
    5.607 poços em produção, alguns perfurados ainda na década de 1950. Também temos 1.739 poços injetando 
    água, gás carbônico e outras substâncias para aumentar a eficiência dos poços de produção"
"""
)
