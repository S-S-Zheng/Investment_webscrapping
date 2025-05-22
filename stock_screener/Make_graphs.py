# stock_screener/Make_Graphs.py
'''
Class type Plotter that'll use plotly in order to create html and png files
'''
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class Plotter:
    def __init__(self, df:pd.DataFrame, company_name:list):
        """
        Initialise la figure avec 4 sous-graphiques pour visualiser :
        - Valorisation (PER, PEG)
        - Création de valeur (ROE, ROA, ROTC)
        - Solidité financière & cash réel (Rendement FCF, Dette/CP, (EBITDA-CAPEX)/Interêts)
        - Croissance durable (CAGR 3-5 ans sur CA, Bénéfice net, FCF)
        """
        self.df = df #Stockage de la dataframe
        self.company = company_name.split('/')[0]
        self.rows = 2
        self.cols = 2
        self.vertical_spacing = 0.1
        self.horizontal_spacing = 0.1

        self.subplot_height = (1 - (self.rows - 1) * self.vertical_spacing) / self.rows
        self.subplot_width = (1 - (self.cols - 1) * self.horizontal_spacing) / self.cols

        #Crée la figure principale avec Plotly, pouvant contenir plusieurs sous-graphes.
        self.fig = make_subplots(
            rows=self.rows, cols=self.cols,
            subplot_titles=(
                "Valorisation PER | PEG",
                f"Création de valeur ROA|ROE | ROTC",
                f"Solidité financière et cash réel FCF | Dette/CP | EBITDA/Charges",
                f"Croissance durable CAGR 2-5 ans CA | Bénéf | FCF"
            ),
            vertical_spacing=self.vertical_spacing,
            horizontal_spacing=self.horizontal_spacing,
        )
        #Applique la mise en page générale : taille, couleur de fond, polices, légende, marges, etc.
        self.fig.update_layout(
            autosize = True,
            title_text=f"Analyse Fondamentale - {self.company}",
            title_font=dict(size=22),
            title_x = 0.5,
            font=dict(family="Arial", size=14, color="black"),
            #showlegend=True,
            plot_bgcolor="white",
            #legend=dict(x=1, y=1),
            bargap = 0.3,
            bargroupgap = 0.1
        )


    def _add_traces(self, ratios:list, row:int, col:int, num:int):
        x = self.df.columns
        legend_name = f'legend{num}'
        x_leg = ((col - 1) * (self.subplot_width + self.horizontal_spacing)) + (self.subplot_width/1.25)
        y_leg = 1 - ((row - 1) * (self.subplot_height + self.vertical_spacing)) - 2*self.vertical_spacing
        for ratio in ratios:
            if ratio in self.df.index:
                y = self.df.loc[ratio]
                self.fig.add_trace(
                    go.Bar(
                        x=x,
                        y=y,
                        name=ratio,
                        opacity=0.8,
                        legend=legend_name,
                        showlegend=True),
                        row=row,
                        col=col
                )
        self.fig.update_layout(
            {
                legend_name: dict(
                    xref='paper',
                    yref='paper',
                    x=x_leg,
                    y=y_leg,
                    bgcolor='rgba(0,0,0,0)'
                )
            }
        )


    def create_charts(self):
        self._add_traces(["PER", "PEG"],
                         row=1, col = 1, num = 2)
        self._add_traces(["Rentabilité des actifs (ROA)",
                          "Rentabilité des capitaux propres (ROE)",
                          "Rentabilité du capital total (ROTC)"],
                          row=2, col=1, num = 3)
        self._add_traces(["FCF Yield %",
                          "Total des dettes/capitaux propres",
                          "(EBITDA - Capex) / Charges d'intérêt"],
                          row=1, col= 2, num = 4)
        self._add_traces(["Chiffre d’affaires, CAGR sur 2 ans", 
                          "Résultat net, CAGR sur 2 ans", 
                          "Flux de trésorerie d’exploitation, CAGR sur 2 ans",
                          "Chiffre d’affaires, CAGR sur 5 ans", 
                          "Résultat net, CAGR sur 5 ans", 
                          "Flux de trésorerie d’exploitation, CAGR sur 5 ans"],
                          row=2, col=2, num = 5)

        for i in range(1, 3):
            for j in range(1,3):
                self.fig.update_xaxes(title_text="Année", row=i, col=j,
                                  showline=True, linewidth=2, linecolor="black")
                self.fig.update_yaxes(showline=True, linewidth=2, linecolor="black",
                                  zeroline=True, zerolinecolor="gray", row=i, col=j)
        return self.fig

    def save_graphs(self, filename="graph.html"):
        """Exporte le graphique en HTML interactif + créer un dossier pour graphs"""
        #os.makedirs("graphs", exist_ok=True)
        #os.makedirs("html", exist_ok=True)

        self.fig.write_html(f"html/{self.company}.html")
        #self.fig.write_image(f"graphs/{self.company}.png",format="png")

    def show(self):
        """Affiche le graphique dans le notebook ou le navigateur"""
        self.fig.show()
