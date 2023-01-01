import requests
from bs4 import BeautifulSoup as bs
import time
from datetime import datetime

def proxy_scraper():
    url = 'https://free-proxy-list.net/'
    # request and grab content
    try:
        soup = bs(requests.get(url).content, 'html.parser')
    except Exception as e:
        print(e)
       
    proxies = []
    for row in soup.find(
        'table',attrs={'class': 'table-striped'}
        ).find_all('tr')[1:]:
        tds = row.find_all('td')
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            anonymity = tds[4].text.strip()
            google = tds[5].text.strip()
            https = tds[6].text.strip()
            # code = tds[2].text.strip()
            # country = tds[3].text.strip()
            # retreived_on = datetime.date
            if (
              https == 'no' and anonymity == 'elite proxy' and google =='yes'
              ):
                proxy = str(ip) + ':' + str(port)
                proxies.append(proxy)

        except Exception as e:
            # augment exception handling here
            continue
    return proxies










