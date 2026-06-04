import streamlit as st
from src.layers.business.analytics import (graphCreator_serietemporal, graphCreator_regiao, graphCreator_distribuicaosexo)

def render_serie_temporal(ano: int):
    st.subheader(f"Evolução Mensal ({ano})")
    fig = graphCreator_serietemporal(ano)
    if fig:
        st.pyplot(fig, width="stretch", clear_figure=True)
    else:
        st.info("Não há dados temporais para exibir neste período")
        
def render_casos_regiao(ano: int):
    st.subheader(f"Casos por Região Administrativa")
    fig = graphCreator_regiao(ano)
    if fig:
        st.pyplot(fig, width="stretch", clear_figure=True)
    else:
        st.info("Não há dados regionais para exibir")
        
def render_casos_distribuicao_sexo(ano: int):
    st.subheader(f"Distribuição por Sexo")
    fig = graphCreator_distribuicaosexo(ano)
    if fig:
        st.pyplot(fig, width="stretch", clear_figure=True)
    else:
        st.info("Não há dados de distribuição de sexo para exibir")