# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:51:10 2023

@author: Josa -- josageof@gmail.com
"""

import streamlit as st


# @st.cache_data(experimental_allow_widgets=True)
def st_selectbox_filter(df, col, msg):
    try:
        selected_item = "Todas as opções"
        items_list = sorted(df[col].astype(str).unique().tolist())
        uniq_items_list = [selected_item] + items_list
        filtered_df = df

        selected_item = st.sidebar.selectbox(msg, uniq_items_list)

        if selected_item != "Todas as opções":
            filtered_df = df[df[col] == selected_item]
        return filtered_df
    except:
        return df



# @st.cache_data(experimental_allow_widgets=True)
def st_selectbox_filter2(df, col, msg):
    try:
        selected_item = "Todas as opções"

        ## Divide a coluna e expande para várias colunas
        items_split = df[col].str.split(',', expand=True)
        ## Converte as colunas em uma unica séria e remove espaços em branco
        uniq_items = items_split.stack().str.strip()
        ## Remove os itens vazios da lista unica
        uniq_items = uniq_items[uniq_items.str.strip().str.len() > 0]
        ## Obtém a lista de itens únicos
        uniq_items_list = sorted(uniq_items.astype(str).unique().tolist())
        uniq_items_list = [selected_item] + uniq_items_list
        ## guarda a df original
        filtered_df = df
        ## Obtem os dados do usuário
        selected_item = st.sidebar.selectbox(msg, uniq_items_list)

        if selected_item != "Todas as opções":
            filtered_df = df[df[col].str.contains(selected_item)]
        return filtered_df
    except:
        return df



# @st.cache_data(experimental_allow_widgets=True)
def st_multiselect_filter(df, col, msg):
    try:
        uniq_values = df[col].unique().tolist()
        ## Obtém uma lista dos itens selecionados
        selected_items = st.sidebar.multiselect(msg, uniq_values)
        ## Se foi selecionado algum item
        if len(selected_items) > 0:
            df = df[df[col].isin(selected_items)]
        return df
    except:
        return df



# @st.cache_data(experimental_allow_widgets=True)
def st_checkbox_filter(df, col):
    try:
        uniq_items_list = sorted(df[col].astype(str).unique().tolist())
        filtered_df = df

        selected_options = []
        for option in uniq_items_list:
            test = st.sidebar.checkbox(option, value=True)
            if test:
                selected_options.append(option)
                
        filtered_df = df[df[col].isin(selected_options)]
        return filtered_df
    except:
        return df



## Filtra linhas baseado em determina coluna
# @st.cache_data(experimental_allow_widgets=True)
def st_slider_vfilter(df, col, msg):
    try:
        min_val = int(min(df[col]))
        max_val = int(max(df[col]))
    
        selected_min, selected_max = st.sidebar.slider(msg, 
                                                    min_value = min_val,
                                                    max_value = max_val,
                                                    value = (min_val, max_val))
        filtered_df = df[(df[col] >= selected_min) & (df[col] <= selected_max)]
        return filtered_df
    except:
        return df



## Filtra colunas numericas baseado no indice
# @st.cache_data(experimental_allow_widgets=True)
def st_slider_hfilter(df, icol_ini, icol_fin, msg):
    try:
        ## Obtém os nomes das colunas indicadas para o filtro
        colunas = df.columns[icol_ini:icol_fin]
        ## Obtém os nomes das demais colunas
        outras_colunas = df.columns[:icol_ini-1].to_list() + df.columns[icol_fin:].tolist()

        col_ini = int(colunas[0])
        col_fin = int(colunas[-1])
        ## Obtém os nomes das colunas selecionadas
        selected_cols = st.sidebar.slider(msg, min_value=col_ini, max_value=col_fin, value=(col_ini, col_fin))
        ## Filtra a lista de col entre as colunas definidas como inicial e final 
        colunas_filtradas = [col for col in colunas if selected_cols[0] <= int(col) <= selected_cols[1]]
        ## Compôe o dataframe com as colunas filtradas mais as demais colunas
        filtered_df = df[outras_colunas + colunas_filtradas]
        ## Soma as linhas das colunas filtradas e compôe a coluna 'SUM'
        filtered_df['SUM'] = filtered_df[colunas_filtradas].sum(axis=1)
        return filtered_df, colunas_filtradas
    except:
        return df