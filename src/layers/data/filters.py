import pandas as pd
from src.layers.data.cleaner import limpar
from src.layers.data.loader import data_loadSinan

def _filter(ano: int, mes: int=None,uf: str=None, xfilters: dict= None, return_df: bool= False): #função filtro base/principal para as outras

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

def filter_distrib_idade(ano: int, mes: int=None, uf: str=None): #função para filtrar a distribuição de idades
    dfFiltrado = _filter(ano, mes=mes, uf=uf, return_df=True)

    counter_idade = dfFiltrado["FX_ETARIA"].value_counts().sort_index()

    return counter_idade

def filter_df(ano: int, mes: int=None, uf: str="53"): #função derivada da principal para filtrar somente por UF(DF)
    total = _filter(ano, mes=mes, uf=uf)
    return total

def filter_sexo(ano: int, sex: str, mes: int=None, uf: str=None): #função derivada da principal para filtrar sexo no DF
    filtro = {"CS_SEXO": sex}
    total = _filter(ano, mes=mes, uf=uf, xfilters=filtro)
    return total

def filter_idade(ano: int, fx_etaria: str, mes: int=None, uf: str=None): #função derivada da principal para filtrar idade especifica no DF
    filtro = {"FX_ETARIA": fx_etaria}
    total = _filter(ano, mes=mes, uf=uf, xfilters=filtro)
    return total

def filter_regiao_df(ano: int, regiao: str, mes: int=None, uf: str="53"): # função derivada para filtrar regiao generica do DF
    filtro = {"ID_REGIONA": regiao}
    total = _filter(ano, mes=mes, uf=uf, xfilters=filtro)
    return total

#Funções cruzadas:

def filter_cross(ano: int, regiao: str=None, fx_etaria: str =None,sexo: str=None, mes: int=None, uf: str=None): #filtro para casos de multiplos parametros
    filtros = {}
    if regiao:
        filtros["ID_REGIONA"] = regiao
    if fx_etaria:
        filtros["FX_ETARIA"] = fx_etaria
    if sexo:
        filtros["CS_SEXO"] = sexo
    
    xfilters_ready = filtros if filtros else None #verificação da existencia de filtros para prevenção de erros
    
    total = _filter(ano, mes=mes, uf=uf, xfilters=xfilters_ready)
    return total
