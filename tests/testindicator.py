import pandas as pd
from src.layers.data.loader import data_loadSinan
from src.layers.data.filters import _filter
from src.layers.business.indicator import (
    classificar_regiao,
    variacao_mensal,
    regioes_em_alerta,
)

ANO_TESTE = 2025

print("=" * 60)
print(f"INICIANDO TESTE: INDICATOR (ANO {ANO_TESTE})")
print("=" * 60)

data_loadSinan(ANO_TESTE)  # garante que o parquet já está em cache
df = _filter(ANO_TESTE, uf="53", return_df=True)
print(f"\nDataFrame carregado: {len(df)} linhas.\n")

# --- TESTE 1: CLASSIFICAR REGIÃO ---
print("[Teste 1] classificar_regiao...")
classificacao = classificar_regiao(df)
print(classificacao)
assert isinstance(classificacao, pd.Series), "Erro: classificar_regiao deveria retornar uma Series."
assert classificacao.isin(["NORMAL", "ALERTA", "CRÍTICO"]).all(), "Erro: classificações inválidas encontradas."

# --- TESTE 2: VARIAÇÃO MENSAL ---
print("\n[Teste 2] variacao_mensal...")
variacao = variacao_mensal(df)
print(variacao)
assert isinstance(variacao, pd.Series), "Erro: variacao_mensal deveria retornar uma Series."
assert variacao.iloc[0] != variacao.iloc[0], "Erro: primeiro valor deveria ser NaN."

# --- TESTE 3: REGIÕES EM ALERTA ---
print("\n[Teste 3] regioes_em_alerta...")
alerta = regioes_em_alerta(df)
print(alerta)
assert isinstance(alerta, pd.Series), "Erro: regioes_em_alerta deveria retornar uma Series."
assert (alerta >= 1000).all(), "Erro: todas as regiões em alerta devem ter pelo menos 1000 casos."

print("\n" + "=" * 60)
print("TODAS AS FUNÇÕES DO INDICATOR VALIDADAS COM SUCESSO!")
print("=" * 60)