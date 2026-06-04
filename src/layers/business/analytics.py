from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from src.layers.data.cleaner import REGIAO_VALIDAS
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

def graphCreator_regiao(ano: int): #função criadora de gráficos/histogramas por número de casos por região do DF
    df = filter_df(ano)
    if df.empty:
        return None
    prcssd_rg = casos_por_regiao(df)
    if prcssd_rg.empty:
        return None
    
    nomes_ra = prcssd_rg.index.map(REGIAO_VALIDAS).fillna("Outras Regiões")
    
    qtd_barras = len(prcssd_rg)
    if qtd_barras <= 3:
        largura_dinamica = 6.5
        largura_barra = 0.45
    else:
        largura_dinamica = max(7, min(15, qtd_barras * 1.1))
        if qtd_barras <= 12:
            largura_barra = 0.45
        else:
            largura_barra = 0.35

    fig, ax = plt.subplots(figsize=(largura_dinamica, 6))

    bars = ax.bar(
        nomes_ra.astype(str),
        prcssd_rg.values,
        color= "#006CC5",
        edgecolor= "black",
        linewidth=0.8,
        width=largura_barra
    )

    ax.set_title(f"Ranking de Casos de Dengue por Região Administrativa {ano}:", fontsize=13, pad=20, fontweight="bold")
    ax.set_xlabel("Regiões do DF", fontsize=11, labelpad=10)
    ax.set_ylabel("Quantidade de Casos Notificados", fontsize=11, labelpad=10)

    ax.tick_params(axis='x', rotation=20, labelsize=9)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    maior_valor = prcssd_rg.max()
    ax.set_ylim(0, maior_valor * 1.15)

    for barra in bars: #add numeros em cima de cada barra
        altura = barra.get_height()
        ax.annotate(
            f'{int(altura)}',
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center', 
            va='bottom', 
            fontsize=9, 
            fontweight="bold"
        )

    plt.tight_layout()

    return fig