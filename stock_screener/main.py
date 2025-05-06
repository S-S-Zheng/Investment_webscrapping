# stock_screener/main.py
'''Responsabilité : orchestration – appeler fetcher, transformer, exporter, plotter.'''

import datetime as dt
import pandas as pd
import os
import aiohttp
import asyncio

from fetcher     import fetch_meta, fetch_ratios
from transformer import merge_data, normalize_dataframe
from exporter    import export_to_excel
from Make_graphs import Plotter


# Coroutine qui regroupe meta et ratios
async def process_company(session, cid):
    meta = await fetch_meta(session, cid)
    df_val = await fetch_ratios(session, cid, "valorisation")
    df_fin = await fetch_ratios(session, cid, "finances-ratios")
    df_merge = merge_data(df_val[0], df_fin[0])
    df_normalize = normalize_dataframe(df_merge)
    df = df_normalize.reindex(sorted(df_normalize.columns), axis=1)

    # Extrait le dividende de l'année courante ou 0
    current_year=int(dt.date.today().strftime('%Y'))
    dividende = df.loc["Dividende / Action",current_year]

    sheet_name = meta["TAG"]
    company_name = meta["Entreprise"]
    publication = df.loc["Date de publication", current_year]
    return sheet_name, meta, df, dividende, company_name, publication

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
        "BNP-PARIBAS-4618/",
        "AIR-LIQUIDE-4605/",
        "SAINT-GOBAIN-4697/",
        "TSMC-TAIWAN-SEMICONDUCTOR-6492349/",
        "RHEINMETALL-AG-436527/",
        "SANOFI-4698/",
        "MEDPACE-HOLDINGS-INC-30506552/",
        "REDDIT-INC-167442757/",
        "AMAZON-COM-INC-12864605/",
        "ORACLE-CORPORATION-13620698/",
        "BAE-SYSTEMS-PLC-444896/",
        "TENCENT-HOLDINGS-LIMITED-16686492/",
        "ALIBABA-GROUP-HOLDING-LIM-17916677/",
        "HIMS-HERS-HEALTH-INC-65220697/"
    ]
    summary_rows = []
    detail_dfs    = {}

    async with aiohttp.ClientSession() as session:
        tasks = [process_company(session, cid) for cid in company_identifiers]
        # gather permet de lancer toutes les tâches de scrapping en coroutine
        for sheet_name, meta, df, dividende, company_name, publication in await asyncio.gather(*tasks):
            summary_rows.append({
                **meta,
                "Dividende par action": dividende,
                "Date de publication": publication
            })
            detail_dfs[sheet_name] = df

            # Graphiques
            #Une fois les df recupérées, on execute synchroniquement les I/O plot-Excel
            plotter = Plotter(df,company_name)
            fig = plotter.create_charts()
            os.makedirs("graphs", exist_ok=True)
            os.makedirs("html", exist_ok=True)
            plotter.save_graphs(f"{company_name}.html")

    summary_df = pd.DataFrame(summary_rows)
    export_to_excel(summary_df, detail_dfs, "donnees_financieres.xlsx")

if __name__ == "__main__":
    asyncio.run(main())


    '''
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
    '''
