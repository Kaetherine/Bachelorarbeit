from datetime import datetime
import pandas as pd

# from postgres_connection import connect_to_db, disconnect_from_db
from s3_bucket import *
from get_zara import extract_products
from logger import setup_logger

logger = setup_logger()
date = datetime.now().strftime('%Y-%m-%d')

def normalize_related_products():
    '''docstring here'''
    related_products_dict = get_bucket_file(f'{date}-related_products.json')
    data = []
    for product, products in related_products_dict.items():
        for related_product in products:
            data.append({
                "product_id": product,
                "related_product_id": related_product
            })
    related_products = pd.DataFrame(data)
    return related_products

def normalize_target_groups(categories_dict):
    target_groups = []
    for item in categories_dict:
        target_group = item['name']
        target_group_id = item['id']
        if (target_group == 'WOMAN' or target_group == 'MAN' or target_group == 'KIDS'):
            target_groups.append({
                'target_group_id': target_group_id,
                'target_group': target_group
            })
    target_groups = pd.DataFrame(target_groups)
    return target_groups
            

def normalize_categories():
    categories_dict = get_bucket_file(f'{date}-categories.json')
    categories_dict = categories_dict['categories']
    target_groups = normalize_target_groups(categories_dict)
    # categories = []

    # for item in categories_dict:
    #     target_group = item['name']
    #     target_group_id = item['id']
    #     if (target_group == 'WOMAN' or target_group == 'MAN' or target_group == 'KIDS'):
    #         categories['target_group'] = target_group
        
    #         subcategories_1 = item['subcategories']
    #         for item in subcategories_1:
    #             if 'name' in item:
    #                 categories['name_1'] = item['name']
    #             if 'id' in item:
    #                 categories['id_1'] = item['id']
                
    #             if 'subcategories' in item:
    #                 subcategories_2 = item['subcategories']
    #                 for item in subcategories_2:
    #                     if 'name' in item:
    #                         categories['name_2'] = item['name']
    #                     if 'id' in item:
    #                         categories['id_2'] = item['id']
    # return categories
    return target_groups

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

def normalize_materials(materials, product_id):
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
                        material_list.append({
                            'product_id': product_id,
                            'material_part': attribute_name,
                            'percentage': percentage,
                            'material': material
                            })
    return material_list

def normalize_origin(origin, product_id):
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
        extracted_details = extract_product_details(
            product_details,
            product_id
            )
        try:
            normalized_materials = normalize_materials(
                extracted_details[3],
                product_id
                )
            materials.append(normalized_materials)
        except Exception as e:
            logger.error(e)

        try:
            normalized_origin = normalize_origin(
                extracted_details[4],
                product_id
                )
            origin.append(normalized_origin)
        except Exception as e:
            logger.error(e)

    materials = detail_to_df(materials)
    origin = detail_to_df(origin)

    return materials, origin

# materials, origin = organise_product_details()
# related_products = normalize_related_products()
categories = normalize_categories()
print(categories)



