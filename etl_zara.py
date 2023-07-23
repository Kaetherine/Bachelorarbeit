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

def extract_product_details(product_details, product_id):
    '''This function extracts care, certified materials, materials, and 
    origin details for a given product from the product details dataset.'''
    care, certified_materials, materials, origin = None, None, None, None
    for detail in product_details[product_id]:
        section_type = detail['sectionType']
        if section_type == 'care':
            care = detail
        elif section_type == 'certifiedMaterials':
            certified_materials = detail
        elif section_type == 'materials':
            materials = detail
        elif section_type == 'origin':
            origin = detail
    return [product_id, care, certified_materials, materials, origin]

def extract_care():
    pass
        
def extract_certified_materials():
    pass

def extract_materials(materials):
    '''docstring here'''
    df = pd.DataFrame()
    for i, item in enumerate(materials['components']):
        if 'text' in item and 'value' in item['text']:
            if ('typography' in item['text'] and 
                item['text']['typography'] in ['heading-s', 'heading-xs']):
                attribute_name = item['text']['value']
                if attribute_name not in list(df.columns):
                    list(df.columns).append(attribute_name)
            else:
                attribute_value = item['text']['value']
                df[attribute_name] = attribute_value


def extract_origin():
    pass

date = '2023-07-22'
def organise_product_details():
    product_details = get_bucket_file(f'{date}-product_details.json')
    product = []
    care = []
    certified_materials = []
    materials = []
    origin = []

    for product_id in product_details:
        extracted_details = extract_product_details(product_details, product_id)
        

        # extracted_care = extract_care(extracted_details[1])
        # care.append(extracted_care)

        # extracted_certified_materials = extract_certified_materials(extracted_details[2])
        # certified_materials.append(extracted_certified_materials)

        extracted_materials = extract_materials(extracted_details[3])
        print(extracted_materials)
        # materials.append(extracted_materials)

        # extracted_origin = extract_origin(extracted_details[4])
        # origin.append(extracted_origin)

    # return materials

organise_product_details()
# print(organised_product_details)


