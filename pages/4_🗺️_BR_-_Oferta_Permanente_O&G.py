# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 14:51:10 2023

@author: Josa -- josageof@gmail.com
"""

import pandas as pd
import geopandas as gpd
import streamlit as st
import pydeck as pdk

from utils.components import page_config, local_css, sidebar_vspace, sidebar_click_rside
from utils.filters import st_selectbox_filter, st_slider_vfilter, st_checkbox_filter


# %%===========================================================================
# !!! DATA

## Carregar os dados de bacias sedimentares brasileiras a partir de um arquivo GeoJSON
br_bacias_geojson_file = "data/bacias_sedimentares_brasileiras.geojson"

## Ler o arquivo geojson como geopandas
gdf_bacias = gpd.read_file(br_bacias_geojson_file)


## Carregar os blocos da Oferta Permanente a partir de arquivos Shapefile
blocos_exp_file = "data/blocos-exploratorios-concessao/BLOCOS_EXPLORATORIOS_08082023.shp"

## Ler os arquivos como geopandas
gdf_blocos_exp = gpd.read_file(blocos_exp_file)

# tmp_df_blocos_exp = gdf_blocos_exp.drop(columns=['geometry'])

## Carrega os resultados dos ciclos de Oferta Permanente
resultado_op1_file = "data/resultado_oferta_permanente/resultado_operadora_bloco_UT_op1.csv"
resultado_op2_file = "data/resultado_oferta_permanente/resultado_operadora_bloco_UT_op2.csv"
resultado_op3_file = "data/resultado_oferta_permanente/resultado_operadora_bloco_UT_op3.csv"

## Ler os arquivos como dataframe
df_resultado_op1 = pd.read_csv(resultado_op1_file, sep=';')
df_resultado_op2 = pd.read_csv(resultado_op2_file, sep=';')
df_resultado_op3 = pd.read_csv(resultado_op3_file, sep=';')

## Adiciona a coluna Ciclo
df_resultado_op1['Ciclo'] = 1
df_resultado_op2['Ciclo'] = 2
df_resultado_op3['Ciclo'] = 3

# Junta os DataFrames verticalmente (ao longo das linhas)
df_resultado_op = pd.concat([df_resultado_op1, df_resultado_op2, df_resultado_op3], axis=0)


## Adiciona os df dos resultados ao gdf dos blocos em oferta
gdf_resultado_op = gdf_blocos_exp.merge(df_resultado_op, 
                                            left_on='NOM_BLOCO', 
                                            right_on='Bloco', 
                                            how='left')


## Separa os dados consolidados das Ofertas Permanentes
gdf_op1 = gdf_resultado_op[gdf_resultado_op['Ciclo'] == 1]
gdf_op2 = gdf_resultado_op[gdf_resultado_op['Ciclo'] == 2]
gdf_op3 = gdf_resultado_op[gdf_resultado_op['Ciclo'] == 3]

# Junta apenas os dados da Oferta Permanente
gdf_op = pd.concat([gdf_op1, gdf_op2, gdf_op3], axis=0)

# tmp_df_op = gdf_op.drop(columns=['geometry'])



# %%===========================================================================
# !!! HEADER

APP_TITLE = "Blocos Exploratórios Arrematados em Oferta Permanente pela ANP"
APP_SUBTITLE = """    
    Todos os blocos dos 3 primeiros ciclos atendem ao disposto na Resolução CNPE nº 17/2017
    (`www.gov.br/anp/pt-br/servicos/legislacao-da-anp/rl/cnpe/resolucao-cnpe-n17-2017.pdf`).
    """

page_config("wide")

# Use local CSS
local_css("style/style.css")

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)




# %%===========================================================================
# !!! SIDEBAR

sidebar_vspace(10)

sidebar_click_rside()

sidebar_vspace(10)

## Filtro por bacia sedimentar
gdf_op = st_selectbox_filter(gdf_op, 
                             "NOM_BACIA", 
                             "Selecione uma bacia sedimentar:")

sidebar_vspace(10)

## Filtro por Ciclo
gdf_op = st_checkbox_filter(gdf_op, 
                            "RODADA")

sidebar_vspace(10)

## Filtro por Operador
gdf_op = st_selectbox_filter(gdf_op, 
                             "OPERADOR_C", 
                             "Selecione uma operadora responsável:")

sidebar_vspace(10)

## Filtro por PEM
gdf_op = st_slider_vfilter(gdf_op, 
                          'PEM (UT)', 
                          'Selecione um intervalo de PEM (UT):')



# %%===========================================================================
#!!! MAIN PAGE

INITIAL_VIEW_STATE = pdk.ViewState(
    latitude=-15, 
    longitude=-55, 
    zoom=3, 
    max_zoom=16, 
    pitch=0, 
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
    get_line_color="[210, 180, 140]",
)

layer_op1 = pdk.Layer(
    "GeoJsonLayer",
    gdf_op[gdf_op['Ciclo'] == 1],
    pickable=True,
    opacity=0.5,
    filled=True,
    extruded=False,
    wireframe=False,
    line_width_min_pixels=5,
    get_line_color="[255, 255, 255, 255]",
    get_fill_color="[255, 255, 255, 255]",
)

layer_op2 = pdk.Layer(
    "GeoJsonLayer",
    gdf_op[gdf_op['Ciclo'] == 2],
    pickable=True,
    opacity=0.5,
    filled=True,
    extruded=False,
    wireframe=False,
    line_width_min_pixels=5,
    get_line_color="[255, 255, 18, 255]",
    get_fill_color="[255, 255, 18, 255]",
)

layer_op3 = pdk.Layer(
    "GeoJsonLayer",
    gdf_op[gdf_op['Ciclo'] == 3],
    pickable=True,
    opacity=0.5,
    filled=True,
    extruded=False,
    wireframe=False,
    line_width_min_pixels=5,
    get_line_color="[222, 0, 18, 255]",
    get_fill_color="[222, 0, 18, 255]",
)

m = pdk.Deck(
    # map_style=None,
    map_style="mapbox://styles/mapbox/satellite-v9", 
    layers=[bacias, layer_op1, layer_op2, layer_op3], 
    initial_view_state=INITIAL_VIEW_STATE,
    tooltip={"text": """Bacia: {NOM_BACIA} 
             Bloco: {Bloco}
             Rodada: {RODADA}
             PEM: {PEM (UT)} UT
             Área: {Área Arrematada (Km2)} km²
             {Empresa / Consórcio (*operador)}"""}
)

st.pydeck_chart(m, use_container_width=True)




# %%===========================================================================
#!!! FOOTER

st.subheader("🦉 A ANP já está realizando o 4º ciclo da Oferta Permanente")

st.markdown(
"""
    As empresas interessadas devem enviar declarações de interesse até 28/09/2023.
"""
)

st.info(
"""
    "O edital do 4º Ciclo da Oferta Permanente de Concessão (OPC) inclui a área com 
    acumulação de gás natural de Japiim, na Bacia do Amazonas, e 955 blocos exploratórios 
    localizados nas bacias Amazonas, Camamu-Almada, Campos, Ceará, Espírito Santo, 
    Foz do Amazonas, Jacuípe, Paraná, Parecis, Parnaíba, Pelotas, Pernambuco-Paraíba, 
    Potiguar, Recôncavo, Santos, Sergipe-Alagoas e Tucano"
"""
)