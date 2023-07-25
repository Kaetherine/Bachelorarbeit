import pandas as pd

from s3_bucket import *
from logger import setup_logger
from helper_functions import convert_date, flatten_and_convert_to_df, date

logger = setup_logger()

def normalize_related_products():
    '''Creates a normalized DataFrame from a dictionary of related 
    products.'''
    related_products_dict = get_bucket_file(f'{date}-related_products.json')
    data = []
    for product, products in related_products_dict.items():
        for related_product in products:
            data.append({
                'source': 'zara.com/de',
                'product_id': product,
                'related_product_id': related_product
            })
    related_products = pd.DataFrame(data)
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
        age_range = None
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
        categories.append({
            'source': 'zara.com/de',
            'category_id': subcategory_id,
            'category_name': subcategory_name,
            'age_range': age_range
            })
    return categories

def normalize_categories():
    '''Normalize categories data obtained from the "categories.json" file.'''
    categories_dict = get_bucket_file(f'{date}-categories.json')
    categories_dict = categories_dict['categories']

    # normalizing target_groups
    categories = []
    target_groups = []
    desired_target_groups = ['WOMAN', 'MAN', 'KIDS']
    categories_by_target_group = []

    for entry in categories_dict:
        target_group = entry['name']
        target_group_id = entry['id']
        if target_group in desired_target_groups:
            target_groups.append({
                'source': 'zara.com/de',
                'target_group_id': str(target_group_id),
                'target_group': target_group
                })
            
        # normalizing subcategories
        try:
            categories_0 = extract_subcategories(entry['subcategories'])
            categories.extend(categories_0)
        except Exception as e:
            logger.warning(e)

        # normalize categories by target_groups
        temp = [{
                'source': 'zara.com/de',
                'target_group': entry['id'],
                'category_id': value['category_id']
                } for value in categories_0
            ]
        categories_by_target_group.append(temp)

    categories_by_target_group = flatten_and_convert_to_df(
        categories_by_target_group
        )
    target_groups = pd.DataFrame(target_groups)
    categories = pd.DataFrame(categories)

    return target_groups, categories, categories_by_target_group

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

def create_material_dict(product_id, attribute_name, attribute_value):
    '''Extracts the percentage and material type from a given string and 
    returns a dictionary with the information.'''
    m = attribute_value.split('%')
    percentage = f'{m[0]}%'
    material = m[1]
    return {
        'source': 'zara.com/de',
        'product_id': product_id,
        'material_part': attribute_name,
        'percentage': percentage,
        'material': material
    }

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
                            material_dict = create_material_dict(
                                product_id, attribute_name, value
                                )
                            material_list.append(material_dict)
                    else:
                        material_dict = create_material_dict(
                            product_id, attribute_name, attribute_value
                            )
                        material_list.append(material_dict)

    return material_list

def normalize_origin(origin, product_id):
    '''Normalize the origin data and extract relevant information.'''
    origin_list = []
    country_of_origin = origin['components'][-1]['text']['value']
    country_of_origin= country_of_origin.split('Made in')[1]
    origin_list.append({
            'source': 'zara.com/de',
            'product_id': product_id,
            'country_of_origin': country_of_origin
            })
    return origin_list

def organise_product_details():
    '''Organize product details data by normalizing materials 
    and origin information.'''
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

    materials = flatten_and_convert_to_df(materials)
    origin = flatten_and_convert_to_df(origin)

    return materials, origin

def create_product_dict(entry):
    '''Generates and returns a product dictionary from a provided entry.'''
    product_id = entry['id']
    color_interpretation = entry['detail']['colors'][0]['name']
    color_hex_code = entry.get('colorInfo', {}).get('mainColorHexCode')
    
    return {
        'source': 'zara.com/de',
        'product_id': product_id,
        'name':entry['name'],
        'price':float(entry['price']/100),
        'publish_date':convert_date(entry['startDate']),
        'color_hex_code':color_hex_code,
        'color_interpretation':color_interpretation
    }

def create_availability_dict(entry):
    '''Generates and returns a dictionary containing product availability from a 
    provided entry.'''
    return {
        'source': 'zara.com/de',
        'product_id': entry['id'],
        'availability':entry['availability']
    }

def create_color_interpretation_dict(color_hex_code, color_interpretation):
    '''Generates and returns a dictionary containing color interpretation for a 
    given product entry.'''
    return {
        'color_hex_code':color_hex_code,
        'zara.com/de':color_interpretation
    }

def transform_product_data():
    '''Extracts product data from a JSON file, transforms it, and returns it 
    as four Pandas DataFrames.'''
    products_by_category_dict = get_bucket_file(
        f'{date}-products_by_category.json'
        )
    products_by_category = []
    products = []
    availability = []
    color_interpretations = []
    
    for category in products_by_category_dict:
        for item in products_by_category_dict[category]:
            for entry in item:

                try:
                    product_dict = create_product_dict(entry)
                    products.append(product_dict)
                except Exception as e:
                    logger.warning(e)

                try:
                    availability_dict = create_availability_dict(entry)
                    availability.append(availability_dict)
                except Exception as e:
                    logger.warning(e)

                try:
                    color_interpretation_dict = create_color_interpretation_dict(
                        product_dict['color_hex_code'],
                        product_dict['color_interpretation']
                        )
                    color_interpretations.append(color_interpretation_dict)
                except Exception as e:
                    logger.warning(e)
                
                products_by_category.append({
                    'source': 'zara.com/de',
                    'category_id': category,
                    'product_id': product_dict['product_id']
                })
    
    products_by_category = pd.DataFrame(products_by_category)
    products = pd.DataFrame(products)
    availability = pd.DataFrame(availability)
    color_interpretations = pd.DataFrame(color_interpretations)
    
    return products_by_category, products, availability, color_interpretations


def augment_color_hex_codes():
    pass


x, y = organise_product_details()
print(x, '\n', y)

rel_prod = normalize_related_products()
print(rel_prod, '\n')

target_groups, categories, categories_by_target_group = normalize_categories()
print(target_groups,'\n', categories,'\n', categories_by_target_group)

products_by_category, products, availability, color_interpretations = transform_product_data()
print(products_by_category,'\n', products,'\n', availability,'\n', color_interpretations)