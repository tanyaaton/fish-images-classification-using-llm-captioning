import ibm_boto3
from ibm_botocore.client import Config
import os
from dotenv import load_dotenv

load_dotenv()

def download_from_cos(bucket_name, object_key, download_path):
    # You should set these as environment variables for security
    api_key = os.environ.get('IBM_COS_API_KEY')
    resource_instance_id = os.environ.get('IBM_COS_RESOURCE_INSTANCE_ID')
    endpoint_url = os.environ.get('IBM_COS_ENDPOINT')

    cos = ibm_boto3.client(
        's3',
        ibm_api_key_id=api_key,
        ibm_service_instance_id=resource_instance_id,
        config=Config(signature_version='oauth'),
        endpoint_url=endpoint_url
    )

    cos.download_file(Bucket=bucket_name, Key=object_key, Filename=download_path)
    print(f"Downloaded {object_key} to {download_path}")

if __name__ == "__main__":
    bucket = 'intern-bucket'
    object_key = '1753170220487-star-medal.png'
    download_path = './1753170220487-star-medal.png'
    download_from_cos(bucket, object_key, download_path)
    print("Done.")
