import pandas as pd
from src.layers.data.cleaner import limpar
from src.layers.data.loader import data_loadSinan

def _filter(ano: int, mes: str=None,uf: str=None, xfilters: dict= None)->int: #função filtro base/principal para as outras

    df = limpar(data_loadSinan(ano))
    condition = pd.Series(True, index=df.index)

    if mes: #verifica se existe busca por mes
        date_search = f"{ano}{mes}"
        condition &= df["DT_NOTIFIC"].astype(str).str.contains(date_search, na=False)
    
    if uf: #verifica se existe busca pela UF
        condition &= (df["SG_UF_NOT"] == uf)
    
    if xfilters: #verifica a existencia de outros filtro (abstração da função para uso com outros parametros)
        for column, value in xfilters.items():
            if column in df.columns:
                condition = condition & (df[column] == value)
    
    return df[condition].shape

def filter_distrib_idade(ano: int, mes: str=None, uf: str=None): #função para filtrar a distribuição de idades
    df = limpar(data_loadSinan(ano))
    condition = pd.Series(True, index=df.index)

    if mes:
        date_search = f"{ano}{mes}"
        condition &= df["DT_NOTIFIC"].astype(str).str.contains(date_search, na=False)
    
    if uf:
        condition &= (df["SG_UF_NOT"] == uf)

    dfFiltrado = df[condition].copy()

    dfFiltrado = dfFiltrado[(dfFiltrado["NU_IDADE_N"] >= 4000) & dfFiltrado["NU_IDADE_N"] <= 4120]
    dfFiltrado["IDADE_LIMPA"] = dfFiltrado["NU_IDADE_N"] - 4000

    counter_idade = dfFiltrado["IDADE_LIMPA"].value_counts().sort_index()

    return counter_idade

def filter_df(ano: int, mes: str=None, uf: str="53"): #função derivada da principal para filtrar somente por UF
    total = _filter(ano, mes, uf)
    return total

def filter_sexo_df(ano: int, sex: str, mes: str=None, uf: str="53"): #função derivada da principal para filtrar sexo na UF
    filtro = {"CS_SEXO": sex}
    total = _filter(ano, mes, uf, filtro)
    return total

def filter_sexo(ano: int, sex: str, mes: str=None): #função derivada da principal para filtrar somente por sexo
    filtro = {"CS_SEXO": sex}
    total = _filter(ano, mes, filtro)
    return total

def filter_idade_df(ano: int, idade: int, mes: str=None, uf: str="53"): #função derivada da principal para filtrar idade especifica na UF
    filtro = {"NU_IDADE_N": idade + 4000}
    total = _filter(ano, mes, uf, filtro)
    return total
