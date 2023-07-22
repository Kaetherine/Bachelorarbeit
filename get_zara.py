#%%
import helper_functions as helper
from credentials import client
import random
from logger import setup_logger
from s3_bucket import upload_json_to_bucket

#%%
logger = setup_logger()

#%%
base_url = 'https://www.zara.com/de/en'

#%%
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

#%%
accept_language = [
    'en-US,en;q=0.5',
    'en-US,en;q=0.8',
    'en-US,en-GB;q=0.5,en;q=0.3'
    ]

#%%
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
    '''extracts the category ids only'''
    logger.info('Executing extract_category_ids.')
    categories = []
    if response:
        response = response['categories']
    for item in response:
        customer = item['name']
        if (customer == 'WOMAN' or customer == 'MAN' or customer == 'KIDS'):
            category_ids = item['subcategories']
            for item in category_ids:
                categories.append(item['id'])
                if item['subcategories']:
                    subcategories = item['subcategories']
                    for item in subcategories:
                        categories.append(item['id'])
    categories = {'category_ids':list(set(categories))}
    return categories

#%%
def get_categories():
    '''get the category pages and, extracts the categories from 
    their responses and returns a list of categories'''
    logger.info('Executing get_categories.')
    response = helper.get_page(
        url = f'{base_url}/categories',
        client = client,
        headers = headers
        )
    if response:
        categories = extract_category_ids(response)
        return categories

#%%
def extract_product_list(response):
    '''takes the response and saves the key containing 
    the products of that response in "products"'''
    logger.info('Executing extract_product_list.')
    products = []
    if 'productGroups' in response:
        for item in response['productGroups']:
            if 'elements' in item:
                for product in item['elements']:
                    if 'commercialComponents' in product:
                        products.append(product['commercialComponents'])
    return products

#%%
def get_product_list(category_id):
    '''gets all available products of each category of the to the constructor 
    passed list, extracts the products and assignes them to their category. 
    The functions output is a dictionary with the category as key and a 
    list of its products as values'''
    logger.info('Executing get_product_list.')
    products_url = f'{base_url}/category/{category_id}/products?ajax=true'
    response = helper.get_page(
        url = products_url,
        client = client,
        headers = headers
        )
    if response:
        product_list = extract_product_list(response)
    return product_list

#%%
def extract_products(products_by_category):
    '''takes the dict "product by categories" and returns a list of 
    products (without assigned categories)'''
    logger.info('Executing get_products.')
    products = []
    for category in products_by_category:
        logger.info(f'category_id: {category}')
        for item in products_by_category[category]:
                for product in item:
                    if 'id' in product:
                        products.append(product)
    return products

#%%
def extract_product_ids(products_by_category):
    '''returns a list with product ids'''
    logger.info('Executing get_product_ids.')
    products = extract_products(products_by_category)
    product_ids = {
        'product_ids': [str(product['id']) for product in products]
        }
    product_ids['product_ids'] = list(set(product_ids['product_ids']))
    return product_ids

#%%
def get_product_details(product_id):
    '''gets products details of in the constructor passed product
    and returns the response'''
    logger.info('Executing get_product_details.')
    logger.info(f'product details for: {product_id}')
    product_details_url = f'{base_url}/product/{product_id}/extra-detail?ajax=true'
    response = helper.get_page(
            url = product_details_url,
            client = client,
            headers = headers
            )
    return response

#%%
def extract_related_product_ids(response):
    '''extracts related products by id, stores them in a list and retunrs that list'''
    recommended_products = []
    if 'recommend' in response:
        for product in response['recommend']:
            recommended_products.append(str(product['id']))
        return recommended_products
    
#%%
def get_related_products(product_id):
    '''gets the related products of in constructor passed products and returns'''
    logger.info('Executing get_related_products.')
    logger.info(f'related products for: {product_id}')
    product_details_url = f'{base_url}/product/{product_id}/related'
    response = helper.get_page(
            url = product_details_url,
            client = client,
            headers = headers
            )
    if response:
        recommended_products = extract_related_product_ids(response)
        return recommended_products