import pandas as pd
from src.layers.data.cleaner import limpar
from src.layers.data.loader import data_loadSinan

def _filter(ano: int, mes: str=None,uf: str=None, xfilters: dict= None, return_df: bool= False): #função filtro base/principal para as outras

    df = limpar(data_loadSinan(ano))
    condition = pd.Series(True, index=df.index)

    if mes: #verifica se existe busca por mes
        condition &= (df["DT_NOTIFIC"].dt.month == mes)
    
    if uf: #verifica se existe busca pela UF
        condition &= (df["SG_UF_NOT"] == uf)
    
    if xfilters: #verifica a existencia de outros filtro (abstração da função para uso com outros parametros)
        for column, value in xfilters.items():
            if column in df.columns:
                condition = condition & (df[column] == value)
    
    df_filtrado = df[condition]

    if return_df:
        return df_filtrado
    
    return df_filtrado.shape[0]

def filter_distrib_idade(ano: int, mes: str=None, uf: str=None): #função para filtrar a distribuição de idades
    dfFiltrado = _filter(ano, mes=mes, uf=uf, return_df=True)

    counter_idade = dfFiltrado["FX_ETARIA"].value_counts().sort_index()

    return counter_idade

def filter_df(ano: int, mes: str=None, uf: str="53"): #função derivada da principal para filtrar somente por UF
    total = _filter(ano, mes=mes, uf=uf)
    return total

def filter_sexo_df(ano: int, sex: str, mes: str=None, uf: str="53"): #função derivada da principal para filtrar sexo na UF
    filtro = {"CS_SEXO": sex}
    total = _filter(ano, mes=mes, uf=uf, xfilters=filtro)
    return total

def filter_sexo(ano: int, sex: str, mes: str=None): #função derivada da principal para filtrar somente por sexo
    filtro = {"CS_SEXO": sex}
    total = _filter(ano, mes=mes, uf=None, xfilters=filtro)
    return total

def filter_idade_df(ano: int, fx_etaria: str, mes: str=None, uf: str="53"): #função derivada da principal para filtrar idade especifica na UF
    filtro = {"FX_ETARIA": fx_etaria}
    total = _filter(ano, mes=mes, uf=uf, xfilters=filtro)
    return total
