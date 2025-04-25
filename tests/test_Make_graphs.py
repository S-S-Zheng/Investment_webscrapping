import pandas as pd
from stock_screener.Make_graphs import Plotter

def test_plotter():
    df = pd.DataFrame({"PER":[10,12], "PEG":[0.8,0.9]}, index=[2022,2023])
    plotter = Plotter(df,company_name="SAF")
    fig = plotter.create_charts()
    assert fig.layout.title.text == "Analyse Fondamentale"
    # export HTML
    out = "plot.html"
    plotter.save_graphs(out)
    #assert out.exists()
