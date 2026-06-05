import streamlit as st
from src.layers.presentation.charts import (
    render_serie_temporal,
    render_casos_regiao,
    render_casos_distribuicao_sexo
)
from src.layers.business.process import total_casos, regiao_com_mais_casos

def mostrar_dashboard(df, ano: int):
    st.markdown("### 📌 Visão Geral do Período")
    
    col1, col2 = st.columns(2)
    with col1:
        total = total_casos(df)
        st.metric("Total de Casos Notificados", f"{total:,}".replace(",", "."))
    with col2:
        st.metric("Região com Mais Casos", regiao_com_mais_casos(df))
        
    st.divider()

    st.markdown("### 📈 Análise Detalhada")    
    
    row1_col1, row1_col2 = st.columns([2, 1.7])
    row2, x = st.columns([1.5,1])

    with row1_col1:
        render_serie_temporal(ano)
    
    with row1_col2: 
        render_casos_distribuicao_sexo(ano)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with row2:
        render_casos_regiao(ano)