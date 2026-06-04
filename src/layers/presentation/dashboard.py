import streamlit as st
from src.layers.presentation.charts import (
    render_serie_temporal,
    render_casos_regiao,
    render_casos_distribuicao_sexo
)
from src.layers.business.process import total_casos, regiao_com_mais_casos

def mostrar_dashboard(df, ano: int):
    st.subheader("Indicadores Gerais")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Casos", total_casos(df))
    with col2:
        st.metric("Região com mais casos", regiao_com_mais_casos(df))

    st.subheader("Gráficos")
    render_serie_temporal(ano)
    render_casos_distribuicao_sexo(ano)
    render_casos_regiao(ano)