# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 23:55:25 2023

@author: Josa -- josageof@gmail.com
"""

import pandas as pd
import streamlit as st
import colorsys


def sidebar_vspace(height):
    st.sidebar.markdown(f'<div style="height: {height}px;"></div>', unsafe_allow_html=True)
    
    
def sidebar_click_rside():
    st.sidebar.info("Use os filtros abaixo para interagir com a visualização ao lado 👉")
    

# Função para mapear um valor da coluna 'PROF_SOND' para uma cor RGB entre azul e vermelho
def map_rgb_from_col(df, col):
    min_value = df[col].min()
    max_value = df[col].max()
    rgb = []
    ## Normaliza o valor para um intervalo entre 0 e 1
    for value in df[col]:
        normalized_value = (value - min_value) / (max_value - min_value)
        ## Usa colorsys para criar uma cor interpolada de azul a vermelho
        hue = (1.0 - normalized_value) * 0.7  # 0.7 é a faixa de cores de azul a vermelho em HSV
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        ## Converte a cor para o formato [R, G, B]
        rgb.append([int(r * 255), int(g * 255), int(b * 255)])

    df['RGB'] = pd.DataFrame({'RGB': rgb})
    return df


uf_centers = {
    "AC": (-8.77, -70.55),
    "AL": (-9.71, -35.73),
    "AP": (0.90, -52.00),
    "AM": (-3.47, -65.10),
    "BA": (-12.97, -38.50),
    "CE": (-3.71, -38.54),
    "DF": (-15.78, -47.93),
    "ES": (-19.19, -40.34),
    "GO": (-16.64, -49.31),
    "MA": (-2.55, -44.30),
    "MT": (-12.64, -55.42),
    "MS": (-20.51, -54.54),
    "MG": (-18.52, -44.04),
    "PA": (-5.53, -52.29),
    "PB": (-7.06, -35.55),
    "PR": (-24.89, -51.55),
    "PE": (-8.28, -35.07),
    "PI": (-8.28, -43.68),
    "RJ": (-22.25, -42.66),
    "RN": (-5.81, -35.21),
    "RS": (-30.01, -51.22),
    "RO": (-10.94, -62.83),
    "RR": (1.99, -61.33),
    "SC": (-27.59, -48.55),
    "SP": (-23.55, -46.64),
    "SE": (-10.95, -37.07),
    "TO": (-9.47, -48.48),
}


color_brewer_blue_scale = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]
