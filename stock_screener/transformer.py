# stock_screener/transformer.py
'''Responsabilité : nettoyer et agréger les deux DataFrames (valorisation + finances),
calculs additionnels, normalisation des clés, gestion des dates.'''

import pandas as pd

def merge_data(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Concatène verticalement deux DataFrames de ratios.
    """
    return pd.concat([df1, df2], ignore_index=False)

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renomme les index en snake_case, remplace NaN par 0.
    """
    df = df.copy()
    df.index = [
        idx.lower().strip().replace(" ", "_").replace("%","pct") for idx in df.index
    ]
    return df.fillna(0.0)

