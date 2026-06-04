import streamlit as st
from src.layers.presentation.graph_view import render

# Configuração da página
st.set_page_config(
    page_title="BSB Vigilante",
    layout="wide",
    page_icon="🦟"
)

def main():
    render()

if __name__ == "__main__":
    main()