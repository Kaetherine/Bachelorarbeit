import requests
import json
from proxy import client
from logger import setup_logger

logger = setup_logger()

def get_raw_page(url, client=client, headers=None, params=None):
    '''function to get the content of a specific url'''
    try:
        response = client.get(url, headers = headers, params = params)
        logger.info(f'{response.status_code}, {url}')
        return response
    except Exception as e:
        logger.error(f'{url}, e')
        return None
    
def page_to_json(response):
    '''takes a string structured as json and converts it to json'''
    try:
        json_response = json.loads(response.text)
        return json_response
    except Exception as e:
        logger.error(e)
        return None

def get_page(url, client=client, headers=None, params=None):
    '''gets and extracts the categories from given url'''
    response = get_raw_page(
        url = url,
        client = client,
        headers = headers,
        params = params
        )
    if response:
        response = page_to_json(response)
        return response
    
def get_dict_list_values(dict_list, k):
    '''function to get values of given key of a list of dictionaries'''
    values = [str(product[k]) for product in dict_list]
    return values