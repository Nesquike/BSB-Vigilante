import streamlit as st
from src.layers.presentation.dashboard import mostrar_dashboard
from src.layers.data.filters import filter_df

def render():
    # Título do App
    st.sidebar.markdown(
        "<h1 style='text-align: center; color: #006CC5;'>🦟 BSB Vigilante</h1>",
        unsafe_allow_html=True
    )
    st.sidebar.divider()

    # Seção de Navegação
    st.sidebar.markdown("### 🧭 Menu")
    view = st.sidebar.radio(
        "Selecione a seção:", 
        ["📊 Dashboard", "🛡️ Cuidados e Prevenção"],
        label_visibility="collapsed" # Esconde o texto duplicado em cima das opções
    )
    
    st.sidebar.divider()

    # Seção de Filtros
    st.sidebar.markdown("### 📅 Filtros")
    ano_selecionado = st.sidebar.selectbox("Selecione o Ano", [2025, 2024, 2023, 2022, 2021, 2020])
    
    # Roteamento
    if view == "📊 Dashboard":
        with st.spinner("Processando dados epidemiológicos..."):
            df = filter_df(ano=ano_selecionado)

        if df.empty:
            st.error(f"⚠️ A base de dados do SINAN para {ano_selecionado} está vazia ou indisponível no momento.")
        else:
            mostrar_dashboard(df, ano_selecionado)

    else:
        st.title("🛡️ Cuidados e Prevenção")
        st.markdown("A prevenção continua sendo a melhor arma contra **Dengue, Zika e Chikungunya**.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Grid para as dicas ficarem parecendo "Cards"
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("💧 **Elimine a água parada**\n\nVerifique e esvazie vasos de plantas, pneus velhos, garrafas e limpe as calhas regularmente.")
            st.warning("🦟 **Use repelente**\n\nAplique repelente nas áreas expostas da pele, especialmente ao amanhecer e entardecer.")

        with col2:
            st.success("🏠 **Proteja sua casa**\n\nMantenha caixas d'água bem fechadas, instale telas nas janelas e limpe ralos com frequência.")
            st.error("🩺 **Atenção aos sintomas**\n\nEm caso de febre alta, dores no corpo e manchas, não se automedique. Procure um posto de saúde.")