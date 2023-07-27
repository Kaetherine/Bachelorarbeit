from s3_bucket import *
from logger import setup_logger
from helper_functions import convert_date, date

logger = setup_logger()

def normalize_related_products():
    '''Creates a list of tuples of related products.'''
    related_products_tup = get_bucket_file(f'{date}-related_products.json')
    data = []
    for product, products in related_products_tup.items():
        if products:
            for related_product in products:
                data.append(('zara.com/de', product, related_product))
 
    return related_product
            
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
        categories.append((
            'zara.com/de', subcategory_id, subcategory_name, age_range
            ))
        
    return categories

def normalize_categories():
    '''Normalize categories data obtained from the "categories.json" file.'''
    categories_tup = get_bucket_file(f'{date}-categories.json')
    categories_tup = categories_tup['categories']

    # normalizing target_groups
    categories = []
    target_groups = []
    desired_target_groups = ['WOMAN', 'MAN', 'KIDS']
    categories_by_target_group = []

    for entry in categories_tup:
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
            logger.warning(e)

        # normalize categories by target_groups
        # print(entry, value)
        temp = (
         ('zara.com/de', entry['id'], value) for value in categories_0)
        categories_by_target_group.append(temp)
    
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

def create_material_tup(product_id, attribute_name, attribute_value):
    '''Extracts the percage and material type from a given string and 
    returns a tuple with the information.'''
    m = attribute_value.split('%')
    percage = f'{m[0]}%'
    material = m[1]

    return (date,'zara.com/de', product_id, attribute_name, percage, material)

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
                            material_tup = create_material_tup(
                                product_id, attribute_name, value
                                )
                            material_list.append(material_tup)
                    else:
                        material_tup = create_material_tup(
                            product_id, attribute_name, attribute_value
                            )
                        material_list.append(material_tup)

    return material_list

def normalize_origin(origin, product_id):
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
        try:
            extracted_details = extract_product_details(
                product_details,
                product_id
                )
        except Exception as e:
            logger.warning(product_id, e)
        try:
            normalized_materials = normalize_materials(
                extracted_details[3],
                product_id
                )
            materials.extend(normalized_materials)
        except Exception as e:
            logger.error(product_id, e)

        try:
            normalized_origin = normalize_origin(
                extracted_details[4],
                product_id
                )
            origin.extend(normalized_origin)
        except Exception as e:
            logger.error(product_id, e)

    return materials, origin

def create_product_tup(entry):
    '''Generates and returns a product tuple from a provided entry.'''
    product_id = entry['id']
    color_hex_code = entry.get('colorInfo', {}).get('mainColorHexCode')
    
    return (
        date, 'zara.com/de',  product_id, entry['name'], 
        float(entry['price']/100), 'EUR',
        convert_date(entry['startDate']), color_hex_code,
    )

def create_availability_tup(entry):
    '''Generates and returns a tuple containing product availability from a 
    provided entry.'''
    return (date, 'zara.com/de', entry['id'], entry['availability'])

def create_color_interpretation_tup(color_hex_code, color_interpretation):
    '''Generates and returns a tuple containing color interpretation for a 
    given product entry.'''

    return (color_hex_code, color_interpretation)

def transform_product_data():
    '''Extracts product data from a JSON file, transforms it, and returns it 
    as four Pandas DataFrames.'''
    products_by_category_tup = get_bucket_file(
        f'{date}-products_by_category.json'
        )
    products_by_category = []
    products = []
    availability = []
    color_interpretations = []
    
    for category in products_by_category_tup:
        for item in products_by_category_tup[category]:
            for entry in item:

                try:
                    product_tup = create_product_tup(entry)
                    products.append(product_tup)
                except Exception as e:
                    logger.warning(e)

                try:
                    availability_tup = create_availability_tup(entry)
                    availability.append(availability_tup)
                except Exception as e:
                    logger.warning(e)

                try:
                    color_interpretation_tup = create_color_interpretation_tup(
                        product_tup['color_hex_code'],
                        product_tup['color_interpretation']
                        )
                    color_interpretations.append(color_interpretation_tup)
                except Exception as e:
                    logger.warning(e)

                products_by_category.append((
                    'zara.com/de', category, product_tup[2])
                    )
    
    return products_by_category, products, availability, color_interpretations


# materials, origin = organise_product_details()
# related_products = normalize_related_products()
# target_groups, categories, categories_by_target_group = normalize_categories()
# products_by_category, products, availability, color_interpretations = transform_product_data()

# print(materials,'\n','\n',origin,'\n','\n',related_products,'\n','\n',target_groups,'\n','\n',categories,'\n','\n',categories_by_target_group,
# products_by_category,'\n','\n',products,'\n','\n',availability,'\n','\n',color_interpretations)