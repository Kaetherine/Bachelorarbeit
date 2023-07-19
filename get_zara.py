#%%
import helper_functions as helper
from credentials import client
import random
from logger import setup_logger
from to_s3_bucket import upload_json_to_bucket

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
    logger.info('Executing "extract_category_ids".')
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
    categories = list(set(categories))
    return categories

#%%
def extract_product_list(response):
    '''takes the response and saves the key containing 
    the products of that response in "products"'''
    logger.info('Executing "extract_product_list".')
    products = []
    if response:
        for item in response['productGroups']:
            if item['elements']:
                for product in item['elements']:
                    products.extend(product['commercialComponents'])
        return products

#%%
def get_categories():
    '''get the category pages and, extracts the categories from 
    their responses and returns a list of categories'''
    logger.info('Executing "get_categories".')
    response = helper.get_page(
        url = f'{base_url}/categories',
        client = client,
        headers = headers
        )
    if response:
        categories = extract_category_ids(response)
        return categories

#%%
def get_product_list(category_ids):
    '''gets all available products of each category of the to the constructor 
    passed list, extracts the products and assignes them to their category. 
    The functions output is a dictionary with the category as key and a 
    list of its products as values'''
    logger.info('get_product_list".')
    products_by_category = {}
    for category_id in category_ids:
        products_url = f'{base_url}/category/{category_id}/products?ajax=true'
        response = helper.get_page(
            url = products_url,
            client = client,
            headers = headers
            )
        if response:
            products_by_category[str(category_id)] = extract_product_list(response)
    return products_by_category

#%%
def get_products(products_by_category):
    '''takes the dict "product by categories" and returns a list of 
    products (without assigned categories)'''
    logger.info('get_products".')
    products = []
    for category in products_by_category:
        logger.info(category)
        for item in products_by_category[category]:
            products.append(item)
    return products

#%%
def get_product_ids(products_by_category):
    '''returns a list of product ids'''
    logger.info('Executing "get_product_ids".')
    products = get_products(products_by_category)
    product_ids = helper.get_dict_list_values(products, 'id')
    return product_ids

#%%
def get_product_details(product_ids):
    '''gets all product details pages of given product_ids list 
    and filters them by key'''
    logger.info('get_product_details".')
    product_details = {}
    for product_id in product_ids:
        product_details_url = f'{base_url}/product/{product_id}/extra-detail?ajax=true'
        response = helper.get_page(
                url = product_details_url,
                client = client,
                headers = headers
                )
    # filter content
        if response:
            for detail in response:
                product_details[product_id] = {}
                if detail['sectionType'] == 'materials':
                    product_details[product_id]['materials'] = detail
                elif detail['sectionType'] == 'certifiedMaterials':
                    product_details[product_id]['certifiedmaterials'] = detail
                elif detail['sectionType'] == 'origin':
                    product_details[product_id]['origin'] = detail
            if 'certifiedmaterials' not in product_details[product_id]:
                product_details[product_id]['certifiedmaterials'] = None
    return product_details

#%%
def get_related_products(product_ids):
    '''gets the related products and assignes them to called product'''
    logger.info('Executing "get_related_products".')
    related_products = {}
    for product_id in product_ids:
        product_details_url = f'{base_url}/product/{product_id}/related'
        response = helper.get_page(
                url = product_details_url,
                client = client,
                headers = headers
                )
        if response:
            related_products[product_id] = []
            for product in response['recommend']:
                recommended_product = product['id']
                related_products[product_id].append(recommended_product)
    return related_products

def get_zara():
    '''executes all functions to get the content of zara'''
    category_ids = get_categories()
    print(category_ids)

    #%%
    print(category_ids[:2])

    # %%
    products_by_category = get_product_list(category_ids[3:5])

    #%%
    print(products_by_category)
    print(len(products_by_category))

    # %%
    product_ids = get_product_ids(products_by_category)
    print(product_ids)

    # %%
    product_details = get_product_details(product_ids[3:5])

    #%%
    print(product_details)
    print(len(product_details))

    # %%
    related_products = get_related_products(product_ids[3:5])

    #%%
    print(related_products)