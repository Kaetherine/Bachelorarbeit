import boto3
from credentials import aws_access_key, aws_secret_access_key, aws_bucket, aws_region
import json

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

def data_to_byte(data):
    '''converst json to bytestream'''
    data_byte_stream = bytes(json.dumps(data).encode('UTF-8'))
    return data_byte_stream

def upload_json_to_bucket(filename, data, bucket=aws_bucket, ):
    '''converts json to bytestream and uploads it to the specified 
    (projekt default) s3 bucket'''
    data_byte_stream = data_to_byte(data)
    s3.put_object(
        Bucket=bucket,
        Key=f'{filename}.json',
        Body=data_byte_stream
    )
