import boto3
import json

from credentials import aws_access_key, aws_secret_access_key, aws_bucket, aws_region

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

def data_to_byte(data):
    '''converst json to bytestream'''
    data_byte_stream = bytes(json.dumps(data).encode('UTF-8'))
    return data_byte_stream

def upload_json_to_bucket(data, filename, bucket=aws_bucket, ):
    '''converts json to bytestream and uploads it to the specified 
    (projekt default) s3 bucket'''
    data_byte_stream = data_to_byte(data)
    s3_client.put_object(
        Bucket=bucket,
        Key=filename,
        Body=data_byte_stream
    )

def get_bucket(bucket_name):
    response = s3_client.list_objects(Bucket=bucket_name)
    return response

def get_bucket_content(bucket_name):
    response = get_bucket(bucket_name)
    filenames = []
    for obj in response['Contents']:
        filenames.append(obj['Key'])
    return filenames

def delete_object(bucket_name, filename):
    s3_client.delete_object(
        Bucket=bucket_name,
        Key=filename
        )
    
def get_bucket_file(bucket_name, filename):
    file = s3_client.get_object(
        Bucket=bucket_name,
        Key=filename
        )
    file = file["Body"].read()
    file = json.loads(file.decode('utf-8'))
    return file

