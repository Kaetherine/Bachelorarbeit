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
    care, certified_materials, materials, origin = None, None, None, None
    for product in product_details:
        for detail in product_details[product]:
            section_type = detail['sectionType']
            if section_type == 'care':
                care = detail
            elif section_type == 'certifiedMaterials':
                certified_materials = detail
            elif section_type == 'materials':
                materials = detail
            elif section_type == 'origin':
                origin = detail
    return care, certified_materials, materials, origin