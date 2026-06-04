# Seu arquivo de teste de laboratório
import matplotlib.pyplot as plt
from src.layers.business.analytics import graphCreator_serietemporal
ano = 2026

print(f"[Teste] Gerando gráfico de linhas para o ano de {ano}...")
# 1. Captura o gráfico que a função gerou e guardou na memória
foto_grafico = graphCreator_serietemporal(ano=ano)

if foto_grafico is not None:
    # 2. Exibe o gráfico na tela APENAS aqui no ambiente de teste
    plt.show()
    print("-> Sucesso! Gráfico exibido perfeitamente.")
else:
    print("-> Falha: O gráfico retornou vazio (sem dados).")