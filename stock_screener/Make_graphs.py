import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import os

class Plotter:
    def __init__(self, df, company_name):
        """
        Initialise la figure avec 4 sous-graphiques pour visualiser :
        - Valorisation (PER, PEG)
        - Création de valeur (ROE, ROA, ROTC)
        - Solidité financière & cash réel (Rendement FCF, Dette/CP, (EBITDA-CAPEX)/Interêts)
        - Croissance durable (CAGR 3-5 ans sur CA, Bénéfice net, FCF)
        """
        self.df = df #Stockage de la dataframe
        self.company = company_name.split('/')[0]
        #Crée la figure principale avec Plotly, pouvant contenir plusieurs sous-graphes.
        self.fig = make_subplots(
            rows=4, cols=1,
            subplot_titles=(
                f"Valorisation - {self.company}",
                f"Création de valeur - {self.company}",
                f"Solidité financière et cash réel - {self.company}",
                f"Croissance durable - {self.company}"
            ),
            vertical_spacing=0.1,
        )
        #Applique la mise en page générale : taille, couleur de fond, polices, légende, marges, etc.
        self.fig.update_layout(
            height=900,
            width=1000,
            title_text="Analyse Fondamentale",
            title_font=dict(size=22),
            font=dict(family="Arial", size=14, color="black"),
            showlegend=True,
            plot_bgcolor="white",
            legend=dict(x=1, y=1)
        )

    def _add_traces(self, metrics, row, col):
        x = self.df.columns  # années
        for m in metrics:
            if m in self.df.index:
                y = self.df.loc[m]
                self.fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=m),
                                   row=row, col=col)

    def create_charts(self):
        self._add_traces(["PER", "PEG"], row=1, col = 1)
        self._add_traces(["Rentabilité des actifs (ROA)",
                          "Rentabilité des capitaux propres (ROE)",
                          "Rentabilité du capital total (ROTC)"], row=2, col=1)
        self._add_traces(["FCF Yield %",
                          "Total des dettes/capitaux propres",
                          "(EBITDA - Capex) / Charges d'intérêt"], row=3, col= 1)
        self._add_traces(["Chiffre d’affaires, CAGR sur 2 ans", 
                          "Résultat net, CAGR sur 2 ans", 
                          "Flux de trésorerie d’exploitation, CAGR sur 2 ans",
                          "Chiffre d’affaires, CAGR sur 5 ans", 
                          "Résultat net, CAGR sur 5 ans", 
                          "Flux de trésorerie d’exploitation, CAGR sur 5 ans"], row=4, col=1)

        for i in range(1, 5):
                self.fig.update_xaxes(title_text="Année", row=i, col=1,
                                  showline=True, linewidth=2, linecolor="black")
                self.fig.update_yaxes(showline=True, linewidth=2, linecolor="black",
                                  zeroline=True, zerolinecolor="gray", row=i, col=1)
        return self.fig

    def save_graphs(self, filename="graph.html"):
        """Exporte le graphique en HTML interactif + créer un dossier pour graphs"""
        #os.makedirs("graphs", exist_ok=True)
        #os.makedirs("html", exist_ok=True)

        self.fig.write_html(f"html/{self.company}.html")
        self.fig.write_image(f"graphs/{self.company}.png",format="png")

    def show(self):
        """Affiche le graphique dans le notebook ou le navigateur"""
        self.fig.show()
