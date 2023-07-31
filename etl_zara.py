from helpers import convert_date, date
from logger import setup_logger
from s3_bucket import *

import traceback

logger = setup_logger()

def normalize_related_products():
    '''Creates a list of tuples of related products.'''
    related_products_tuple = get_bucket_file(f'{date}-related_products.json')
    related_products = []
    for product, products in related_products_tuple.items():
        if products:
            for related_product in products:
                related_products.append(('zara.com/de', product, related_product))
 
    return related_products
            
def extract_subcategories(subcategories):
    '''Extracts relevant subcategories from a list of subcategories.'''
    ignore_ids = [
        '194501' , '2118764', 
        '2292949', '2292271', 
        '1950810', '1890848',
        '2307636', '2307635',
        '2307136',
        ]
    ignore_names = ['DISCOVER', 'JOIN LIFE', 'CAREERS']
    categories = []
    for subcategory in subcategories:
        subcategory_name = subcategory['name']
        subcategory_id = str(subcategory['id'])
        age_range = 'Not specified'
        if subcategory_id in ignore_ids:
            continue
        elif 'DIVIDER' in subcategory_name or subcategory_name in ignore_names:
            continue
        elif '|' in subcategory_name:
            if ('BABY' in subcategory_name or 'GIRL' in subcategory_name 
            or 'BOY' in subcategory_name):
                transform_cat = subcategory_name.split('|')
                subcategory_name = transform_cat[1]
                age_range = transform_cat[0]
            else:
                subcategory_name = subcategory_name.replace('|', 'AND')
        cat = ('zara.com/de', subcategory_id, subcategory_name, age_range)
        categories.append(cat)
        
    return categories

def normalize_categories():
    '''Normalize categories data obtained from the "categories.json" file.'''
    categories_tuple = get_bucket_file(f'{date}-categories.json')
    categories_tuple = categories_tuple['categories']

    # normalizing target_groups
    categories = []
    target_groups = []
    desired_target_groups = ['WOMAN', 'MAN', 'KIDS']
    categories_by_target_groups = []

    for entry in categories_tuple:
        target_group = entry['name']
        target_group_id = entry['id']
        if target_group in desired_target_groups:
            target_groups.append((
                'zara.com/de', str(target_group_id), target_group
            ))
            
            # normalizing subcategories
            try:
                categories_0 = extract_subcategories(entry['subcategories'])
                categories.extend(categories_0)
            except Exception as e:
                logger.warning(f'{e}: {traceback.format_exc()}')

            for tup in categories_0:
                category_id = tup[1]
                categories_by_target_groups.append(
                    ('zara.com/de', target_group_id, category_id)
                    )
    
    return target_groups, categories, categories_by_target_groups

