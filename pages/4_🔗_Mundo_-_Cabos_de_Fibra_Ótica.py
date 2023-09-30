# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 19:08:32 2023

@author: Josa -- josageof@gmail.com
"""

import pandas as pd
import geopandas as gpd
import streamlit as st
import pydeck as pdk
import random

from utils.components import sidebar_vspace, sidebar_click_rside
from utils.filters import st_selectbox_filter2, st_slider_vfilter


# %%===========================================================================
# !!! DATA

## Carrega as rotas dos cabos de fibra ótica instalados nos oceanos
world_cables_file = "data/fiber_optic_connections_worldwide_2020/fiber_optic_connections_worldwide_2020.shp"

## Ler os arquivos como geopandas
gdf_cables = gpd.read_file(world_cables_file)

gdf_cables['ReadyForSe'] = gdf_cables['ReadyForSe'].str.extract(r'(\b\d{4}\b)').astype(int)

gdf_cables['LENGTH'] = gdf_cables['LENGTH'].astype(float)



# %%===========================================================================
# !!! PAGE TITLE

APP_TITLE = "Mapa Mundial de Cabos Submarinos de Fibra Óptica"
APP_SUBTITLE = """
    Uma visão global das rotas de comunicação transoceânicas, mostrando
    a estrutura de cabos atualizada até 2020 (`www.itu.int`).
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


# !!! Filtro por anos
gdf_cables = st_slider_vfilter(gdf_cables, 
                               "ReadyForSe", 
                               "Selecione o início de operação (ano):")


sidebar_vspace(10)


## Filtro por dono no cabo
gdf_cables = st_selectbox_filter2(gdf_cables, 
                                  "owners", 
                                  "Selecione um dos donos de cabos:")


sidebar_vspace(10)

## !!! Filtro por LENGTH
gdf_cables = st_slider_vfilter(gdf_cables, 
                               "LENGTH", 
                               "Selecione o comprimento (km):")




# %%===========================================================================
#!!! MAIN PAGE

# Obtem uma lista de valores únicos na coluna 'Name'
unique_names = gdf_cables['NAME'].unique()

# Crie um mapeamento de cores com base nos valores únicos no formato RGB
color_mapping = {name: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
                  for i, name in enumerate(unique_names)}

# Adiciona uma coluna 'color' ao GeoDataFrame com base no mapeamento de cores
gdf_cables['color'] = gdf_cables['NAME'].map(color_mapping)


# Cria uma camada de cabos com cores diferentes com base nos valores de 'Name'
cables = pdk.Layer(
    "GeoJsonLayer",
    gdf_cables,
    pickable=True,
    opacity=1,
    filled=False,
    extruded=False,
    wireframe=False,
    line_width_min_pixels=2,
    get_line_color="color",
)


initial_view = pdk.ViewState(
    latitude=0, 
    longitude=-6, 
    zoom=1.8, 
    # min_zoom=2,
    max_zoom=16, 
    pitch=0, 
    bearing=0,
    wrapLongitude=True  # Permite que o mapa se repita horizontalmente
)

m = pdk.Deck(
    initial_view_state=initial_view,
    # map_style=None,
    map_style="mapbox://styles/mapbox/satellite-v9", 
    layers=[cables], 
    tooltip={"text": """{NAME}
              Length: {length}
              Ready: {ReadyForSe}
              {owners}"""}
)

st.pydeck_chart(m, use_container_width=True)



# %%===========================================================================
#!!! FOOTER

st.subheader("São mais de 550 cabos instalados ao redor do planeta")

st.markdown(
"""
    Cabos submarinos de fibra óptica são sistemas de comunicação que desempenham um papel 
    fundamental na infraestrutura global de comunicações.
"""
)

st.info(
"""
    "
    Esses cabos permitem a transmissão de dados em larga escala através de longas distâncias debaixo
    do oceano, desempenhando um papel vital em nosso mundo altamente conectado.
    Praticamente todas as comunicações hoje são feitas através de cabos submarinos, mais de 90% delas. 
    São opções com muitas vantagens em relação a outras como os satélites, por exemplo. 
    Muitas vezes, eles são muito mais acessíveis que os próprios satélites."
"""
)
