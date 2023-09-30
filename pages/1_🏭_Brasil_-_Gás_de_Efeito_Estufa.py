# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:50:50 2023

@author: Josa -- josageof@gmail.com
"""

import pandas as pd
import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from streamlit_echarts import st_echarts

from utils.components import uf_centers
from utils.components import sidebar_vspace, sidebar_click_rside
from utils.filters import st_selectbox_filter, st_slider_hfilter


# %%===========================================================================
# !!! DATA

br_states_geojson_file = "data/brazil-states.geojson"

## Ler o arquivo geojson como geopandas
gdf_estados = gpd.read_file(br_states_geojson_file)

gee_data_file = 'data/gee_por_estado.csv'
ativ_econ_file = 'data/atividade_economica.csv'

df_gee = pd.read_csv(gee_data_file, encoding='utf-8', sep=';', low_memory=False)
df_ativ_econ = pd.read_csv(ativ_econ_file, encoding='utf-8', sep=';')

# Realize a junção (join) com base na coluna "SIGLA"
df_gee = df_gee.merge(df_ativ_econ, on='SIGLA', how='left')
# Copie os valores da coluna 'Atividade Econômica' para 'SIGLA'
df_gee['SIGLA'] = df_gee['Atividade Econômica']
df_gee.drop(columns=['Atividade Econômica'], inplace=True)
df_gee.rename(columns={'SIGLA': 'Atividade Econômica'}, inplace=True)
df_gee = df_gee.dropna(subset=['Atividade Econômica'])


## CO2e (t): dióxido de carbono equivalente em toneladas
## AR5: Quinto relatório de avaliação do IPCC sobre o aquecimento global

df_gee_emission = df_gee[df_gee['Emissão / Remoção / Bunker'] == 'Emissão']

## O "CO2e (t) GWP-AR5" é uma medida que representa as emissões totais de gases de efeito estufa 
## em dióxido de carbono equivalente em toneladas, usando o Potencial de Aquecimento Global 
## conforme calculado no Quinto Relatório de Avaliação do IPCC ao longo de um período de 100 anos. 
df_gee_co2e_emission = df_gee_emission[df_gee_emission['Gás'] == 'CO2e (t) GWP-AR5']

df = df_gee_co2e_emission.dropna(subset=['Estado'])
df.iloc[:,11:] = df.iloc[:,11:].fillna(0).astype(float)

## Calcula o centro de cada estado
df["latitude"] = df["Estado"].map(lambda uf: uf_centers[uf][0])
df["longitude"] = df["Estado"].map(lambda uf: uf_centers[uf][1])

## Remove os dados de 1970 a 1989
periodo_antigo = [str(ano) for ano in range(1970, 1990)]
df = df.drop(periodo_antigo, axis=1)



# %%===========================================================================
# !!! HEADER

st.set_page_config(
    layout="wide",
    page_title="byCubes View",
    page_icon="👋",
)

# add_logo("assets/bycubes.png", height=100)

APP_TITLE = "Estimativa de Emissões de Gases de Efeito Estufa por Estado"
APP_SUBTITLE = """
    Informação do Relatório SEEG10, Sistema de Estimativa de Emissões de Gases 
    de Efeito Estufa do Observatório do Clima (`seeg.eco.br`).
    """

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)




# %%===========================================================================
# !!! SIDEBAR

sidebar_vspace(10)

sidebar_click_rside()

sidebar_vspace(10)


## !!! Filtro por Setor Economico
filtered_df = st_selectbox_filter(df, 
                                  'Nível 1 - Setor',
                                  'Selecione o Setor Econômico:')


sidebar_vspace(10)


## !!! Filtro por Atividade Aconomica
filtered_df = st_selectbox_filter(filtered_df, 
                                  'Atividade Econômica',
                                  'Selecione a Atividade Econômica:')


sidebar_vspace(10)


## !!! Filtro por anos
filtered_df, filtered_col = st_slider_hfilter(filtered_df, 
                                              11, 
                                              -2, 
                                              "Selecione o período:")




# %%===========================================================================
#!!! MAIN PAGE

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    m = leafmap.Map(
        center=[-15, -55],
        zoom=4,
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
    )
    
    # Adicionar o basemap
    usgs_url = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
    m.add_wms_layer(
        url=usgs_url, layers="0", name="USGS Imagery", format="image/png", shown=True
    )
    
    state_style = {"fillOpacity": 0, "color": "gray", "weight": 1}
    
    m.add_geojson(br_states_geojson_file, layer_name="Brazilian States", style=state_style)
    
    # Adicionar a camada de heatmap
    m.add_heatmap(
        filtered_df,
        lat="latitude",
        lon="longitude",
        value='SUM',
        name="Heat map",
        radius=30,
    )
    
    m.to_streamlit(height=500)


with row1_col2:
    anos = [str(ano) for ano in range(1990, 2022)]
    colunas = ['Nível 1 - Setor'] + anos
    df_setores = df[colunas].groupby('Nível 1 - Setor', as_index=False).sum()
    df_setores = df_setores.set_index('Nível 1 - Setor').transpose()
    df_setores = df_setores[[
        'Agropecuária',
        'Energia',
        'Resíduos',
        'Processos Industriais',
        'Mudança de Uso da Terra e Floresta',
    ]]
    # df_setores = df_setores.astype(int)

    options = {
        "title": {"text": "Agentes:"},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}},
        },
        "legend": {"data": df_setores.columns.to_list()},
        "toolbox": {"feature": {"saveAsImage": {}}},
        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
        "xAxis": [{"type": "category", "boundaryGap": False, "data": df_setores.index.to_list()}],
        "yAxis": [{"type": "value"}],
    
        "series": [
            {
                "name": col,
                "type": "line",
                "stack": "Total",
                "areaStyle": {},
                "emphasis": {"focus": "series"},
                "data": df_setores[col].to_list(),
            } for col in df_setores.columns
        ],
    }

    st_echarts(options=options, height="520px")

    


# %%===========================================================================
#!!! FOOTER

st.subheader("🦉 Metas do Brasil: 2025 e 2030")

st.markdown(
"""
    Redução de emissões para 2025 e 2030, incluída na NDC (Nationally Determined Contribution)
    e promulgada no Acordo de Paris em junho de 2017.
"""
)

st.info(
"""
    "O país comprometeu-se a reduzir as suas emissões líquidas em 37% até 2025 em comparação com os 
    níveis de 2005, o que equivale a uma emissão máxima de 1,3 bilhões de toneladas líquidas de CO2 
    equivalente (GtCO2e) nesse ano. Além da meta para 2025, a NDC indicou o compromisso para 2030, 
    com a redução de 43%, também em relação a 2005."
"""
)
