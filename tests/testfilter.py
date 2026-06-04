import pandas as pd

# Importa apenas as funções da sua camada de filtros
from src.layers.data.filters import _filter, filter_cross
from src.layers.business.process import distribuicao_faixa_etaria

# ==============================================================================
# CONFIGURAÇÃO: Defina o ano que você tem baixado na sua máquina
# ==============================================================================
ANO_TESTE = 2024

print("=" * 60)
print(f"INICIANDO TESTE DIRETO: PIPELINE DATASUS (ANO {ANO_TESTE})")
print("=" * 60)

# --- TESTE 1: FUNÇÃO BASE _FILTER (VALIDAÇÃO DO ENGINE DATA + FILTRO) ---
print("\n[Teste 1] Rodando _filter basico (Ano cheio, UF '53')...")
print("   *Isso vai disparar o data_loadSinan e o limpar() automaticamente internamente*")

total_df = _filter(ANO_TESTE, uf="53")

print(f"-> Sucesso! O pipeline rodou e encontrou {total_df} casos validados no DF.")
assert isinstance(total_df, int), "Erro: O retorno de _filter deveria ser um número inteiro."   


# --- TESTE 2: FILTRO TEMPORAL ---
print("\n[Teste 2] Rodando _filter com mes específico (Mes '05' - Maio, UF '53')...")
total_maio = _filter(ANO_TESTE, mes=5, uf="53")

print(f"-> Sucesso! Encontrados {total_maio} casos em Maio no DF.")
assert total_maio <= total_df, "Erro logico: Os casos de Maio nao podem ser maiores que o ano todo."


# --- TESTE 3: CRUZAMENTOS DINÂMICOS (FILTER_CROSS) ---
print("\n" + "-" * 50)
print("[Teste 3] Rodando filter_cross (Cruzamentos multiplos com dados reais):")
print("-" * 50)

# Cruzando Região Sudoeste (6645) + Sexo Feminino (F)
print(">> Buscando Mulheres na Regiao Sudoeste...")
cruzado_regiao_sexo = filter_cross(ANO_TESTE, regiao="6645", sexo="F", uf="53")
print(f"   Resultado: {cruzado_regiao_sexo} casos encontrados.")

# Cruzando Região Oeste (6646) + Faixa Etária (20-39) + Sexo Masculino (M)
print("\n>> Buscando Homens Adultos (20-39 anos) na Regiao Oeste...")
cruzado_tudo = filter_cross(ANO_TESTE, regiao="6646", fx_etaria="20-39", sexo="M", uf="53")
print(f"   Resultado: {cruzado_tudo} casos encontrados.")


# --- TESTE 4: AGREGAÇÃO EM SÉRIES (FILTER_DISTRIB_IDADE) ---
print("\n" + "-" * 50)
print("[Teste 4] Rodando filter_distrib_idade (Agrupamento final para o Matplotlib):")
print("-" * 50)

distribuicao = distribuicao_faixa_etaria(ANO_TESTE, uf="53")

print("-> Sucesso! Série gerada a partir dos dados reais do cleaner:\n")
if not distribuicao.empty:
    print(distribuicao)
    
    # Validação estrutural da Série
    assert isinstance(distribuicao, pd.Series), "Erro: O retorno deveria ser uma Serie do Pandas."
    assert pd.api.types.is_integer_dtype(distribuicao.values), "Erro: Os valores da contagem devem ser inteiros."
else:
    print("   [Aviso] Nenhuma linha correspondente para listar a distribuicao.")

print("-" * 50)
print("\n" + "=" * 60)
print("TODAS AS FUNÇÕES EXECUTADAS E VALIDADAS COM SUCESSO!")
print("Seu ecossistema Loader -> Cleaner -> Filtros esta totalmente funcional")
print("=" * 60)