from datetime import datetime
import pandas as pd

# from postgres_connection import connect_to_db, disconnect_from_db
from s3_bucket import *
from get_zara import extract_products
from logger import setup_logger

logger = setup_logger()

# date = datetime.now().strftime('%Y-%m-%d')
date = '2023-07-22'

def normalize_related_products(json):
    result = []
    for key, values in json.items():
        for value in values:
            result.append((key, value))
    return result

def normalize_products_by_categories(json):
    pass

def products_to_df(list_of_products):
    '''docstring here'''
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

def extract_materials(materials, product_id):
    '''docstring here'''
    material_list = []
    attribute_name = None
    ignore = ['COMPOSITION', 'Which contains at least:']
    for item in materials['components']:
        if 'text' in item and 'value' in item['text']:
            if ('typography' in item['text'] and 
                item['text']['typography'] in ['heading-s', 'heading-xs']):
                attribute_name = item['text']['value']
                if attribute_name in ignore:
                    attribute_name = None
                    continue
            elif attribute_name is not None:
                attribute_value = item['text']['value']
                if attribute_value not in ignore:
                    if '<br>' in attribute_value:
                        attribute_value = attribute_value.split('<br>')
                        for item in attribute_value:
                            m = item.split('%')
                            percentage = f'{m[0]}%'
                            material = m[1]
                            material_list.append({
                                'product_id': product_id,
                                'material_part': attribute_name,
                                'percentage': percentage,
                                'material': material
                                })
                    else:
                        attribute_value = attribute_value.split('%')
                        percentage = f'{attribute_value[0]}%'
                        material = attribute_value[1]
                        # add a new row for each material
                        material_list.append({
                            'product_id': product_id,
                            'material_part': attribute_name,
                            'percentage': percentage,
                            'material': material
                            })

    return material_list

def extract_origin(origin, product_id):
    '''docstring here'''
    origin_list = []
    country_of_origin = origin['components'][-1]['text']['value']
    country_of_origin= country_of_origin.split('Made in')[1]
    origin_list.append({
                        'product_id': product_id,
                        'country_of_origin': country_of_origin
                        })
    return origin_list
    
def detail_to_df(detail):
    '''docstring here'''
    detail = [item for sublist in detail for item in sublist]
    df_detail = pd.DataFrame(detail)
    return df_detail

def organise_product_details():
    '''docstring here'''
    product_details = get_bucket_file(f'{date}-product_details.json')
    materials = []
    origin = []

    for product_id in product_details:
        extracted_details = extract_product_details(product_details, product_id)
        try:
            extracted_materials = extract_materials(extracted_details[3], product_id)
            materials.append(extracted_materials)
        except Exception as e:
            logger.error(e)

        try:
            extracted_origin = extract_origin(extracted_details[4], product_id)
            origin.append(extracted_origin)
        except Exception as e:
            logger.error(e)

    materials = detail_to_df(materials)
    origin = detail_to_df(origin)

    return materials, origin

materials, origin = organise_product_details()
print(materials)
print(origin)


