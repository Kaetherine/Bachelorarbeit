import requests
from bs4 import BeautifulSoup as bs
# import time
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
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        anonymity = tds[4].text.strip()
        google = tds[5].text.strip()
        https = tds[6].text.strip()
        # country_code = tds[2].text.strip()
        # country = tds[3].text.strip()
        # retreived_on = datetime.date
        if (
            https == 'yes' and anonymity == 'elite proxy' and google =='yes'
            ):
            proxy = str(ip) + ':' + str(port)
            proxies.append(proxy)
        else:
            continue
    return proxies

def test_scraper():

    url = "https://ipinfo.io/json"
    proxies = proxy_scraper()

    if proxies == []:
        print('No Proxies.')
    else:
        for proxy in proxies:
            proxies = {
                'http': proxy,
                'https': proxy,
            }
            try:
                response = requests.get(url, proxies=proxies)
                print(response.json())
            except:
                print(f'Proxie {proxy} is occupied.')
                continue

test_scraper()









