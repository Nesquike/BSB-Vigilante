import pandas as pd
from process import (
    casos_por_regiao,
    serie_temporal
)

def classificar_regiao(df: pd.DataFrame) -> pd.Series:
    # Atribui à variável "casos" os valores pd.Series retornados da função casos_por_regiao()
    casos = casos_por_regiao(df) 
    
    # Sub-função privada para fazer a comparação do número de casos para atribuir uma classificação à região
    def _classificar(n): 
        if n >= 5000: return "CRÍTICO"
        if n >= 1000: return "ALERTA"
        return "NORMAL"

    # Percorre cada valor da Series e aplica a função _classificar()
    # Retorna uma nova Series com os resultados classificados
    return casos.apply(_classificar) 

def variacao_mensal(df: pd.DataFrame) -> pd.Series:
    # Pega cada valor da pd.Series e retorna o cálculo de quanto variou em relação ao valor anterior
    # O primeiro valor sempre terá um resultado NaN
    return serie_temporal(df).pct_change() * 100
    
    
def regioes_em_alerta(df: pd.DataFrame, limite : int = 1000) -> pd.Series:
    # Varredura única do DataFrame. Agrupa por região e mês
    casos_mensais = df.groupby(["ID_REGIONA", df["DT_NOTIFIC"].dt.to_period("M")]).size()
    
    # Calcula o total de casos reaproveitando a variável casos_mensais (soma os meses de cada região)
    casos_totais = casos_mensais.groupby(level=0).sum().sort_values(ascending=False)
    
    # Calcula a variação percentual do último mês
    tendencia = casos_mensais.groupby(level=0).pct_change().groupby(level=0).last()
    
    # Aplica a máscara booleana e retorna as regiões em alerta
    return casos_totais[(casos_totais >= limite) & (tendencia > 0)]