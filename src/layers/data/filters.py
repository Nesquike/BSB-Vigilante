import pandas as pd
from src.layers.data.loader import data_loadSinan

def filter(ano: int, mes: str):
    df = data_loadSinan(ano)

    statecolumn_search = "SG_UF_NOT"
    statedata_search = "53"
    monthcolumn_search = "DT_NOTIFIC"
    monthdata_search = f"{ano}{mes}"



    rowcounter = df[
        (df[statecolumn_search] == statedata_search) & (df[monthcolumn_search].astype(str).str.contains(monthdata_search, na=False))
        ].shape[0]

    print(f"linhas encontradas: {rowcounter}")


