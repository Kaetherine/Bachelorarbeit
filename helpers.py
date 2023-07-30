import csv
from datetime import datetime
import json
from ratelimiter import RateLimiter
import traceback

from credentials import client
from logger import setup_logger


# date = datetime.now().strftime('%Y-%m-%d')
date = '2023-07-29'

csv_path = '/home/ubuntu/Bachelorarbeit/'

logger = setup_logger()
rate_limiter = RateLimiter(max_calls=4, period=1)

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
            logger.error(f'{e}: {traceback.format_exc()}')
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

def create_csv_file(data, csv_file_name):
    '''Creates a csv file from a list of tuples'''
    with open(csv_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    return csv_file_name

def compare_list_of_tups(list1, index_list1, list2, index_list2):
    '''Compares elements at a specific index in the tuples of two lists.'''
    outliers = []
    elements_list2 = {item[index_list2] for item in list2}

    for item in list1:
        if item[index_list1] not in elements_list2:
            outliers.append(item[index_list1])

    logger.info(f'compare_list_of_tups: {outliers} of {list1} could not be found in {list2}')
    return outliers


def remove_outliers_from_tup(list_containing_outliers, i, outliers):
    '''Removes tuples from a list if the element at a specific index is 
    found in the list "outliers".'''
    for tup in list_containing_outliers:
        if tup[i] in outliers:
            list_containing_outliers.delete(tup[i])

    return list_containing_outliers

    return filtered_list

def compare_list_of_tups_and_remove_outliers(list1, index_list1, list2, index_list2):
    '''Compares two lists of tuples at specific indices and removes the tuples from list1 
    if the elements at index_list1 are not found at index_list2 in list2.'''
    
    outliers = compare_list_of_tups(list1, index_list1, list2, index_list2)
    filtered_list = remove_outliers_from_tup(list1, index_list1, outliers)

    return filtered_list

