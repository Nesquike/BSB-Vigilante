from src.layers.loader import data_loadSinan
import pandas as pd


def teste():
    # Carrega os dados (usando a sua função síncrona atual)
    df = data_loadSinan(2022, 1)

    if df.empty:
        print("O DataFrame está vazio!")
        return

    # CONFIGURAÇÃO DO PANDAS: Força exibir todas as colunas e linhas sem quebrar o layout
    pd.set_option("display.max_columns", None)
    pd.set_option("display.expand_frame_repr", False)

    print("\n--- EXIBINDO AS 10 PRIMEIRAS LINHAS EM FORMATO DE TABELA ---")
    # O .head(10) pega as 10 primeiras linhas. O .round(2) organiza números decimais.
    print(df.head(3).T)


teste()