def extract_product_details(product_details, product_id):
    '''Extracts care, certified materials, materials, and 
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

def create_material_tuple(product_id, material_part, material_info):
    '''Extracts the percage and material type from a given string and 
    returns a tuple with the information.'''
    if material_part == 'MAIN FABRIC':
        material_part = 'OUTER SHELL'
    material_info = material_info.split('%')
    percent = f'{material_info[0]}'
    material = material_info[1]
    if ':' in percent:
        garment_piece_and_percentage = percent.split(':')
        garment_piece = garment_piece_and_percentage[0]
        percent = garment_piece_and_percentage[1]
    else:
        garment_piece = 'Not specified'

    return (date,'zara.com/de', product_id, garment_piece, material_part, percent, material)

def search_duplicates_in_materials(tuple_list_with_duplicates):
    '''Searches for duplicate elements at a specific index in the tuples of a list.'''
    elements_at_i = [str(item[2]) for item in tuple_list_with_duplicates]
    elements = []
    duplicates = []
    for item in elements_at_i:
        item = str(item)
        if item not in elements:
            elements.append(item)
            elements = list(set(elements))
        else:
            duplicates.append(item)
            duplicates = list(set(duplicates))

    return duplicates


def correct_values_in_material_tuples(tuple_list_with_incorrect_values, material_name, duplicates):
    '''Corrects the percentage values in tuples based on the duplicates and given material name.'''
    corrected_list = []
    for tup in tuple_list_with_incorrect_values:
        if tup[3] in duplicates:
            certified_material_tuple = None
            non_certified_material_tuple = None
            if material_name in tup[6]:
                certified_material_tuple = tup
            else:
                non_certified_material_tuple = tup

            if certified_material_tuple and non_certified_material_tuple:
                corrected_percentage = non_certified_material_tuple[5] - certified_material_tuple[5]
                corrected_tuple = tuple(
                    non_certified_material_tuple[:5] + (corrected_percentage,) + non_certified_material_tuple[6:]
                )
                corrected_list.append(corrected_tuple)
                corrected_list.append(certified_material_tuple)
            else:
                corrected_list.append(tup)
        else:
            corrected_list.append(tup)

    return corrected_list


def normalize_materials(materials, product_id):
    '''Normalize the materials data and extract relevant information.'''
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
                        attribute_values = attribute_value.split('<br>')
                        for value in attribute_values:
                            material_tuple = create_material_tuple(
                                product_id, attribute_name, value
                                )
                            material_list.append(material_tuple)
                    else:
                        material_tuple = create_material_tuple(
                            product_id, attribute_name, attribute_value
                            )
                        material_list.append(material_tuple)
                        
    return material_list

def normalize_origins(origin, product_id):
    '''Normalize the origin data and extract relevant information.'''
    origin_list = []
    country_of_origin = origin['components'][-1]['text']['value']
    country_of_origin= country_of_origin.split('Made in')[1]
    origin_list.append((date, 'zara.com/de', product_id, country_of_origin))
    return origin_list

def organise_product_details():
    '''Organize product details data by normalizing materials 
    and origin information.'''
    product_details = get_bucket_file(f'{date}-product_details.json')
    materials = []
    origin = []

    for product_id in product_details:
        logger.info(product_id)
        try:
            extracted_details = extract_product_details(
                product_details,
                product_id
                )
        except Exception as e:
            logger.warning(f'{e}: {traceback.format_exc()}')
            continue
        try:
            normalized_materials = normalize_materials(
                extracted_details[3],
                product_id
                )
            materials.extend(normalized_materials)
        except Exception as e:
            logger.warning(f'{e}: {traceback.format_exc()}')

        try:
            normalized_origin = normalize_origins(
                extracted_details[4],
                product_id
                )
            origin.extend(normalized_origin)
        except Exception as e:
            logger.warning(f'{e}: {traceback.format_exc()}')

    print(len(materials))
    duplicates = search_duplicates_in_materials(materials)
    materials = correct_values_in_material_tuples(materials, 'cotton', duplicates)
    materials = correct_values_in_material_tuples(materials, 'polyester', duplicates)
    print(len(materials))
    # print(materials)

    return materials, origin

def create_product_tuple(entry):
    '''Generates and returns a product tuple from a provided entry.'''
    product_id = entry['id']
    color_hex_code = entry.get('colorInfo', {}).get('mainColorHexCode')
    if not color_hex_code:
        color_hex_code = 'Not specified'
    return (
        date, 'zara.com/de',  product_id, entry['name'], 
        float(entry['price']/100), 'EUR',
        convert_date(entry['startDate']), color_hex_code,
    )

def create_availability_tuple(entry):
    '''Generates and returns a tuple containing product product_availability from a 
    provided entry.'''
    return (date, 'zara.com/de', entry['id'], entry['availability'])

def create_color_interpretation_tuple(entry, hex_code):
    '''Gets the color name and returns it together with the hex code in a tuple'''
    try:
        color_interpretation = entry['detail']['colors'][0]['name']
    except:
        color_interpretation = 'Not specified'
    
    color_interpretation_tuple = (hex_code, color_interpretation)

    return color_interpretation_tuple

def transform_product_data():
    '''Extracts product data from a JSON file, transforms it, and returns it 
    as four Pandas DataFrames.'''
    products_by_category_tuple = get_bucket_file(
        f'{date}-products_by_category.json'
        )
    products_by_category = []
    products = []
    product_availability = []
    color_interpretations = []
    
    for category in products_by_category_tuple:
        for item in products_by_category_tuple[category]:
            for entry in item:

                try:
                    product_tuple = create_product_tuple(entry)
                    products.append(product_tuple)
                except Exception as e:
                    logger.warning(f'{e}: {traceback.format_exc()}')

                try:
                    availability_tuple = create_availability_tuple(entry)
                    product_availability.append(availability_tuple)
                except Exception as e:
                    logger.warning(f'{e}: {traceback.format_exc()}')
                
                if '#' not in product_tuple[-1]:
                    continue
                else:
                    try:
                        color_interpretation_tuple = create_color_interpretation_tuple(entry, product_tuple[-1])
                        color_interpretations.append(color_interpretation_tuple)
                    except Exception as e:
                        logger.warning(f'{e}: {traceback.format_exc()}')

                products_by_category.append((
                    'zara.com/de', category, product_tuple[2])
                    )
    
    return products_by_category, products, product_availability, color_interpretations