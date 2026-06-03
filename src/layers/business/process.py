import pandas as pd

def casos_por_regiao(df: pd.DataFrame) -> pd.Series: # Gráfico de barras
    # Ranking de RA's
    return df.groupby("ID_REGIONA").size().sort_values(ascending=False)
    # Retorna o número de ocorrências da coluna ID_REGIONA com os dados organizados em ordem decrescente (maior para o menor)
    
def serie_temporal(df: pd.DataFrame) -> pd.Series: # Gráfico de linhas
    # Calcula a frequência de notificações por mês
    return df.groupby(df["DT_NOTIFIC"].dt.to_period("M")).size()
    # Agrupa todas as linhas do DataFrame que pertencem ao mesmo mês e retorna a quantidade de linhas (eventos) dentro de cada grupo mensal
    # OBS: Não confundir o "M" com um dos valores válidos da coluna "CS_SEXO". Na função .to_period(), "M" agrupa as datas por mês.
    
def distribuicao_sexo(df: pd.DataFrame) -> pd.Series: # Gráfico de pizza
    # Calcula a frequência total de cada categoria na coluna "CS_SEXO"
    return df["CS_SEXO"].value_counts(normalize=True) * 100 
    # Retorna uma tabela com porcentagem total de registros para cada categoria na coluna "CS_SEXO"
    
def distribuicao_faixa_etaria(df: pd.DataFrame) -> pd.Series: # Gráfico de barras
    # Calcula a frequência total de cada categoria na coluna "FX_ETARIA"
    return df["FX_ETARIA"].value_counts().sort_index()
    # Retorna uma tabela com quantidade total de casos por FX_ETARIA e organiza os indíces (FX_ETARIA) em ordem crescente
    
def regiao_com_mais_casos(df: pd.DataFrame) -> str:
    # Devolve só o nome da RA com mais notificações de dengue
    return casos_por_regiao(df).idxmax()

def total_casos(df: pd.DataFrame) -> int:
    # Retorna um número simples que pode ser exibido no topo de qualquer painel
    return len(df)