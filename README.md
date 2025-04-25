# Investment_webscrapping

**This project has 2 goals:**
[!CAUTION]
    1) *Helping me in my investing strategies by gathering the financials datas of interesting companies*
[!WARNING]
    2) _Improving my programming knowledge using in this case, web scrapping through python_
[!IMPORTANT]
    3) **_BONUS: Starting a data scientist portfolio_**
[!TIP]
    4) ~~Earning money...~~


[!NOTE]
<ins>The first commit will show a usable code and the following commits will improve the coding structure.</ins> :+1:

<!-- This content will not appear in the rendered Markdown -->

simple footnote[¹]
another one [²]

[¹]:footnote [url](https://github.com/S-S-Zheng/Investment_webscrapping)
[²]:footnote2 [url2](https://www.youtube.com/)

##Final structure of the project:

stock_screener/
├── __init__.py          # <— vide
├── fetcher.py
├── transformer.py
├── exporter.py
├── plotter.py
└── main.py

tests/
├── __init__.py          # <— vide
├── test_fetcher.py
├── test_transformer.py
├── test_exporter.py
└── test_plotter.py

README.md
requirements.txt
setup.py


##TODO - Corriger les fichiers du dossier tests
##TODO - Ajouter les ignore dans gitignore
[!WARNING] ##TODO - Modifier les valeurs de millier et les titres cf ci-suit:
    #Muliplication des lignes par 1000000
    #Methode alternative:   map(lambda x: x * 1E6, data['Capitalisation'])
    dico_valeurs['Capitalisation'] = [(1E6)*x for x in dico_valeurs['Capitalisation']]
    dico_valeurs['Valeur Entreprise'] = [(1E6)*x for x in dico_valeurs['Valeur Entreprise']]
    dico_valeurs["Chiffre d'affaires"] = [(1E6)*x for x in dico_valeurs["Chiffre d'affaires"]]
    dico_valeurs['EBITDA'] = [(1E6)*x for x in dico_valeurs['EBITDA']]
    dico_valeurs['Résultat net'] = [(1E6)*x for x in dico_valeurs['Résultat net']]
    dico_valeurs["Endettement Net"] = [(1E6)*x for x in dico_valeurs['Endettement Net']]
    dico_valeurs['Nbr de Titres (en Milliers)'] = [(1E6)*x for x in dico_valeurs['Nbr de Titres (en Milliers)']]
    #Modifier la clef sur le nombre de titre
    dico_valeurs['Nbr de Titres']=dico_valeurs.pop('Nbr de Titres (en Milliers)')
################################################################
    #Mise en df
    #df=pd.DataFrame.from_dict(dico_valeurs,orient='index')
    #Multiplication de 1000000 pour les lignes concernées
    #df.loc['Capitalisation',:] *= 1E6
    #df.loc['Valeur Entreprise',:] *= 1E6
    #df.loc["Chiffre d'affaires",:] *= 1E6
    #df.loc['EBITDA',:] *= 1E6
    #df.loc['Résultat net',:] *= 1E6
    #df.loc["Endettement Net",:] *= 1E6
    #df.loc['Nbr de Titres (en Milliers)',:] *= 1E6
###################################################################
##TODO - Retirer les lignes inutiles?
##TODO - Ajouter des ratios?ROIC?