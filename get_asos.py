import helper_functions as helper

#%%
# welcome_url = 'https://www.asos.com/de/damen/'
welcome_url = 'https://www.asos.com/api/fashion/contentapi/v1/components/?country=DE&store=DE&lang=de-DE&keystoredataversion=ornjx7v-36&viewscope=women&context=eyJwcmVtaWVyIjoiRiIsImN1c3RvbWVyU3RhdHVzIjoidW5rbm93biJ9'
# categories_url
categories_url = 'https://www.asos.com/api/fashion/navigation/v2/tree/navigation?country=GB&keyStoreDataversion=ornjx7v-36&lang=en-GB'

# %%
def get_items(category):
    '''This function executes an api call for the given category'''
    items_url = f'https://www.asos.com/api/product/search/v2/categories/{category}?offset=0&store=DE&lang=de-DE&currency=EUR&rowlength=3&channel=desktop-web&country=DE&keyStoreDataversion=ornjx7v-36&limit=72&attribute_1047=8416'
    items = helper.get_page(items_url)
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
    product_ids = helper.get_dict_list_values(products, 'id')
    return product_ids


# %%
def get_single_product(product_id):
    '''Text here'''
    single_product_url = f'Fill in the URL here{product_id}'
    product = helper.get_page(single_product_url)
    return product

# %%
def get_look(id):
    '''Text here'''
    look_url = f'https://www.asos.com/api/product/search/v2/buythelook/{id}?store=DE&currency=EUR&lang=de-DE'
    look = helper.get_page(look_url)
    return look

# %%
def extract_categories(json_response, k):
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
category_response = helper.get_page(categories_url)

#%%
men_categories = helper.get_categories(category_response, 0) #write to DL
women_categories = helper.get_categories(category_response, 1) #write to DL

