import pandas as pd
import numpy as np

REGIAO_VALIDAS = {
    "6642": "Central (Plano Piloto/Lagoa/Sudoeste)",
    "6643": "Centro-Sul (Guará/Bandeirante/Riacho)",
    "6644": "Norte (Planaltina/Sobradinho)",
    "6645": "Sudoeste (Taguatinga/Samambaia/Aguas Claras)",
    "6646": "Oeste (Ceilândia/Brazlândia)",
    "6647": "Sul (Gama/Santa Maria)",
    "6648": "Leste (Paranoá/São Sebastião/Itapoã)"
}

SEXOS_VALIDOS = {"M", "F", "I"}

FE_VALIDAS = {
    "0-9", "10-19", "20-39", "40-59", "60-79", "80+"
}  

# Função pública

def limpar(df: pd.DataFrame) -> pd.DataFrame:
    # Chama as funções privadas para limpar o DataFrame
    df = df.copy() # O método .copy() garante que as alterações ocorram em um DataFrame independente, ao invés de uma fatia do original
    df = _remover_duplicatas(df)
    df = _tratar_datas(df)
    df = _normalizar_strings(df)
    df = _remover_campos_vazios(df)
    df = _validar_dados(df)
    df = _calcular_faixa_etaria(df)
    
    # Reseta o index do DataFrame para integers sequenciais, prevenindo index antigos de virarem uma nova coluna
    # Retorna o DataFrame limpo
    return df.reset_index(drop=True)
    
# Funções internas:

def _remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates() # Retorna o DataFrame sem linhas duplicadas

def _tratar_datas(df: pd.DataFrame) -> pd.DataFrame:
    df["DT_NOTIFIC"] = pd.to_datetime(
        df["DT_NOTIFIC"], errors="coerce"
    ) # Converte os valores de DT_NOTIFIC para objetos datetime do Pandas. Dados inválidos serão convertidos para NaT
    
    invalidas = df["DT_NOTIFIC"].isna().sum() # Conta a quantidade total de valores nulos na coluna data_notificacao
    if invalidas:
        print(f"[cleaner] {invalidas} linha(s) removida(s) por data inválida.") # Imprime a quantidade de linhas inválidas removidas caso existam
    return df.dropna(subset="DT_NOTIFIC") # Retorna o DataFrame limpo de data_notificacao inválida
    
def _normalizar_strings(df: pd.DataFrame) -> pd.DataFrame:
    # Converte a coluna ID_REGIONA, remove espaços e converte todas as letras para maiúsculas
    df["ID_REGIONA"] = df["ID_REGIONA"].astype(str).str.split('.').str.strip().str.upper()
    df["CS_SEXO"] = df["CS_SEXO"].astype(str).str.strip().str.upper() # Converte a coluna CS_SEXO para string, remove espaços e converte todas as letras para maiúsculas
    df["NU_IDADE_N"] = df["NU_IDADE_N"].astype(str).str.strip() # Converte a coluna NU_IDADE_N para string e remove espaços
    return df # Retorna o DataFrame com strings normalizadas

def _remover_campos_vazios(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df) # Atribui à variável "antes" a quantidade total de linhas do DataFrame
    df = df.dropna(subset=["ID_REGIONA", "CS_SEXO", "NU_IDADE_N"]) # Remove os campos nulos das colunas do DataFrame
    removidas = antes - len(df) # Subtrai a quantidade anterior de linhas pelo DataFrame limpo para encontrar a quantidade total de itens removidos
    if removidas:
        print(f"[cleaner] {removidas} linha(s) removida(s) por campos vazios.") # Imprime a quantidade de linhas removidas por terem campos nulos
    return df # Retorna o DataFrame sem campos nulos

def _calcular_faixa_etaria(df: pd.DataFrame) -> pd.DataFrame:
    # Converte para int temporariamente para fazer a matemática do DATASUS
    idades_brutas = pd.to_numeric(df["NU_IDADE_N"], errors='coerce').fillna(0).astype(int)
    
    # Considerando apenas dados possiveis de idade, de 0 anos de idade a 120
    idade_anos = np.where((idades_brutas >= 4000) & (idades_brutas <= 4120), idades_brutas - 4000, 0)
    
    # Agrupa nas faixas definidas em FE_VALIDAS
    df["FX_ETARIA"] = pd.cut(
        idade_anos,
        bins=[0, 10, 20, 40, 60, 80, np.inf],
        labels=["0-9", "10-19", "20-39", "40-59", "60-79", "80+"],
        right=False
    ).astype(str)
    
    return df


def _validar_dados(df: pd.DataFrame) -> pd.DataFrame:
    ra = df["ID_REGIONA"].isin(REGIAO_VALIDAS) # Verifica se os valores da coluna ID_REGIONA estão no set RA_VALIDAS
    sexo = df["CS_SEXO"].isin(SEXOS_VALIDOS) # Verifica se os valores da coluna sexo estão no set SEXOS_VALIDOS
    fe = df["NU_IDADE_N"].isin(FE_VALIDAS) # Verifica se os valores da coluna faixa_etaria estão no set FE_VALIDAS
    
    # Caso algum valor desconhecido seja encontrado, imprime:
    if(~ra).sum():
        print(f"[cleaner]: {(~ra).sum()} linha(s) com RA desconhecida(s): {df.loc[~ra, "ID_REGIONA"].unique()}") # A quantidade de valores desconhecidos na coluna ID_REGIONA
    if(~sexo).sum():
        print(f"[cleaner]: {(~sexo).sum()} linha(s) com sexo inválido.") # A quantidade de valores desconhecidos na coluna sexo
    if(~fe).sum():
        print(f"[cleaner]: {(~fe).sum()} linha(s) com faixa etária inválida.") # A quantidade de valores desconhecidos na coluna faixa_etaria
        
    return df[ra & sexo & fe] # Retorna o DataFrame apenas com os valores que foram validados