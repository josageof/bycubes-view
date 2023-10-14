# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 19:08:32 2023

@author: Josa -- josageof@gmail.com
"""

import pandas as pd
import geopandas as gpd
import streamlit as st
import pydeck as pdk

from utils.components import page_config, sidebar_vspace, sidebar_click_rside
from utils.filters import st_selectbox_filter2, st_multiselect_filter, st_slider_vfilter


# %%===========================================================================
# !!! DATA

## Carrega as localizações das usinas nucleares ao redor do mundo
nuclear_power_plant_file = "data/world_nuclear_power_plant_2023/World_Nuclear_Power_Plant_2023.shp"

## Ler os arquivos como geopandas
gdf_usinas = gpd.read_file(nuclear_power_plant_file)

gdf_usinas = gdf_usinas.dropna(subset=['country', 'type', 'status'])

gdf_usinas = gdf_usinas[gdf_usinas['grosspower'] != 0]



# %%===========================================================================
# !!! HEADER

APP_TITLE = "Mapa das Usinas Nucleares ao Redor do Mundo"
APP_SUBTITLE = """
    Usina nuclear é uma instalação industrial empregada para produzir eletricidade a partir de energia nuclear. 
    Caracteriza-se pelo uso de materiais radioativos que produzem calor como resultado de reações nucleares
    (`www.iaea.org`).
    """

page_config("wide")

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)



# %%===========================================================================
# !!! SIDEBAR

sidebar_vspace(10)

sidebar_click_rside()

sidebar_vspace(10)

# Filtro de tipos de usinas
gdf_usinas = st_multiselect_filter(gdf_usinas, 
                                   'type', 
                                   'Selecione os tipos de usinas')

sidebar_vspace(10)

gdf_usinas = st_slider_vfilter(gdf_usinas, 
                               'grosspower', 
                               'Selecione a potência da usina (MWe):')

sidebar_vspace(10)

# Filtro por status da usina
gdf_usinas = st_selectbox_filter2(gdf_usinas, 
                                  "status", 
                                  "Selecione um status das usinas:")




# %%===========================================================================
#!!! MAIN PAGE

ICON_URL = 'https://upload.wikimedia.org/wikipedia/commons/b/b8/NuclearPowerPlant_Icon.svg'

icon_data = {
    "url": ICON_URL,
    "width": 100,
    "height": 100,
    "anchorY": 100,
}

## populate gdf_usinas with icon data 
gdf_usinas['icon'] = [icon_data for _ in gdf_usinas.index]

usinas = pdk.Layer(
    "IconLayer",
    gdf_usinas,
    get_icon="icon",
    get_size=4,
    size_scale=5,
    get_position=["longitude", "latitude"],
    pickable=True
)

initial_view = pdk.ViewState(
    latitude=20, 
    longitude=15, 
    zoom=1.5,
    max_zoom=16, 
    pitch=0, 
    bearing=0,
    wrapLongitude=True  # Permite que o mapa se repita horizontalmente
)

m = pdk.Deck(
    initial_view_state=initial_view,
    # map_style=None,
    map_style="mapbox://styles/mapbox/satellite-v9", 
    layers=[usinas], 
    tooltip={"text": """{powerplant}
              Tipo: {type}
              Potência: {grosspower} MWe
              País: {country}"""}
)

st.pydeck_chart(m, use_container_width=True)


# st.write(gdf_usinas)



# %%===========================================================================
#!!! FOOTER

st.subheader("🦉 Curiosidades sobre as descobertas das principais formas de radiação")

st.markdown(
"""
    O raio-X foi descoberto por _Wilhelm Röntgen_ em 1895, ao passar uma corrente elétrica por um tubo de vidro. 
    No ano seguinte, _Henri Becquerel_ demonstrou as radiações Beta e Alfa ao escurecer placas fotográficas 
    através de Urânio e Radio. No mesmo período, a radiação Gama veio a ser compreendida por _Pierre Curie_ e
    _Marie Curie_, fenômeno ao qual deram o nome de “radioatividade”.
"""
)

st.info(
"""
    "
    Os estudos da radiação atômica, transformações atômicas e fissão nuclear foram inicialmente desenvolvido 
    com intuito militar, principalmente de 1895 a 1945, grande parte nos últimos seis anos desse período. 
    De 1939 a 1945 a maior parte do desenvolvimento esteve focado em desenvolver a bomba atômica. 
    De 1945 para frente a atenção sobre a bomba atômica foi diminuída, porém seu estudo continua forte 
    principalmente nas áreas de energia e propulsão naval controlada."
"""
)