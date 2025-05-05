# stock_screener/transformer.py
'''Responsabilité : nettoyer et agréger les deux DataFrames (valorisation + finances),
calculs additionnels, normalisation des clés, gestion des dates.'''

import pandas as pd

def merge_data(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Concatène verticalement deux DataFrames de ratios.
    """
    df = pd.concat([df1, df2], ignore_index=False)
    df = df.rename(index={'Nbr de Titres (en Milliers)':'Nbr de Titres'})
    df_million = df.loc[[
        "Capitalisation","Valeur Entreprise","Chiffre d'affaires",
        "EBITDA","EBIT","Résultat net","Endettement Net"
        ]]*1E6 #Returns values in unit
    df_shares = df.loc[['Nbr de Titres']]*1E3
    df.loc[df_million.index,:]=df_million[:]
    df.loc[df_shares.index,:]=df_shares[:]
    return df

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renomme les index en snake_case, remplace NaN par 0.
    """
    df = df.copy()
    df.index = [
        idx.lower().strip().replace(" ", "_").replace("%","pct") for idx in df.index
    ]
    return df.fillna(0.0)

