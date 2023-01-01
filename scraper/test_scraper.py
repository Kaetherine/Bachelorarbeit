import requests
from proxy_scraper import proxy_scraper

def test_scraper():

    url = "https://ipinfo.io/json"
    proxies = proxy_scraper()

    if proxies == []:
        print('Proxies = []')
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
                # if proxy is occupied
                continue

test_scraper()