# Seu arquivo de teste de laboratório
import matplotlib.pyplot as plt
from src.layers.business.analytics import (
    graphCreator_serietemporal,
    graphCreator_distribuicaosexo,
    graphCreator_regiao,
    graphCreator_fxetaria
)
ano = 2025

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
    foto_pizza = graphCreator_distribuicaosexo(ano=ano)

    if foto_pizza is not None:
        plt.show() # Vai abrir a janela com o gráfico de rosca na tela!
        print("-> Sucesso! Gráfico de pizza renderizado.")
    else:
        print("-> Falha ao gerar o gráfico de pizza.")

def barras_regiao():
    print(f"[Teste] Gerando gráfico de barras por região para {ano}...")
    foto_barras = graphCreator_regiao(ano=ano)

    if foto_barras is not None:
        print("-> Sucesso! Gráfico de barras gerado.")
        plt.show()  # Abre a janela interativa com o ranking na tela
    else:
        print("-> Falha ao gerar o gráfico de barras por região.")

def barras_fxetaria():
    print(f"[Teste] Gerando gráfico de barras por fxetária para {ano}...")
    foto_barras = graphCreator_fxetaria(ano=ano)

    if foto_barras is not None:
        print("Sucesso! Gráfico gerado.")
        plt.show()
    else:
        print("Falha ao gerar o gráfico.")


barras_fxetaria()