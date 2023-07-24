import get_zara as zara
from s3_bucket import upload_json_to_bucket
from logger import setup_logger
from helper_functions import date

logger = setup_logger()

def get_zara_data_and_upload():
    '''docstring here'''
    try:
        categories = zara.get_categories()
    except Exception as e:
        logger.error(e)
    if categories:
        upload_json_to_bucket(categories, f'{date}-categories.json')

    category_ids = zara.extract_category_ids(categories)
    upload_json_to_bucket(category_ids, f'{date}-category_ids.json')

    products_by_category = {}
    for category_id in category_ids['category_ids'][38:40]:
        try:
            products_by_category[category_id] = zara.get_product_list(category_id)
        except Exception as e:
            logger.error(e)
            continue
        upload_json_to_bucket(products_by_category, f'{date}-products_by_category.json')

    products = zara.extract_products(products_by_category)
    upload_json_to_bucket(products, f'{date}-products.json')

    product_ids = zara.extract_product_ids(products_by_category)
    upload_json_to_bucket(product_ids, f'{date}-product_ids.json')

    product_details = {}
    for product_id in product_ids['product_ids'][1:3]:
        try:
            product_details[product_id] = zara.get_product_details(product_id)
        except Exception as e:
            logger.error(e)
            continue
        upload_json_to_bucket(product_details, f'{date}-product_details.json')

    related_products = {}
    for product_id in product_ids['product_ids'][1:3]:
        try:
            related_products[product_id] = zara.get_related_products(product_id)
        except Exception as e:
            logger.error(e)
            continue
        upload_json_to_bucket(related_products, f'{date}-related_products.json')


if __name__ == "__main__":
    get_zara_data_and_upload()