import streamlit as st
from src.layers.business.analytics import (graphCreator_serietemporal, graphCreator_regiao, graphCreator_distribuicaosexo, graphCreator_fxetaria)

def render_serie_temporal(ano: int):
    fig = graphCreator_serietemporal(ano)
    if fig:
        st.pyplot(fig, width="content", clear_figure=True)
    else:
        st.info("Não há dados temporais para exibir neste período")
        
def render_casos_regiao(ano: int):
    fig = graphCreator_regiao(ano)
    if fig:
        st.pyplot(fig, width="content", clear_figure=True)
    else:
        st.info("Não há dados regionais para exibir")
        
def render_casos_distribuicao_sexo(ano: int):
    fig = graphCreator_distribuicaosexo(ano)
    if fig:
        st.pyplot(fig, width="content", clear_figure=True)
    else:
        st.info("Não há dados de distribuição de sexo para exibir")

def render_casos_faixa_etaria(ano: int):
    fig = graphCreator_fxetaria(ano)
    if fig:
        st.pyplot(fig, width="content", clear_figure=True)
    else:
        st.info("Não há dados referentes à faixa etaria a exibir")