import requests
import json
from proxy import client

def get_page(url, client=client, headers=None, params=None):
    '''function to get the content of a specific url'''
    try:
        response = client.get(url, headers = headers, params = params)
        return response
        # response = requests.get(url, headers = headers)
    except Exception as e:
        return e
    
def page_to_json(response):
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