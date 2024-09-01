import boto3


s3_client = boto3.client('s3')

s3_client.download_file('adib-source-bucket', 'adib-blue.png', 'adib-blue.png')