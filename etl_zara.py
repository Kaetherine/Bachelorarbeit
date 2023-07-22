from datetime import datetime
import pandas as pd

from postgres_connection import connect_to_db, disconnect_from_db
from s3_bucket import *
from get_zara import extract_products


date = datetime.now().strftime('%Y-%m-%d')

def normalize_related_products(json):
    result = []
    for key, values in json.items():
        for value in values:
            result.append((key, value))
    return result

def normalize_product_details(json):
    pass

def normalize_products_by_categories(json):
    pass

def normalize_products(json):
    pass

def products_to_df(list_of_products):
    df_products = pd.DataFrame(list_of_products)
    return df_products

products = get_bucket_file(
    f'{date}-products.json', 'raw-apparel-marketdata'
    )

df = products_to_df(products)
print(df.columns)


def product_details(json):
    pass
    '''doctstring here'''
        # filter content
    # product_details = {}
    # if response:
    #     for detail in response:
    #         product_details[product_id] = {}
    #         if detail['sectionType'] == 'materials':
    #             product_details[product_id]['materials'] = detail
    #         elif detail['sectionType'] == 'certifiedMaterials':
    #             product_details[product_id]['certifiedmaterials'] = detail
    #         elif detail['sectionType'] == 'origin':
    #             product_details[product_id]['origin'] = detail
    #     if 'certifiedmaterials' not in product_details[product_id]:
    #         product_details[product_id]['certifiedmaterials'] = None
    # return product_details