# stock_screener/fetcher.py
'''
Fetch the datas from Zone Bourse using the URLs and parsing into HTML (TAG, ISIN, prices...).
The requests uses async methods through aiohttp.ClientSession
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import re
from currency_converter import CurrencyConverter



HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0 Safari/537.36"
    )
}
BASE_URL = "https://www.zonebourse.com/cours/action/"

async def fetch_calendar(session: aiohttp.ClientSession,
                        company_id: str, section: str) -> dict:
    """
    Fetch the coming events names and date
    """
    url = f"{BASE_URL}{company_id}{section}"
    # await pour lire le HTML
    async with session.get(url, headers=HEADERS) as r:
        r.raise_for_status()
        text = await r.text()
    soup = BeautifulSoup(text, "html.parser")
    # Store the related table
    table = soup.find_all('table', class_=["table","table--small","table--bordered"])[2]
    rows = table.find_all('tr')
    unsorted_events = {}
    #Filtering by ignoring everything aside from Quarter and year in its name
    for tr in rows:
        if re.search(r'\bQ[1-4]\s\d{4}',tr.find_all('td')[1].text.strip()):
            unsorted_events[tr.find_all('td')[1].text.strip()]=re.sub(
                '\n\s{44}',' ',
                tr.find_all('td')[0].text.strip()
                )
            '''
            unsorted_events[tr.find_all('td')[1].text.strip()]=(
                tr.find_all('td')[0].text.strip()
                .replace('\n                                            ','-'))
            '''

    return unsorted_events

async def fetch_meta(session: aiohttp.ClientSession, company_id: str) -> dict:
    """
    Retrieve name, tag, isin and price
    """
    url = f"{BASE_URL}{company_id}"

    async with session.get(url, headers=HEADERS) as r:
        r.raise_for_status()
        text = await r.text()
    soup = BeautifulSoup(text, "html.parser")

# TAG, ISIN, Country, Sector
    '''
    badges = soup.find_all("h2", attrs={"class": "m-0 badge txt-b5 txt-s1"})
    '''
    badges = soup.find_all("h2", class_=["m-0" ,"txt-b5", "txt-s1"])
    country = badges[0].i.attrs['title']
    tag = badges[1].text.strip()
    isin =  badges[2].text.strip()
    sector = badges[3].text.strip()
# Price and Currency
    price_td = soup.find_all("td",
                            class_=["txt-s7","is__realtime-last","txt-align-left"])
    price_unit = price_td[0].text.strip()
    unitless = re.split(' \D',price_unit)[0]
    price = float(unitless.replace('\u202f','').replace(',','.'))
    try:
        price_euro = CurrencyConverter().convert(price,price_unit.split()[-1],'EUR')
    except ValueError:
        price_euro = "N/A"
# Name of the company
    company_name = soup.find("span", attrs = {"class":"pl-5"}).text.strip().split('(')[0]
# Fluctuation of the price for 5 days and since january the 1st
    var_week = soup.find_all("span",
                            class_=["variation variation--pos","variation--no-bg","txt-bold"]
                            )[2].text.strip().replace('\xa0', ' ')
    var_jan = soup.find_all("span",
                            class_=["variation variation--pos","variation--no-bg","txt-bold"]
                            )[3].text.strip().replace('\xa0', ' ')
    return {
        "Entreprise": company_name,
        "Pays": country,
        "TAG": tag,
        "ISIN": isin,
        "Secteur": sector,
        "Prix_devise": price_unit,
        "Prix en euros": price_euro,
        "Variation sur 5 jours": var_week,
        "Variation depuis le 1er janvier": var_jan
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
                txt = td.text.strip().replace("\u202f", "").replace("x", "").replace(",", ".").replace("\xa0%",'')
                if name == "Date de publication":
                    values.append(txt)
                else:
                    try:
                        values.append(float(txt))
                    except ValueError:
                        values.append('')
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
                if '\xa0k' in txt:
                    txt = float(txt.replace(',','.').replace('\xa0k',''))*1E3
                    values.append(txt)
                else:
                    try:
                        values.append(float(txt))
                    except ValueError:
                        values.append('')
            data[name] = values

        years = [int(span.text.strip()) for span in thead.find_all("span")]
        start = years[-1]-len(tds)+1
        years = list(filter(lambda x : x >= start, years))
    else:
        print(
            f"Section {section} has an issue or hasn't been validated yet",
            " Please check again or modify fetcher.py file."
            )
        pass

    df = pd.DataFrame(data).T
    df.columns = years

    return df,years