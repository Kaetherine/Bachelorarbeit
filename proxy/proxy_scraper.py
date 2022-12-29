import requests
from bs4 import BeautifulSoup as bs
import time

def proxy_scraper():
    url = 'https://free-proxy-list.net/'
    # request and grab content
    try:
        soup = bs(requests.get(url).content, 'html.parser')
    except Exception as e:
        print('hi')
        print(e)
        # time.sleep(600)
    # to store proxy_adresses
    proxies = []
    for row in soup.find('table', attrs={'class': 'table-striped'}).find_all('tr')[1:]:
        tds = row.find_all('td')
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(str(ip) + ':' + str(port))
        except IndexError:
            continue
    return proxies










