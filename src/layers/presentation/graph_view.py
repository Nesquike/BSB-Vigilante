import streamlit as st
from src.layers.presentation.dashboard import mostrar_dashboard
from src.layers.data.filters import filter_df

def render():
    st.sidebar.title("Navegação")
    view = st.sidebar.radio("Selecione a seção:", ["Dashboard", "Cuidados e Prevenção"])
    
    ano_selecionado = st.sidebar.selectbox("Ano", [2025, 2024, 2023, 2022, 2021, 2020])

    if view == "Dashboard":
        with st.spinner("Carregando dados..."):
            df = filter_df(ano=ano_selecionado)
            
        if df.empty:
            st.warning(f"⚠️ Não há dados disponíveis para o ano de {ano_selecionado}. O cache pode estar vazio ou o arquivo corrompido.")
        else:
            mostrar_dashboard(df, ano_selecionado)
        
    else:
        st.subheader("Cuidados e Prevenção")
        st.write("A prevenção é a melhor arma contra Dengue, Zika e Chikungunya.")
        st.info("💧 Elimine a água parada — verifique vasos, pneus e calhas.")
        st.success("🏠 Proteja sua casa — mantenha caixas d'água fechadas e use telas.")
        st.warning("🦟 Use repelente — aplique nas áreas expostas.")