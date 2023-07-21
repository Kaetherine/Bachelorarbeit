from datetime import datetime

import get_zara as zara
from to_s3_bucket import upload_json_to_bucket
from logger import setup_logger

logger = setup_logger()
date = datetime.now().strftime('%Y-%m-%d')

def get_zara_data_and_upload():
    '''docstring here'''
    category_ids = zara.get_categories()
    upload_json_to_bucket(category_ids, f'{date}-category_ids.json')

    products_by_category = {}
    for category_id in category_ids[23:26]:
        try:
            products_by_category[category_id] = zara.get_product_list(category_id['category_ids'])
        except Exception as e:
            logger.error(e)
            continue
        upload_json_to_bucket(products_by_category, f'{date}-products_by_category.json')

    product_ids = zara.get_product_ids(products_by_category)
    upload_json_to_bucket(product_ids, f'{date}-product_ids.json')

    for product in product_details:
        try:
            product_details = zara.get_product_details(product['product_ids'][23:26])
            upload_json_to_bucket(product_details, f'{date}-product_details.json')
        except Exception as e:
            logger.error(e)
            continue

    for product in related_products:
        try:
            related_products = zara.get_related_products(product['product_ids'][23:26])
            upload_json_to_bucket(related_products, f'{date}-related_products.json')
        except Exception as e:
            logger.error(e)
            continue


if __name__ == "__main__":
    get_zara_data_and_upload()