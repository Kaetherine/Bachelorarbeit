# %%
import requests
import json

#%%
def get_page(url):
    try:
        response = requests.get(url)
    except Exception as e:
        return e
    try:
        json_response = json.loads(response.text)
        return json_response
    except Exception as e:
        return e
categories_url = 'https://www.asos.com/api/fashion/navigation/v2/tree/navigation?country=GB&keyStoreDataversion=ornjx7v-36&lang=en-GB'

json_response = get_page(categories_url)
men = json_response[0]
women = json_response[1]
# categories_w = women['link']['categoryId']
print(women['link'].keys())

# for item in women:
#     print(item, '\n')


# categories = [
#     'Bestsellers',
#     'New in',
#     'Dresses',
#     'Tops',
#     'Swimwear & Beachwear',
#     'Skirts',
#     'Shorts',
#     'Blazers',
#     'Cargo Trousers',
#     'Co-ords',
#     'Coats & Jackets',
#     'Curve & Plus Size',
#     'Designer',
#     'Exclusives at ASOS',
#     'Hoodies & Sweatshirts',
#     'Jeans',
#     'Jumpers & Cardigans',
#     'Jumpsuits & Playsuits',
#     'Lingerie & Nightwear',
#     'Loungewear',
#     'Maternity',
#     'Multipacks',
#     'Petite',
#     'Shirts & Blouses',
#     'Socks & Tights',
#     'Sportswear',
#     'Suits & Tailoring',
#     'T-Shirts & Vests',
#     'Tall',
#     'Tracksuits & Joggers',
#     'Trousers & Leggings',
#     'Workwear'
#     ]
# items_api = 'https://www.asos.com/api/product/search/v2/categories/2623?offset=0&store=DE&lang=de-DE&currency=EUR&rowlength=3&channel=desktop-web&country=DE&keyStoreDataversion=ornjx7v-36&limit=72&attribute_1047=8416'


# # %%
# # url = 'https://www.asos.com/api/product/search/v2/categories/20553?offset=0&store=DE&lang=de-DE&currency=EUR&rowlength=3&channel=desktop-web&country=DE&keyStoreDataversion=ornjx7v-36&limit=72&base_colour=3'
# single_item_url = 'https://www.asos.com/api/product/search/v2/buythelook/204189058?store=DE&currency=EUR&lang=de-DE'
# # 204
# response = requests.get(single_item_url)
# print(response)

# # %%
# response = json.loads(response.text)
# print(response)

# # %%
# for k in response['pr']:
#   print(k)
# # searchTerm
# # categoryName
# # itemCount
# # redirectUrl
# # products
# # facets
# # diagnostics
# # searchPassMeta
# # queryId
# # discoverSearchProductTypes
# # campaigns
# # print(response)

# # %%
# for key in response:
#   print(key)


