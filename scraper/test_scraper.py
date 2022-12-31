import requests
from proxy.proxy_scraper import proxy_scraper

def test_scraper():

    url = "https://ipinfo.io/json"
    proxies = proxy_scraper()

    if proxies == []:
        print('no proxies')
    else:
        for proxy in proxies:
            proxies = {
                'http': proxy,
                'https': proxy,
            }
            try:
                response = requests.get(url, proxies = proxies)
                print(response.json())
            except:
                # if the proxy is pre occupied
                print(f'Proxy is occupied.')

test_scraper()