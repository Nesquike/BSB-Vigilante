from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from src.layers.business.process import(
    casos_por_regiao,
    serie_temporal,
    distribuicao_faixa_etaria,
    distribuicao_sexo,
    regiao_com_mais_casos,
    total_casos
)

from src.layers.data.filters import _filter

def graphCreator_serietemporal(ano: int):
    df = _filter(ano=ano, uf="53", return_df=True)
    if df.empty:
        return None
    prcssd_serie = serie_temporal(df)
    if prcssd_serie.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(10,4.5))

    ax.plot(
        prcssd_serie.index.astype(str),
        prcssd_serie.values,
        marker= 'o',
        color = "#006CC5"
    )

    ax.set_title( 
        f"Evolução Mensal dos casos de Denguue no DF em {ano}",
        fontsize = 14,
        fontname= "Arial",
        fontweight="bold"
        )
    ax.set_xlabel("Meses do ano", fontsize=10, fontname="Arial")
    ax.set_ylabel("Número de casos", fontsize=10, fontname="Arial")

    plt.xticks(rotation=30)
    plt.tight_layout()

    return fig