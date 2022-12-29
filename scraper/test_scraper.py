import requests
from proxy_scraper import proxy_scraper

def test_scraper():

    url = "http://httpbin.org/ip"
    proxies = proxy_scraper()

    if proxies == []:
        print('bye')
        pass
    else:
        for i in range(len(proxies)-1):
            try:
                response = requests.get(url, proxies = {"http":proxies[i], "https":proxies[i]})
                print(response.json())
            except:
                # if the proxy is pre occupied
                print(f'Proxy is occupied.')

test_scraper()