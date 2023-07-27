import get_zara
import etl_zara
from s3_bucket import upload_json_to_bucket
from logger import setup_logger
from helpers import date, csv_path
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
    for product_id in product_ids['product_ids'][:5]:
        try:
            product_details[product_id] = get_zara.get_product_details(product_id)
        except Exception as e:
            logger.error(e)
            continue
        upload_json_to_bucket(product_details, f'{date}-product_details.json')

    related_products = {}
    for product_id in product_ids['product_ids'][:5]:
        try:
            related_products[product_id] = get_zara.get_related_products(product_id)
        except Exception as e:
            logger.error(e)
            continue
        upload_json_to_bucket(related_products, f'{date}-related_products.json')

def etl_zara_data_and_upload_to_db():
    '''Executes the zara ETL Script functions from the file etl_zara.py and
    saves the data to the RDS database'''

    products_by_cat, products, product_availability, color_interp = etl_zara.transform_product_data()
    target_groups, categories, categories_by_target_groups = etl_zara.normalize_categories()
    materials, origins = etl_zara.organise_product_details()
    related_products = etl_zara.normalize_related_products()

    # products
    try:
        copy_csv_to_db(
            products,
            f'{csv_path}products.csv',
            pk_columns='retrieved_on, src, product_id'
            )
    except Exception as e:
        logger.warning(e)
    
    #target_groups
    try:
        copy_csv_to_db(
            target_groups,
            f'{csv_path}target_groups.csv',
            pk_columns='src, target_group_id'
            )
    except Exception as e:
        logger.warning(e)
    
    #categories
    try:
        copy_csv_to_db(
            categories,
            f'{csv_path}categories.csv',
            pk_columns='src, category_id'
            )
    except Exception as e:
        logger.warning(e)
    
    #materials
    try:
        copy_csv_to_db(
            materials,
            f'{csv_path}materials.csv',
            pk_columns='retrieved_on, src, product_id, material_part, perc, material'
            )
    except Exception as e:
        logger.warning(e)

    #origins
    try:
        copy_csv_to_db(
            origins,
            f'{csv_path}origins.csv',
            pk_columns='retrieved_on, src, product_id, country_of_origin'
            )

    except Exception as e:
        logger.warning(e)

    #related products
    try:
        copy_csv_to_db(
            related_products,
            f'{csv_path}related_products.csv',
            pk_columns='src, product_id , related_product_id'
            )
    except Exception as e:
        logger.warning(e)
    
    #categories by target groups
    try:
        copy_csv_to_db(
            categories_by_target_groups,
            f'{csv_path}categories_by_target_groups.csv',
            pk_columns='src, target_group_id , category_id'
            )
    except Exception as e:
        logger.warning(e)
    
    #products by categories
    try:
        copy_csv_to_db(
            products_by_cat,
            f'{csv_path}products_by_categories.csv',
            pk_columns='src, category_id , product_id'
            )
    except Exception as e:
        logger.warning(e)

    #product availability
    try:
        copy_csv_to_db(
            product_availability,
            f'{csv_path}product_availability.csv',
            pk_columns='retrieved_on, src, product_id'
            )
    except Exception as e:
        logger.warning(e)
    
    #color interpretations
    try:
        copy_csv_to_db(
            color_interp,
            f'{csv_path}color_interpretations.csv',
            pk_columns='hex_color, interpret_zara_com_de'
            )
    except Exception as e:
        logger.warning(e)
   

if __name__ == "__main__":
    # get_zara_data_and_upload_to_s3_bucket()
    etl_zara_data_and_upload_to_db()