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

from src.layers.data.filters import (
    _filter,
    filter_cross,
    filter_df,
    filter_idade,
    filter_regiao_df,
    filter_sexo
)

def graphCreator_serietemporal(ano: int): #função criadora de gráficos lineares para evolução do numero de casos de dengue no DF
    df = filter_df(ano=ano)
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
        f"Evolução Mensal dos casos de Dengue no DF em {ano}:",
        fontsize = 14,
        fontname= "Arial",
        fontweight="bold"
        )
    ax.set_xlabel("Meses do ano", fontsize=10, fontname="Arial")
    ax.set_ylabel("Número de casos", fontsize=10, fontname="Arial")

    plt.xticks(rotation=30)
    plt.tight_layout()

    return fig

def graphCreator_distribuiçãosexo(ano: int): #função criadora de gráficos pizza da distribuição de sexos no DF
    df = _filter(ano=ano, uf="53")
    if df.empty:
        return None
    prcssd_sex = distribuicao_sexo(df)
    if prcssd_sex.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(7,7))

    cores_map = {
        "F": "#8c0000",
        "M": "#0000b9",
        "I": "#208800"
    }

    cores = [cores_map.get(sexo, "#B47500")for sexo in prcssd_sex.index]

    wedges, texts, autotexts = ax.pie(
        prcssd_sex.values,
        labels=prcssd_sex.index,
        autopct='%1.1f%%',
        colors=cores,
        textprops=dict(color="black", fontsize=10, fontweight="bold")
    )

    plt.setp(autotexts, size=10, weight="bold", color="white")
    ax.set_title(f"Distribuição de casos de Dengue por Sexo no DF {ano}:", fontsize=12, pad=20, fontweight="bold")
    ax.axis("equal")
    plt.tight_layout()

    return fig

