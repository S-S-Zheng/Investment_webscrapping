# stock_screener/fetcher.py
'''
Responsabilité : isolation du scraping de ZoneBourse (URLs, parsing HTML,
récupération de TAG/ISIN/prix, construction du DataFrame des ratios).
On utilise une session partagée pour toutes les requêtes via aiohttp.ClientSession.
Chaque fonction est une co-routine suivant async.
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import re


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0 Safari/537.36"
    )
}
BASE_URL = "https://www.zonebourse.com/cours/action/"

async def fetch_meta(session: aiohttp.ClientSession, company_id: str) -> dict:
    """
    Récupère NOM, TAG, ISIN et prix via la page principale.
    """
    url = f"{BASE_URL}{company_id}"
    # await pour lire le HTML
    async with session.get(url, headers=HEADERS) as r:
        r.raise_for_status()
        text = await r.text()
    soup = BeautifulSoup(text, "html.parser")

#Obtenir le TAG et l'ISIN
    badges = soup.find_all("h2", attrs={"class": "m-0 badge txt-b5 txt-s1"})
    tag, isin = badges[0].text.strip(), badges[1].text.strip()
#Obtenir le prix de l'action et la devise
    price_td = soup.find_all("td", attrs={"class": "txt-s7 txt-align-left is__realtime-last"})
    price_unit = price_td[0].text.strip()
    price = re.split(' \D',price_unit)[0]
#Nom de l'entreprise
    company_name = soup.find("span", attrs = {"class":"pl-5"}).text.strip()

    return {
        "Entreprise": company_name,
        "TAG": tag,
        "ISIN": isin,
        "Prix_devise": price_unit,
        "Prix": float(price.replace('\u202f','').replace(',','.'))
        }

async def fetch_ratios(session: aiohttp.ClientSession,
                       company_id: str, section: str) -> pd.DataFrame:
    """
    Scrape un tableau de ratios pour la section donnée (e.g. 'valorisation',
    'finances-ratios'). Retourne un DataFrame indexé par nom de ratio,
    colonnes = années.
    """
    url = f"{BASE_URL}{company_id}/{section}/"
    async with session.get(url, headers=HEADERS) as r:
        r.raise_for_status()
        text = await r.text()
    soup = BeautifulSoup(text, "html.parser")

    # Récupération des dates
    thead = soup.find("thead")
    #years = [int(span.text.strip()) for span in thead.find_all("span")]
    '''
    Equivalence:
    years=[]
    Date_head=soup.find('thead')
    Date_section=Date_head.find_all('span')
    for k in range(len(Date_section)):
        date_scrap=int(Date_section[k].text.strip())
        years.append(date_scrap)
    '''
    #
    if section == "valorisation":
        # Récupération des lignes du tableau
        tbody = soup.find("tbody")
        rows = tbody.find_all("tr")

        data = {}
        for tr in rows:
            # 1) nom du ratio
            name_td = tr.find("td", attrs={"class": "table-child--w200"})
            if not name_td:
                continue
            name = name_td.text.strip().split("\n")[0]

            # 2) valeurs
            tds = tr.find_all("td")[1:]  # Exclut la 1re cellule titre
            values = []
            for td in tds:
                txt = td.text.strip().replace("\u202f", "").replace("x", "").replace(",", ".")
                try:
                    values.append(float(txt))
                except ValueError:
                    values.append(0.0)
            data[name] = values

        years = [int(span.text.strip()) for span in thead.find_all("span")]

    elif section == "finances-ratios":
        # Récupération des lignes du tableau
        tbody = soup.find_all("tbody")
        rows = tbody[3].find_all("tr")

        data = {}
        for tr in rows:
            # 1) nom du ratio
            name_p = tr.find("p", attrs={"class": "c txt-inline table-child--hover-display m-0 ml-5 pl-0"})
            if not name_p:
                continue
            name = name_p.text.strip().split("\n")[0]

            # 2) valeurs
            tds = tr.find_all("td",attrs={"table-child--right table-child--w80"})
            values = []
            for td in tds:
                txt = td.text.strip().replace("\u202f", "").replace("x", "").replace(",", ".")
                try:
                    values.append(float(txt))
                except ValueError:
                    values.append(0.0)
            data[name] = values

        years = [int(span.text.strip()) for span in thead.find_all("span")]
        start = years[-1]-len(tds)+1
        years = list(filter(lambda x : x >= start, years))
        #years = years[5:]
    else:
        print(
            f"La section {section} comporte une erreur",
            " ou n'a pas encore été validée, veuillez revérifier l'orthographe"
            " ou modifier le fichier fetcher.py"
            )
        pass

    df = pd.DataFrame(data).T
    df.columns = years
    #df_nonT = df.T
    return df,years
