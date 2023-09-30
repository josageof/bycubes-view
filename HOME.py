# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 21:45:33 2023

@author: Josa -- josageof@gmail.com
"""

import streamlit as st


# %%===========================================================================
# !!! SIDEBAR

st.set_page_config(
    page_title="byCubes View",
    page_icon="🎯",
)

st.sidebar.success("Clique acima 👆 e divirta-se!")


st.sidebar.info(
    """
    </> Developed by Francisco Josa: <josageof@gmail.com>
    [GitHub](https://github.com/josageof) | [LinkedIn](https://www.linkedin.com/in/josageof)
    """
)



# %%===========================================================================
# !!! MAIN PAGE

st.write("# Bem vindo ao byCubes View! 👋")

# Adiciona um espaço em branco para melhorar a formatação
st.markdown(f'<div style="height: {30}px;"></div>', unsafe_allow_html=True)

# Descreve o propósito do dashboard
st.markdown(
    """
    ###### 🗃️ Aqui você encontrará uma amostra visual da nossa Exploração de Dados Online.
    
    ###### 👈 **Selecione um link no painel à esquerda** e explore análises e insights❕
    
    ###### 📣 Se sentir confortável, compartilhe seus achados com amigos: [bycubes-view.app](https://bycubes-view.streamlit.app/)
"""
)

# Adiciona mais espaço em branco
st.markdown(f'<div style="height: {15}px;"></div>', unsafe_allow_html=True)

st.markdown(
    """
    ### O que você encontrará aqui?
    - <span style="color: #FFC83D"><strong>Dados</strong></span> sobre energia, agricultura, telecomunicações e meio ambiente
    - Resumos <span style="color: #FFC83D"><strong>informativos</strong></span> sobre esses temas
    - <span style="color: #FFC83D"><strong>Visualizações</strong></span> interativas e amigáveis
    ### Como isso pode ser útil?
    - Tome <span style="text-decoration: underline"><strong>decisões</strong></span> informadas com base em análises de dados
    - Compreenda <span style="text-decoration: underline"><strong>tendências</strong></span> e padrões em diferentes setores
    - Explore informações públicas brasileiras de forma <span style="text-decoration: underline"><strong>acessível</strong></span>
""", unsafe_allow_html=True
)

