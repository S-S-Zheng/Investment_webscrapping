import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import os

class Plotter:
    def __init__(self, df, company_name):
        """
        Initialise la figure avec 3 sous-graphiques pour visualiser :
        - Valorisation (PER, PEG)
        - Gestion des ressources (ROE, ROA, Marge nette)
        - Maîtrise des coûts (Debt/Equity, Current ratio, EV/EBITDA)
        """
        self.df = df #Stockage de la dataframe
        self.company = company_name.split('/')[0]
        #Crée la figure principale avec Plotly, pouvant contenir plusieurs sous-graphes.
        self.fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                f"Valorisation - {self.company}",
                f"Gestion des ressources - {self.company}",
                f"Maîtrise des coûts - {self.company}"
            ),
            vertical_spacing=0.1
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
            legend=dict(x=0.85, y=1)
        )

    '''
    def _plot_line(self, x, y, name, row, col):
        self.fig.add_trace(
            go.Scatter(x=x, y=y, mode="lines+markers", name=name),
            row=row, col=col
        )

    def create_charts(self):
        """
        Ajoute les 3 graphiques fondamentaux à la figure :
        - Valorisation : PER, PEG
        - Ressources : ROE, ROA, Marge nette
        - Coûts : Debt/Equity, Current ratio, EV/EBITDA
        """
        x = self.df["Année"] if "Année" in self.df.columns else self.df.index

        # Graphique 1 : Valorisation
        for metric in ["PER", "PEG"]:
            if metric in self.df.columns:
                self._plot_line(x, self.df[metric], metric, row=1, col=1)

        # Graphique 2 : Gestion des ressources
        for metric in ["Rentabilité des actifs (ROA)", "Rentabilité des capitaux propres (ROE)", "Marge nette %"]:
            if metric in self.df.columns:
                self._plot_line(x, self.df[metric], metric, row=2, col=1)

        # Graphique 3 : Maîtrise des coûts
        for metric in ["Total des dettes/capitaux propres", "Current Ratio", "Valeur Entreprise / EBITDA"]:
            if metric in self.df.columns:
                self._plot_line(x, self.df[metric], metric, row=3, col=1)

        # Mise en forme des axes
        for i in range(1, 4):
            self.fig.update_xaxes(title_text="Année", row=i, col=1, showline=True, linewidth=2, linecolor='black')
            self.fig.update_yaxes(showline=True, linewidth=2, linecolor='black', zeroline=True, zerolinewidth=1, zerolinecolor='gray', row=i, col=1)
    '''
    def _add_traces(self, metrics, row):
        x = self.df.columns  # années
        for m in metrics:
            if m in self.df.index:
                y = self.df.loc[m]
                self.fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=m),
                                   row=row, col=1)

    def create_charts(self):
        self._add_traces(["PER", "PEG"], row=1)
        self._add_traces(["Rentabilité des actifs (ROA)", "Rentabilité des capitaux propres (ROE)", "Marge nette %"], row=2)
        self._add_traces(["Total des dettes/capitaux propres", "Current Ratio", "Valeur Entreprise / EBITDA"], row=3)
        for i in range(1, 4):
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



'''
    def create_charts(self):
        self._add_traces(["PER", "PEG"], row=1)
        self._add_traces(["roe", "roa", "marge_nette_pct"], row=2)
        self._add_traces(["debt_equity", "current_ratio", "ev_ebitda"], row=3)
        for i in range(1, 4):
            self.fig.update_xaxes(title_text="Année", row=i, col=1,
                                  showline=True, linewidth=2, linecolor="black")
            self.fig.update_yaxes(showline=True, linewidth=2, linecolor="black",
                                  zeroline=True, zerolinecolor="gray", row=i, col=1)
        return self.fig

    def save_html(self, path):
        self.fig.write_html(path)
'''