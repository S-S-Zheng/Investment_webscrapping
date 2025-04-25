import pandas as pd
from stock_screener.transformer import merge_data, normalize_dataframe

def test_merge_and_normalize():
    df1 = pd.DataFrame({"A":[1], "B":[2]}, index=[2022]).T
    df2 = pd.DataFrame({"C":[3]}, index=[2023]).T
    df_merged = merge_data(df1, df2)
    assert set(df_merged.index) == {"A","B","C"}

    df_norm = normalize_dataframe(df_merged)
    assert "a" in df_norm.index  # renommage en snake_case
    assert df_norm.fillna(0).isnull().sum().sum() == 0
