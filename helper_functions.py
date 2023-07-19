# import requests
import json
from credentials import client
from logger import setup_logger
from ratelimiter import RateLimiter

logger = setup_logger()
rate_limiter = RateLimiter(max_calls=3, period=1)

def get_raw_page(url, client=client, headers=None, params=None):
    '''function to get the content of a specific url'''
    with rate_limiter:
        try:
            response = client.get(url, headers = headers, params = params)
            logger.info(
                f'''
                statuscode: {response.status_code},
                url: {url},
                headers: {headers},
                params:{params}'''
            )
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