import get_zara as zara
from to_s3_bucket import upload_json_to_bucket
from datetime import datetime

date = datetime.now()

def get_zara_data_and_upload():
    category_ids = zara.get_categories()
    products_by_category = zara.get_product_list(category_ids[14:18])
    product_ids = zara.get_product_ids(products_by_category)
    product_details = zara.get_product_details(product_ids[14:18])
    related_products = zara.get_related_products(product_ids[14:18])

    # saving data to s3bucket
    upload_json_to_bucket(category_ids, f'{date}-category_ids.json')
    upload_json_to_bucket(products_by_category, f'{date}-products_by_category.json')
    upload_json_to_bucket(product_ids, f'{date}-product_ids.json')
    upload_json_to_bucket(product_details, f'{date}-product_details.json')
    upload_json_to_bucket(related_products, f'{date}-related_products.json')


if __name__ == "__main__":
    get_zara_data_and_upload()