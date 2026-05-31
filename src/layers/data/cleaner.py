import pandas as pd

RA_VALIDAS = {
    "ÁGUAS CLARAS", "ASA NORTE", "ASA SUL", "BRAZLÂNDIA", "CANDANGOLÂNDIA", 
    "CEILÂNDIA", "CRUZEIRO", "FERCAL", "GAMA", "GUARÁ", "LAGO NORTE", 
    "LAGO SUL", "NÚCLEO BANDEIRANTE", "PARANOÁ", "PARK WAY", "PLANALTINA", 
    "RECANTO DAS EMAS", "RIACHO FUNDO", "SAMAMBAIA", "SANTA MARIA", 
    "SÃO SEBASTIÃO", "SCIA", "SIA", "SOBRADINHO", "SUDOESTE/OCTOGONAL", 
    "TAGUATINGA", "VARJÃO", "VICENTE PIRES"
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
    df = _validar_num_casos(df)
    df = _validar_dados(df)
    
    # Reseta o index do DataFrame para integers sequenciais, prevenindo index antigos de virarem uma nova coluna
    # Retorna o DataFrame limpo
    return df.reset_index(drop=True)
    
# Funções internas:

def _remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates() # Retorna o DataFrame sem linhas duplicadas

def _tratar_datas(df: pd.DataFrame) -> pd.DataFrame:
    df["data_notificacao"] = pd.to_datetime(
        df["data_notificacao"], errors="coerce"
    ) # Converte os valores de data_notificacao para objetos datetime do Pandas. Dados inválidos serão convertidos para NaT
    
    invalidas = df["data_notificacao"].isna().sum() # Conta a quantidade total de valores nulos na coluna data_notificacao
    if invalidas:
        print(f"[cleaner] {invalidas} linha(s) removida(s) por data inválida.") # Imprime a quantidade de linhas inválidas removidas caso existam
    return df.dropna(subset="data_notificacao") # Retorna o DataFrame limpo de data_notificacao inválida
    
def _normalizar_strings(df: pd.DataFrame) -> pd.DataFrame:
    # Converte a coluna regiao_administrativa, remove espaços e converte todas as letras para maiúsculas
    df["regiao_administrativa"] = df["regiao_administrativa"].astype(str).str.strip().str.upper()
    df["sexo"] = df["sexo"].astype(str).str.strip().str.upper() # Converte a coluna sexo para string, remove espaços e converte todas as letras para maiúsculas
    df["faixa_etaria"] = df["faixa_etaria"].astype(str).str.strip() # Converte a coluna faixa_etaria para string e remove espaços
    return df # Retorna o DataFrame com strings normalizadas

def _remover_campos_vazios(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df) # Atribui à variável "antes" a quantidade total de linhas do DataFrame
    df = df.dropna(subset=["regiao_administrativa", "num_casos", "sexo", "faixa_etaria"]) # Remove os campos nulos das colunas do DataFrame
    removidas = antes - len(df) # Subtrai a quantidade anterior de linhas pelo DataFrame limpo para encontrar a quantidade total de itens removidos
    if removidas:
        print(f"[cleaner] {removidas} linha(s) removida(s) por campos vazios.") # Imprime a quantidade de linhas removidas por terem campos nulos
    return df # Retorna o DataFrame sem campos nulos

def _validar_num_casos(df: pd.DataFrame) -> pd.DataFrame:
    df["num_casos"] = pd.to_numeric(df["num_casos"], errors="coerce") # Converte os valores de num_casos para um dado numérico. Em caso do valor que não puder ser convertido para número, converte para NaN
    invalidos = df["num_casos"].isna() | (df["num_casos"] < 0) # Atribui à variável invalidos todos os valores que forem nulos ou menores que zero
    if invalidos.sum():
        print(f"[cleaner] {invalidos.sum()} linha(s) removida(s) de num_casos inválidos.") # Imprime a quantidade total de valores inválidos encontrados na coluna num_casos
    df_valido = df[~invalidos].copy() # Remove todos os NaN do DataFrame. O método .copy() garante que a alteração ocorra em um DataFrame independente, ao invés de uma fatia do original
    df_valido["num_casos"] = df_valido["num_casos"].astype(int) # Converte a coluna num_casos do DataFrame para int
    return df_valido

def _validar_dados(df: pd.DataFrame) -> pd.DataFrame:
    ra = df["regiao_administrativa"].isin(RA_VALIDAS) # Verifica se os valores da coluna regiao_administrativa estão no set RA_VALIDAS
    sexo = df["sexo"].isin(SEXOS_VALIDOS) # Verifica se os valores da coluna sexo estão no set SEXOS_VALIDOS
    fe = df["faixa_etaria"].isin(FE_VALIDAS) # Verifica se os valores da coluna faixa_etaria estão no set FE_VALIDAS
    
    # Caso algum valor desconhecido seja encontrado, imprime:
    if(~ra).sum():
        print(f"[cleaner]: {(~ra).sum()} linha(s) com RA desconhecida(s): {df.loc[~ra, "regiao_administrativa"].unique()}") # A quantidade de valores desconhecidos na coluna regiao_administrativa
    if(~sexo).sum():
        print(f"[cleaner]: {(~sexo).sum()} linha(s) com sexo inválido.") # A quantidade de valores desconhecidos na coluna sexo
    if(~fe).sum():
        print(f"[cleaner]: {(~fe).sum()} linha(s) com faixa etária inválida.") # A quantidade de valores desconhecidos na coluna faixa_etaria
        
    return df[ra & sexo & fe] # Retorna o DataFrame apenas com os valores que foram validados