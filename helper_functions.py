import requests
import json
from proxy import client

def get_page(url, client=client, headers=None, params=None):
    '''function to get the content of a specific url'''
    try:
        response = client.get(url, headers = headers, params = params)
        # response = requests.get(url, headers = headers)
        print(response)
    except Exception as e:
        return e
    try:
        json_response = json.loads(response.text)
        return json_response
    except Exception as e:
        return e

# %%
def get_dict_list_values(dict_list, k):
    '''function to get values of given key of a list of dictionaries'''
    values = [product[k] for product in dict_list]
    return values

# %%
def get_items(category):
    '''This function executes an api call for the given category'''
    items_url = f'https://www.asos.com/api/product/search/v2/categories/{category}?offset=0&store=DE&lang=de-DE&currency=EUR&rowlength=3&channel=desktop-web&country=DE&keyStoreDataversion=ornjx7v-36&limit=72&attribute_1047=8416'
    items = get_page(items_url)
    return items

# %%
def get_products(category):
    '''Text here'''
    items = get_items(category)
    products = items['products']
    return products

# %%
def get_product_id(products):
    '''Text here'''
    product_ids = get_dict_list_values(products, 'id')
    return product_ids


# %%
def get_single_product(product_id):
    '''Text here'''
    single_product_url = f'Fill in the URL here{product_id}'
    product = get_page(single_product_url)
    return product

# %%
def get_look(id):
    '''Text here'''
    look_url = f'https://www.asos.com/api/product/search/v2/buythelook/{id}?store=DE&currency=EUR&lang=de-DE'
    look = get_page(look_url)
    return look

# %%
# look = get_look(204704267)
# ids = get_dict_list_values(look['products'], 'id')
# ids

# %%
category_response = get_page(categories_url)
category_response

# %%
def get_categories(json_response, k):
    '''This function searches for all available product categories
    to be able to call every product from the api'''
    category_ids = []

    categories = json_response[k]['children']
    for value in categories:
        if value['link'] != None:
            # logg here instead of pass
            pass
        if value['children']:
            for item in value['children']:
                if item['link']['linkType'] == 'category':
                    category = item['link']['categoryId']
                    category_ids.append(category)
                if item['children']:
                    for entry in item['children']:
                        if entry['link'] != None:
                            # logg here instead of pass
                            pass
                        if entry['children']:
                            for val in entry['children']:
                                if val['children']:
                                    # logg here instead of pass
                                    pass
                                if val['link']['linkType'] == 'category':
                                    category = val['link']['categoryId']
                                    category_ids.append(category)
    return list(set(category_ids))

# %%
men_categories = get_categories(category_response, 0) #write to DL
women_categories = get_categories(category_response, 1) #write to DL

# %%
# categories = men_categories.extend(women_categories)
i = 0
for category in women_categories:
    if i == 1:
        products = get_items(category) #write to DL
        print(products)
        i += 1
    else:
        break


# %%
# customers = items[0]['data']['columns'][0]['buttons']
# customers = get_dict_list_values(customers, 'url')
# customers


