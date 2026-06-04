import pandas as pd
import streamlit as st
from src.layers.data.cleaner import limpar
from src.layers.data.loader import data_loadSinan

@st.cache_resource(show_spinner="Processando base de dados do SINAN...")
def carregar_e_limpar_ano(ano: int) -> pd.DataFrame:
    """
    Carrega do parquet (ou baixa) e aplica a limpeza apenas uma vez por ano.
    O Streamlit guardará o resultado final limpo direto na memória RAM.
    """
    return limpar(data_loadSinan(ano))

def _filter(ano: int, mes: int=None,uf: str=None, xfilters: dict= None, return_df: bool= False): #função filtro base/principal para as outras

    df = carregar_e_limpar_ano(ano)
    
    if df.empty:
        return df
    
    condition = pd.Series(True, index=df.index)

    condition &= (df["DT_NOTIFIC"].dt.year == ano)

    if mes: #verifica se existe busca por mes
        condition &= (df["DT_NOTIFIC"].dt.month == mes)
    
    if uf: #verifica se existe busca pela UF
        condition &= (df["SG_UF_NOT"] == uf)
    
    if xfilters: #verifica a existencia de outros filtro (abstração da função para uso com outros parametros)
        for column, value in xfilters.items():
            if column in df.columns:
                condition = condition & (df[column] == value)
    
    df_filtrado = df[condition]

    
    return df_filtrado


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
