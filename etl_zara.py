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

def normalize_products_by_categories(json):
    pass

def normalize_products(json):
    pass

def products_to_df(list_of_products):
    df_products = pd.DataFrame(list_of_products)
    return df_products

def extract_product_details(**keys):
    product_details = get_bucket_file(f'{date}-product_details.json')
    for product in product_details:
        for detail in product_details[product]:
            if 'care' in detail:
                care = detail['sectionType']['care']
            if 'certifiedMaterials' in detail:
                certified_materials = detail['sectionType']['certifiedMaterials']
            if 'materials' in detail:
                materials = detail['sectionType']['materials']
            if 'origin' in detail:
                origin = detail['sectionType']['origin']
    return care, certified_materials, materials, origin