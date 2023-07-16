#%%
import helper_functions as helper
from proxy import client
import random

#%%
# urls
base_url = 'https://www.zara.com/us/en'
extension_categories ='/categories'

extension_details = '/product/272001924/extra-detail?ajax=true'
extension_related = '/product/272001924/related'

#%%
# request assets
user_agent = [
    # collected
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.21608.199 Safari/537.36 Avast/114.0.21608.199',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',

    # ai created
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.1919.91',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/1.30.87 Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Brave/1.30.89 Chrome/92.0.4515.159 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/1.30.89 Chrome/92.0.4515.159 Safari/537.36',
    ]

accept_language = [
    'en-US,en;q=0.5',
    'en-US,en;q=0.8',
    'en-US,en-GB;q=0.5,en;q=0.3'
    ]

# headers
headers ={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':random.choice(accept_language),
    'Connection':'keep-alive',
    'Host':'www.zara.com',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'none',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': random.choice(user_agent)
}

#%%
def extract_category_ids(response):
    'extracts the category ids only'
    categories = []
    response = response['categories']
    for item in response:
        customer = item['name']
        if (customer == 'WOMAN' or customer == 'MAN' or customer == 'KIDS'):
            category_ids = item['subcategories'] #[iterate]['subcategories']
            for item in category_ids:
                categories.append(item['id'])
                if item['subcategories']:
                    subcategories = item['subcategories']
                    for item in subcategories:
                        categories.append(item['id'])
    categories = list(set(categories))
    return categories

#%%
def get_categories():
    response = helper.get_page(
        url = 'https://www.zara.com/us/en',
        client = client,
        headers = headers
        )
    categories = extract_category_ids()
    return categories

#%%
def extract_product_list(response):
    products = []
    for i in range(len(response)):
        response = response[i]['elements']
        for i in range(len(response)):
            response = response['commercialComponents']
            products.append(response)
    return products

#%%
def get_product_list(category_ids):
    for category_id in category_ids:
        products_url = f'{base_url}/category/{category_id}/products?ajax=true'
        response = helper.get_page(
            url = products_url,
            client = client,
            headers = headers
            )
        products = extract_product_list(response)
        return products



#%%

categories = helper.get_page(
        url = 'https://www.zara.com/us/en',
        client = client,
        headers = headers
        )
#%%
categories = extract_category_ids()

test = get_products()
#%%
# executions
category_response = get_categories()
print(category_response)

#%%
categories = extract_category_ids(category_response)
print(categories)
# print(categories)
# %%

# https://www.zara.com/us/en/categories