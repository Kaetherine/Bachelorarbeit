import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='YOUR_REGION' # for example, 'eu-central-1'
)

import boto3

# Initialisieren Sie das S3-Client
s3 = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

# Die Daten, die Sie hochladen möchten
data = {"key": "value"}

# Konvertieren Sie Ihre Daten in einen Byte-Stream, bevor Sie sie hochladen
import json
data_byte_stream = bytes(json.dumps(data).encode('UTF-8'))

# Hochladen der Daten
s3.put_object(Bucket='your_bucket_name', Key='your_file_name.json', Body=data_byte_stream)
