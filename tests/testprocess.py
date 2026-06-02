import pandas as pd

from src.layers.data.filters import _filter
from src.layers.business.process import (
    casos_por_regiao,
    serie_temporal,
    distribuicao_sexo,
    distribuicao_faixa_etaria,
    regiao_com_mais_casos,
    total_casos,
)

ANO_TESTE = 2025

print("=" * 60)
print(f"INICIANDO TESTE: PROCESS (ANO {ANO_TESTE})")
print("=" * 60)

df = _filter(ANO_TESTE, uf="53", return_df=True)
print(f"\nDataFrame carregado: {len(df)} linhas.\n")

# --- TESTE 1: TOTAL DE CASOS ---
print("[Teste 1] total_casos...")
total = total_casos(df)
print(f"-> {total} casos no total.")
assert isinstance(total, int), "Erro: total_casos deveria retornar int."
assert total == len(df), "Erro: total_casos deveria ser igual ao número de linhas do DataFrame."

# --- TESTE 2: CASOS POR REGIÃO ---
print("\n[Teste 2] casos_por_regiao...")
por_regiao = casos_por_regiao(df)
print(por_regiao)
assert isinstance(por_regiao, pd.Series), "Erro: casos_por_regiao deveria retornar uma Series."
assert por_regiao.is_monotonic_decreasing, "Erro: resultado deveria estar em ordem decrescente."

# --- TESTE 3: SÉRIE TEMPORAL ---
print("\n[Teste 3] serie_temporal...")
temporal = serie_temporal(df)
print(temporal)
assert isinstance(temporal, pd.Series), "Erro: serie_temporal deveria retornar uma Series."
assert len(temporal) > 0, "Erro: serie_temporal não deveria estar vazia."

# --- TESTE 4: DISTRIBUIÇÃO POR SEXO ---
print("\n[Teste 4] distribuicao_sexo...")
sexo = distribuicao_sexo(df)
print(sexo)
assert isinstance(sexo, pd.Series), "Erro: distribuicao_sexo deveria retornar uma Series."
assert sexo.sum().round() == 100, "Erro: as porcentagens deveriam somar 100%."

# --- TESTE 5: DISTRIBUIÇÃO POR FAIXA ETÁRIA ---
print("\n[Teste 5] distribuicao_faixa_etaria...")
faixa = distribuicao_faixa_etaria(df)
print(faixa)
assert isinstance(faixa, pd.Series), "Erro: distribuicao_faixa_etaria deveria retornar uma Series."
assert len(faixa) > 0, "Erro: distribuicao_faixa_etaria não deveria estar vazia."

# --- TESTE 6: REGIÃO COM MAIS CASOS ---
print("\n[Teste 6] regiao_com_mais_casos...")
regiao_lider = regiao_com_mais_casos(df)
print(f"-> Região com mais casos: {regiao_lider}")
assert isinstance(regiao_lider, str), "Erro: regiao_com_mais_casos deveria retornar uma string."
assert regiao_lider in por_regiao.index, "Erro: região retornada não está no índice de casos_por_regiao."

print("\n" + "=" * 60)
print("TODAS AS FUNÇÕES DO PROCESS VALIDADAS COM SUCESSO!")
print("=" * 60)