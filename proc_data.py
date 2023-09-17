# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:51:39 2023

@author: Josa -- josageof@gmail.com
"""

# from IPython import get_ipython
# get_ipython().run_line_magic('reset', '-f')


import pandas as pd


# %%===========================================================================
# !!! IMPORT DATA

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


# %%===========================================================================
# !!! FILT/FIX DATA

## CO2e (t): dióxido de carbono equivalente em toneladas
## AR5: Quinto relatório de avaliação do IPCC sobre o aquecimento global

df_gee_emission = df_gee[df_gee['Emissão / Remoção / Bunker'] == 'Emissão']

## O "CO2e (t) GWP-AR5" é uma medida que representa as emissões totais de gases de efeito estufa 
## em dióxido de carbono equivalente em toneladas, usando o Potencial de Aquecimento Global 
## conforme calculado no Quinto Relatório de Avaliação do IPCC ao longo de um período de 100 anos. 
df_gee_co2e_emission = df_gee_emission[df_gee_emission['Gás'] == 'CO2e (t) GWP-AR5']

df_gee_co2e = df_gee_co2e_emission.dropna(subset=['Estado'])
df_gee_co2e.iloc[:,11:] = df_gee_co2e.iloc[:,11:].fillna(0).astype(float)

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

df_gee_co2e["latitude"] = df_gee_co2e["Estado"].map(lambda uf: uf_centers[uf][0])
df_gee_co2e["longitude"] = df_gee_co2e["Estado"].map(lambda uf: uf_centers[uf][1])


# %%===========================================================================
# !!! DELIVERY DATA

def bring_data():
    return df_gee_co2e