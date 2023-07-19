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
    data_byte_stream = bytes(json.dumps(data).encode('UTF-8'))
    return data

def upload_json_to_bucket(bucket=aws_bucket, filename, data):
    data_byte_stream = data_to_byte(data)
    s3.put_object(
        Bucket=bucket,
        Key=f'{filename}.json',
        Body=data_byte_stream
    )
