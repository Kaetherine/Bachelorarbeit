from postgres_connection import connect_to_db, disconnect_from_db
from s3_bucket import *


def normalize_related_products(data):
    result = []
    for key, values in data.items():
        for value in values:
            result.append((key, value))
    return result


related_products = get_bucket_file('raw-apparel-marketdata', '2023-07-21-related_products.json')
print(related_products)

normalized_data = normalize_related_products(related_products)
print(normalized_data)



# # Delete a specific file
# s3_client.delete_object(Bucket='your_bucket_name', Key='your_file_key')


def product_details(json):
    pass
    '''doctstring here'''
        # filter content
    # product_details = {}
    # if response:
    #     for detail in response:
    #         product_details[product_id] = {}
    #         if detail['sectionType'] == 'materials':
    #             product_details[product_id]['materials'] = detail
    #         elif detail['sectionType'] == 'certifiedMaterials':
    #             product_details[product_id]['certifiedmaterials'] = detail
    #         elif detail['sectionType'] == 'origin':
    #             product_details[product_id]['origin'] = detail
    #     if 'certifiedmaterials' not in product_details[product_id]:
    #         product_details[product_id]['certifiedmaterials'] = None
    # return product_details