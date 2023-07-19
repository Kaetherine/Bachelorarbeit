import get_zara as zara
from to_s3_bucket import upload_json_to_bucket

def get_zara_data_and_upload():
    category_ids = zara.get_categories()
    products_by_category = zara.get_product_list(category_ids[14:18])
    product_ids = zara.get_product_ids(products_by_category)
    product_details = zara.get_product_details(product_ids[14:18])
    related_products = zara.get_related_products(product_ids[14:18])


    '''executes all functions to get the content of zara'''
    # print(category_ids)
    # print(category_ids[14:18])
    # print(products_by_category)
    # print(len(products_by_category))
    # print(product_ids)
    # print(product_details)
    # print(len(product_details))
    # print(related_products)


    # saving data to s3bucket
    upload_json_to_bucket(category_ids, 'category_ids.json')
    upload_json_to_bucket(products_by_category, 'products_by_category.json')
    upload_json_to_bucket(product_ids, 'product_ids.json')
    upload_json_to_bucket(product_details, 'product_details.json')
    upload_json_to_bucket(related_products, 'related_products.json')


if __name__ == "__main__":
    get_zara_data_and_upload()