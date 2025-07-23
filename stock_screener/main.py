# stock_screener/main.py
'''
THE Main
'''

import datetime as dt
import pandas as pd
import os
import aiohttp
import asyncio

from fetcher     import fetch_meta, fetch_ratios, fetch_calendar
from transformer import merge_data, normalize_dataframe, searching_string, no_division_error,df_add
from exporter    import export_to_excel
#from Make_graphs import Plotter
from Make_graphs_nosubplot import Plotter


# Async process that groups meta, calendar and ratios
async def process_company(session: aiohttp.ClientSession, cid:str):
    meta = await fetch_meta(session, cid)
    df_val = await fetch_ratios(session, cid, "valorisation")
    df_fin = await fetch_ratios(session, cid, "finances-ratios")
    df_merge = merge_data(df_val[0], df_fin[0])
    df_normalize = normalize_dataframe(df_merge)
    df_reindex = df_normalize.reindex(sorted(df_normalize.columns), axis=1)
    df = df_add(df_reindex)
    calendar = await fetch_calendar(session, cid, "agenda")

    current_year=int(dt.date.today().strftime('%Y'))
    dividende = df.loc["Dividende / Action",current_year]
    sheet_name = meta["TAG"]
    company_name = meta["Entreprise"]

    return sheet_name, meta, df, dividende, company_name, calendar

async def main():
    company_identifiers = [
        "SAFRAN-4696/",
        "FERMENTALG-16118042/",
        "MANITOU-GROUP-4773/",
        "NVIDIA-CORPORATION-57355629/",
        "TOTALENERGIES-SE-4717/",
        "BYD-COMPANY-LIMITED-111963805/",
        "ASML-HOLDING-N-V-12002973/",
        "NOVO-NORDISK-A-S-1412980/",
        "LVMH-4669/",
        "OVH-GROUPE-127472031/",
        "TSMC-TAIWAN-SEMICONDUCTOR-6492349/",
        "RHEINMETALL-AG-436527/",
        "SANOFI-4698/",
        "REDDIT-INC-167442757/",
        "AMAZON-COM-INC-12864605/",
        "ORACLE-CORPORATION-13620698/",
        "BAE-SYSTEMS-PLC-444896/",
        "TENCENT-HOLDINGS-LIMITED-16686492/",
        "ALIBABA-GROUP-HOLDING-LIM-17916677/",
        "HIMS-HERS-HEALTH-INC-65220697/",
        "JD-COM-INC-16538052/",
        "SCHNEIDER-ELECTRIC-SE-4699/",
        "SIDETRADE-S-A-3033378/",
        "PUBLICIS-GROUPE-S-A-4685/",
        "WAVESTONE-45568714/",
        "GEELY-AUTOMOBILE-HOLDINGS-6165704/",
        "NEWBORN-TOWN-INC-103501720/",
        "T-L-CO-LTD-120976556/",
        "LH-HOTEL-LEASEHOLD-REAL-E-31763173/",
        "PDD-HOLDINGS-INC-45049866/",
        "ACM-RESEARCH-INC-38533881/"
    ]
    summary_rows = []
    detail_dfs    = {}

    async with aiohttp.ClientSession() as session:
        tasks = [process_company(session, cid) for cid in company_identifiers]
        # gather permet de lancer toutes les tâches de scrapping en coroutine
        for sheet_name, meta, df, dividende, company_name, calendar in await asyncio.gather(*tasks):
            summary_rows.append({
                **meta,
                "Dividende par action": dividende,
                **calendar
            })
            detail_dfs[sheet_name] = df

            # Charts
            #Une fois les df recupérées, on execute synchroniquement les I/O plot-Excel
            plotter = Plotter(df,company_name)
            fig = plotter.create_charts()
            #os.makedirs("graphs", exist_ok=True)
            os.makedirs("html", exist_ok=True)
            plotter.save_graphs(f"{company_name}.html")

    unsorted_summary_df = pd.DataFrame(summary_rows)

    # Reorganize the events form year and quarters using searching_string
    fixed_df = unsorted_summary_df.columns[:len(meta)+1]
    sorted_df = sorted(unsorted_summary_df.columns[len(meta)+1:], key=searching_string)
    summary_df = unsorted_summary_df[list(fixed_df) + list(sorted_df)]

    export_to_excel(summary_df, detail_dfs, "donnees_financieres.xlsx")

if __name__ == "__main__":
    asyncio.run(main())
