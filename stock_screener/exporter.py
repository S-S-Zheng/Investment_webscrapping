# stock_screener/exporter.py
'''Responsabilité : écriture du fichier Excel (openpyxl), sommaire,
onglets par entreprise, mise en forme conditionnelle, ajustement de largeur.'''

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import CellIsRule

def auto_adjust_columns(ws):
    for col in ws.columns:
        max_len = max(len(str(cell.value)) for cell in col if cell.value)
        ws.column_dimensions[col[0].column_letter].width = max_len + 2

'''
def apply_conditional_formatting(ws):
    red = PatternFill("solid", fgColor="FFC7CE")
    green = PatternFill("solid", fgColor="C6EFCE")
    # format >1 en rouge, ≤1 en vert
    ws.conditional_formatting.add(
        f"B2:{ws.max_column}{ws.max_row}",
        CellIsRule(operator="greaterThan", formula=["1"], fill=red)
    )
    ws.conditional_formatting.add(
        f"B2:{ws.max_column}{ws.max_row}",
        CellIsRule(operator="lessThanOrEqual", formula=["1"], fill=green)
    )
'''
def export_to_excel(summary: pd.DataFrame, details: dict, filename: str):
    """
    summary : DataFrame pour l'onglet 'Sommaire'
    details : {sheet_name: DataFrame_ratios}
    """
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Sommaire", index=False)
        for name, df in details.items():
            df.to_excel(writer, sheet_name=name[:31])
    wb = load_workbook(filename)
    for ws in wb.worksheets:
        auto_adjust_columns(ws)
        #apply_conditional_formatting(ws)
    wb.save(filename)
