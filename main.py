import get_zara
import etl_zara
from s3_bucket import upload_json_to_bucket
from logger import setup_logger
from helper_functions import date
from postgres_db import copy_csv_to_db

logger = setup_logger()

def get_zara_data_and_upload_to_s3_bucket():
    '''Executes the zara API Client functions from the file get_zara.py and
    saves the json data to the s3 bucket'''
    try:
        categories = get_zara.get_categories()
    except Exception as e:
        logger.error(e)
    if categories:
        upload_json_to_bucket(categories, f'{date}-categories.json')

    category_ids = get_zara.extract_category_ids(categories)
    upload_json_to_bucket(category_ids, f'{date}-category_ids.json')

    products_by_category = {}
    for category_id in category_ids['category_ids'][38:40]:
        try:
            products_by_category[category_id] = get_zara.get_product_list(category_id)
        except Exception as e:
            logger.error(e)
            continue
        upload_json_to_bucket(products_by_category, f'{date}-products_by_category.json')

    products = get_zara.extract_products(products_by_category)
    upload_json_to_bucket(products, f'{date}-products.json')

    product_ids = get_zara.extract_product_ids(products_by_category)
    upload_json_to_bucket(product_ids, f'{date}-product_ids.json')

    product_details = {}
    for product_id in product_ids['product_ids'][1:3]:
        try:
            product_details[product_id] = get_zara.get_product_details(product_id)
        except Exception as e:
            logger.error(e)
            continue
        upload_json_to_bucket(product_details, f'{date}-product_details.json')

    related_products = {}
    for product_id in product_ids['product_ids'][1:3]:
        try:
            related_products[product_id] = get_zara.get_related_products(product_id)
        except Exception as e:
            logger.error(e)
            continue
        upload_json_to_bucket(related_products, f'{date}-related_products.json')

def etl_zara_data_and_upload_to_db():
    '''Executes the zara ETL Script functions from the file etl_zara.py and
    saves the data to the RDS database'''
    path = '/home/katherine/Development/Bachelorarbeit/'

    materials, origins = etl_zara.organise_product_details()
    copy_csv_to_db(materials, f'{path}materials.csv', 'materials')
    copy_csv_to_db(origins, f'{path}origins.csv', 'origins')

    related_products = etl_zara.normalize_related_products()
    copy_csv_to_db(related_products, f'{path}related_products.csv', 'related_products')

    target_groups, categories, target_groups_by_categories = etl_zara.normalize_categories()
    copy_csv_to_db(target_groups, f'{path}target_groups.csv', 'target_groups')
    copy_csv_to_db(categories, f'{path}categories.csv', 'categories')
    copy_csv_to_db(
        target_groups_by_categories,
        f'{path}target_groups_by_categories.csv',
        'target_groups_by_categories'
        )
    
    products_by_cat, products, availability, color_interp = etl_zara.transform_product_data()
    copy_csv_to_db(products_by_cat, f'{path}products_by_categories.csv', 'products_by_categories')
    copy_csv_to_db(products, f'{path}products.csv', 'products')
    copy_csv_to_db(availability, f'{path}availability.csv', 'availability')
    copy_csv_to_db(color_interp, f'{path}color_interpretations.csv', 'color_interpretations')

if __name__ == "__main__":
    get_zara_data_and_upload_to_s3_bucket()
    etl_zara_data_and_upload_to_db()