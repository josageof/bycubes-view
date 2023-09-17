# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:50:50 2023

@author: Josa -- josageof@gmail.com
"""

# import folium
import streamlit as st
import leafmap.foliumap as leafmap
import altair as alt
from PIL import Image

from proc_data import bring_data

# %%===========================================================================
# !!! DATA

# Carrega os dados de emissão de GEE
df = bring_data()


# Carregar os limites dos estados brasileiros a partir de um arquivo GeoJSON
br_states_geojson_file = "data/brazil-states.geojson"


# %%===========================================================================
# !!! PAGE TITLE

APP_TITLE = "Greenhouse Gas Emissions in Brazil up to 2021"
APP_SUBTITLE = """
    The information comes from SEEG10 Report, the Climate Observatory's 
    Greenhouse Gas Emission Estimation System (`seeg.eco.br`).
    """

st.set_page_config(layout="wide")

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)



# %%===========================================================================
# !!! SIDEBAR

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

logo_file = Image.open('assets/bycubes.png')
with st.sidebar:
    st.image(logo_file, width=100)

st.sidebar.title("Welcome, really enjoy it 👋")

st.sidebar.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)

st.sidebar.info("Click the filters below to interact with the charts on the right side.")

st.sidebar.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

# !!! Filtro por ano
min_year = min(df.columns[11:-2].astype(int))
max_year = max(df.columns[11:-2].astype(int))
selected_year = str(
    st.sidebar.slider(
        "Select the Year:", min_value=min_year, max_value=max_year, value=max_year
    )
)

st.sidebar.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

# !!! Filtro por atividade economica

atividades_economicas = sorted(df["Atividade Econômica"].astype(str).unique().tolist())
atividades_unicas = ["All activities"] + atividades_economicas
selected_activ = st.sidebar.selectbox(
    "Select the economic activity:", atividades_unicas
)

# filtered_df = df[df['Atividade Econômica'] == selected_activ]
if selected_activ == "All activities":
    filtered_df = df
else:
    filtered_df = df[df["Atividade Econômica"] == selected_activ]


st.sidebar.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)

st.sidebar.info(
    """
    Francisco Josa: <josageof@gmail.com>
    [GitHub](https://github.com/josageof) | [LinkedIn](https://www.linkedin.com/in/josageof)
    """
)


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
    
    state_style = {"fillOpacity": 0, "color": "gray", "weight": 1.5}
    
    m.add_geojson(br_states_geojson_file, layer_name="Brazilian States", style=state_style)
    # folium.GeoJson(
    #     brazil_states_geojson_url,
    #     style_function=lambda feature: state_style,
    #     name="Brazilian States",
    # ).add_to(m)
    
    # Adicionar a camada de heatmap
    m.add_heatmap(
        filtered_df,
        lat="latitude",
        lon="longitude",
        value=selected_year,
        name="Heat map",
        radius=40,
    )
    
    # folium.LayerControl(position='topright', collapsed=False, autoZIndex=False).add_to(m)
    
    m.to_streamlit(height=500)
    

with row1_col2:
    anos = filtered_df.columns[31:-2].to_list()
    colunas = ['Nível 1 - Setor'] + anos
    df_setor = filtered_df[colunas].groupby('Nível 1 - Setor', as_index=False).sum()
    df_setor.rename(columns={'Nível 1 - Setor': 'Setor'}, inplace=True)
    y_label_format = 'datum.value >= 1e9 ? format(datum.value / 1e9, ".1f") + " Bi" : format(datum.value / 1e6, ".1f") + " Mi"'
    color_scale = alt.Scale(domain=['Mudança de Uso da Terra e Floresta', 'Processos Industriais', 'Resíduos', 'Agropecuária', 'Energia'],
                            range=["#95C11F", "#7F4337", "#76BDDB", "#F1D774", "#C2151C"])

    # Transforme o DataFrame em um formato longo para o Altair
    melted_df = df_setor.melt(id_vars=['Setor'], 
                               value_vars=anos, 
                               var_name='Ano', 
                               value_name='Valor'
                               )
    # Crie um gráfico de histograma empilhado em Altair
    chart = alt.Chart(melted_df).mark_bar().encode(
        x=alt.X('Ano:N', title='Year'),
        y=alt.Y('sum(Valor):Q', 
                axis=alt.Axis(format='-s', title='Tons of CO2e (GWP – AR5)', labelExpr=y_label_format)),
        # color=alt.Color('Setor:N'),
        color=alt.Color('Setor:N', scale=color_scale),
        order=alt.Order('Setor', sort='ascending')
    ).properties( 
        height=550
    ).configure_legend(
        labelFontSize=10,
        orient='top'
    )
    
    st.altair_chart(chart)


# %%===========================================================================
#!!! FOOTER

st.subheader("Brazil's Goals: 2025 and 2030")

st.markdown(
"""
    Emissions reduction for 2025 and 2030, included in the NDC (Nationally Determined Contribution)
    and enacted in the Paris Agreement in June 2017.
"""
)

st.info(
"""
    "The country committed to reduce its net emissions by 37% by 2025 compared to 2005 levels, which
    would amount to a maximum emission of 1.3 billion net tons of CO2 equivalent (GtCO2e) in that year. 
    In addition to the 2025 target, the NDC indicated a commitment for 2030, with a 43% reduction, 
    also relative to 2005."
"""
)
