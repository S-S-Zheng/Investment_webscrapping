# stock_screener/Make_graphs_nosubplot.py
'''
Same as Make_graphs with Plotter class but without using subplots.
Plotly is quite annoying when it comes to split legends through subplots (either
difficulties in placing sublegends + no more dynamic legend or lack in space + one big legend list).

This module will only display one plot with a hell big legend but it'll stay interactive
'''
import plotly.graph_objects as go
import pandas as pd

class Plotter:
    def __init__(self, df:pd.DataFrame, company_name:list):
        """
        Displays a plot with many ratios such as:
        - Evaluation of the company (PER, PEG)
        - Returns of values (ROE, ROA, ROTC)
        - Financial stability and cash (FCF yield, Debt/equity, (EBITDA-CAPEX)/interests)
        - Growth (CAGR 3-5 years on revenue, net income, FCF)
        """
        self.df = df # Store the df
        self.company = company_name.split('/')[0]


        self.legend_group=[
        "Valorisation",
        "Création de valeur",
        "Solidité financière et cash réel",
        "Croissance durable"
        ]

        '''
        Couldn't find a better way to place these &é"ù*$ legend groups but this method is bad.
        Need to find a better way...
        '''
        self.legend_space =[
            0.9, 0.79, 0.52, 0.22
        ]

        #Applique la mise en page générale : taille, couleur de fond, polices, légende, marges, etc.
        self.fig = go.Figure().update_layout(
            #autosize = True,
            width=1000,
            height=900,
            title_text=f"Analyse Fondamentale - {self.company}",
            title_font=dict(size=22),
            title_x = 0.5,
            font=dict(family="Arial", size=14, color="black"),
            showlegend=True,
            plot_bgcolor="white",
            bargap = 0.3,
            bargroupgap = 0.1
        )


    def _add_traces(self, ratios:list, num:int):
        x = self.df.columns
        legend_name = f'legend{num}'

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
                        #Gather legends in groups but group the interactiveness too
                        #legendgroup=self.legend_group[num-1]
                        ),
                )
        self.fig.update_layout(
            {
                legend_name: dict(
                    title = dict(text=self.legend_group[num-1]),
                    xref="paper", yref="paper",
                    x=1.02,
                    y=self.legend_space[num-1],
                    xanchor="left",
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="black",
                    borderwidth=1,
                )
            }
        )


    def create_charts(self):
        self._add_traces(["PER",
                          "PEG",
                          "PCF"],
                         num = 1)
        self._add_traces(["Rentabilité des actifs (ROA)",
                          "Rentabilité des capitaux propres (ROE)",
                          "Rentabilité sur le capital investi (ROIC approximé)",
                          "Marge brute %",
                          "Marge nette %"],
                          num = 2)
        self._add_traces(["FCF Yield %",
                          "FCF",
                          "Total des dettes/capitaux propres",
                          "(EBITDA - Capex) / Charges d'intérêt",
                          "Current Ratio"],
                          num = 3)
        self._add_traces(["Chiffre d’affaires, CAGR sur 2 ans", 
                          "Résultat net, CAGR sur 2 ans", 
                          "Flux de trésorerie d’exploitation, CAGR sur 2 ans",
                          "Chiffre d’affaires, CAGR sur 5 ans", 
                          "Résultat net, CAGR sur 5 ans", 
                          "Flux de trésorerie d’exploitation, CAGR sur 5 ans"],
                          num = 4)

        self.fig.update_xaxes(title_text="Année",showline=True, linewidth=2, linecolor="black")
        self.fig.update_yaxes(showline=True, linewidth=2, linecolor="black",
                              zeroline=True, zerolinecolor="gray")

    def save_graphs(self, filename="graph.html"):
        """Exporte le graphique en HTML interactif + créer un dossier pour graphs"""
        #os.makedirs("graphs", exist_ok=True)
        #os.makedirs("html", exist_ok=True)

        self.fig.write_html(f"html/{self.company}.html")
        #self.fig.write_image(f"graphs/{self.company}.png",format="png")

    def show(self):
        """Affiche le graphique dans le notebook ou le navigateur"""
        self.fig.show()
