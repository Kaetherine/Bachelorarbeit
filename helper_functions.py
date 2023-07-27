import json
from ratelimiter import RateLimiter
from datetime import datetime
import pandas as pd
import csv

from credentials import client
from logger import setup_logger

date = datetime.now().strftime('%Y-%m-%d')

logger = setup_logger()
rate_limiter = RateLimiter(max_calls=5, period=1)

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

    
def page_to_json(response):
    '''takes a string structured as json and converts it to json'''
    if response:
        try:
            json_response = json.loads(response.text)
            return json_response
        except Exception as e:
            logger.error(e)
            pass

def get_page(url, client=client, headers=None, params=None):
    '''Gets and extracts the categories from given url'''
    response = get_raw_page(
        url = url,
        client = client,
        headers = headers,
        params = params
        )
    response = page_to_json(response)
    return response

def convert_date(date_string):
    '''Converts the formate of a datetime string. Example 2023-07-23'''
    date_time_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_time_obj.date()

def flatten_and_convert_to_df(obj):
    '''Flatten a nested list and convert it into a DataFrame.'''
    obj = [item for sublist in obj for item in sublist]
    df_obj = pd.DataFrame(obj)
    return df_obj

def create_csv_file(data, csv_file_name):
    '''Creates a csv file from a list of tuples'''
    with open(csv_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    return csv_file_name