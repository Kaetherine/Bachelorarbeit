from postgres_connection import connect_to_db, disconnect_from_db
from to_s3_bucket import s3_client

# List all objects in your bucket
response = s3_client.list_objects(Bucket='your_bucket_name')
print(response)

# for obj in response['Contents']:
#     print(obj['Key'])

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