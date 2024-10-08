import boto3
import os

from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def upload_folder_to_s3(folder_path, bucket, s3_prefix=""):
    """
    :param folder_path: Path to the local folder
    :param bucket: S3 bucket name
    :param s3_prefix: Prefix in the S3 bucket (optional)
    :return: None
    """
    # Initialize the S3 client

    # Walk through the directory structure
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # Construct full local path
            local_file_path = os.path.join(root, file_name)

            # Construct the S3 key (path) by removing the root folder part and adding the prefix
            relative_path = os.path.relpath(local_file_path, folder_path)
            s3_file_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")  # Replace backslashes with slashes for S3 compatibility

            try:
                # Upload the file
                s3_client.upload_file(local_file_path, bucket, s3_file_key)
                print(f"Uploaded {local_file_path} to {bucket}/{s3_file_key}")
            except FileNotFoundError:
                print(f"The file {local_file_path} was not found.")
            except NoCredentialsError:
                print("Credentials not available.")
                return
            except ClientError as e:
                print(f"Failed to upload file {local_file_path}: {e}")
                return
            print(f"Upload of {local_file_path} to {bucket}/{s3_file_key} complete.")
    
    # remove the raw video file and output directory
    os.system(f'rm -rf media/*')