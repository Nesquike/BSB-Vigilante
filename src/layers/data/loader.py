import os
import pandas as pd
from pysus import sinan

processed_data = os.path.join("data", "processed")


def data_loadSinan(ano: int) -> pd.DataFrame:
    os.makedirs(processed_data, exist_ok=True)

    filename = f"sinan_Dengue_{ano}.parquet"
    filepath = os.path.join(processed_data, filename)

    # cache
    if os.path.exists(filepath):
        return pd.read_parquet(filepath)

    try:
        # download
        dfFull = sinan(disease="DENG", year=ano)

        # validação
        if dfFull is None or dfFull.empty:
            print("Nenhum dado encontrado para este período.")
            return pd.DataFrame()

        # salvar
        dfFull.to_parquet(filepath, index=False)

        return dfFull

    except Exception as e:
        print("Erro ao buscar ou salvar os dados do SINAN:", e)
        return pd.DataFrame()