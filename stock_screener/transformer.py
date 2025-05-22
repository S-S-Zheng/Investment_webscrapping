# stock_screener/transformer.py
'''
Module used to regroup functions that'll reshape datas:
Clean, merge and normalize the dataframes.
String matcher using regex
'''

import pandas as pd
import re

def merge_data(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Concat vertically 2 df.
    """
    df = pd.concat([df1, df2], ignore_index=False)
    return df

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Correct indexes and values in df.
    """
    df = df.rename(index={'Nbr de Titres (en Milliers)':'Nbr de Titres',
                        'Variation': 'Variation %', 'FCF Yield':'FCF Yield %',
                        'Taux de rendement':'Taux de rendement %',
                        'Taux de distribution':'Taux de distribution %'
                        })
    df_million = df.loc[[
        "Capitalisation","Valeur Entreprise","Chiffre d'affaires",
        "EBITDA","EBIT","Résultat net","Endettement Net"
        ]]*1000000 #Returns values in unit
    df_shares = df.loc[['Nbr de Titres']]*1000
    df.loc[df_million.index,:]=df_million[:]
    df.loc[df_shares.index,:]=df_shares[:]

    return df


def searching_string(string_to_evaluate:str):
    '''
    Look for a matching string, in this case a string structure resembling to Q(1-2-3 or 4),a space
    followed by 4 numbers and will return the quarter and year
    '''
    match = re.match(r'Q([1-4])\s(\d{4})', string_to_evaluate)
    if match:
        quarter = int(match.group(1))
        year = int(match.group(2))
        return (year, quarter)
    return (0, 0) # default values if format issues

def no_division_error(func)->float:
    try:
        return func()
    except (ZeroDivisionError, TypeError, KeyError):
        return ''

def df_add(df:pd.DataFrame) ->pd.DataFrame:
    df.loc["FCF"]=no_division_error(lambda:df.loc["Valeur Entreprise"]/df.loc["Valeur Entreprise / FCF"])
    df.loc["PCF"]=no_division_error(lambda:df.loc["Cours de référence"]/df.loc["FCF"])
    df.loc["Taux imposition (approximé)"]=no_division_error(lambda:1-(df.loc["Résultat net"]/df.loc["EBIT"]))
    df.loc["Rentabilité sur le capital investi (ROIC approximé)"]= no_division_error(lambda:(1-df.loc["Taux imposition (approximé)"])/df.loc["Valeur Entreprise / EBIT"])
    return df