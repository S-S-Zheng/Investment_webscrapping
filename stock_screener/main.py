# stock_screener/main.py
'''Responsabilité : orchestration – appeler fetcher, transformer, exporter, plotter.'''

import datetime as dt
import pandas as pd
import os

from fetcher     import fetch_meta, fetch_ratios
from transformer import merge_data, normalize_dataframe
from exporter    import export_to_excel
from Make_graphs import Plotter


def main():
    company_identifiers = [
        "SAFRAN-4696/",
        "FERMENTALG-16118042/",
        "MANITOU-GROUP-4773/",
        "NVIDIA-CORPORATION-57355629/",
        #"TOTALENERGIES-SE-4717/",
        #"BYD-COMPANY-LIMITED-5640763/",
        #"ASML-HOLDING-N-V-12002973/",
        #"NOVO-NORDISK-A-S-1412980/",
        #"LVMH-4669/"
        #"OVH-GROUPE-127472031/"
        #"BNP-PARIBAS-4618/",
        #"AIR-LIQUIDE-4605/",
        #"SAINT-GOBAIN-4697/",
        #"TSMC-TAIWAN-SEMICONDUCTOR-6492349/",
        #"RHEINMETALL-AG-436527/",
        #"SANOFI-4698/",
        #"MEDPACE-HOLDINGS-INC-30506552/"
    ]
    summary_rows = []
    detail_dfs    = {}
    current_year=int(dt.date.today().strftime('%Y'))

    for cid in company_identifiers:
        meta = fetch_meta(cid)
        df_val = fetch_ratios(cid, "valorisation")
        df_fin = fetch_ratios(cid, "finances-ratios")
        df = merge_data(df_val[0], df_fin[0])
        df.columns = df_val[1]
        #df = normalize_dataframe(df.T)

        summary_rows.append({
            **meta,
            "Dividende par action": df.loc["Dividende / Action",current_year]
        })
        sheet_name = meta["TAG"][:31]
        detail_dfs[sheet_name] = df

        # Graphiques
        plotter = Plotter(df,sheet_name)
        fig = plotter.create_charts()
        os.makedirs("graphs", exist_ok=True)
        os.makedirs("html", exist_ok=True)
        plotter.save_graphs(f"{sheet_name}.html")

    summary_df = pd.DataFrame(summary_rows)
    export_to_excel(summary_df, detail_dfs, "donnees_financieres.xlsx")

if __name__ == "__main__":
    main()
