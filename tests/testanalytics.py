# Seu arquivo de teste de laboratório
import matplotlib.pyplot as plt
from src.layers.business.analytics import (
    graphCreator_serietemporal,
    graphCreator_distribuiçãosexo
)
ano = 2026

def serie_tempo():
    print(f"[Teste] Gerando gráfico de linhas para o ano de {ano}...")
    # 1. Captura o gráfico que a função gerou e guardou na memória
    foto_grafico = graphCreator_serietemporal(ano=ano)
    if foto_grafico is not None:
    # 2. Exibe o gráfico na tela APENAS aqui no ambiente de teste
        plt.show()
        print("-> Sucesso! Gráfico exibido perfeitamente.")
    else:
        print("-> Falha: O gráfico retornou vazio (sem dados).")


def sex_pizza():
    # No final do seu testanalytics.py:
    print(f"[Teste] Gerando gráfico de pizza por sexo para {ano}...")
    foto_pizza = graphCreator_distribuiçãosexo(ano=ano)

    if foto_pizza is not None:
        plt.show() # Vai abrir a janela com o gráfico de rosca na tela!
        print("-> Sucesso! Gráfico de pizza renderizado.")
    else:
        print("-> Falha ao gerar o gráfico de pizza.")

sex_pizza()