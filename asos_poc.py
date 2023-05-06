# %%
import requests
import json

def get_page(url):
    try:
        response = requests.get(url).text
    except Exception as e:
        return e
    try:
        json_response = json.loads(response)
        return json_response
    except:
        return response
    

items = 'https://www.asos.com/api/product/search/v2/categories'

print(get_page(items))
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


