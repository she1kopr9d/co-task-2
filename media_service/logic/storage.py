import os
import boto3
import botocore.exceptions


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
)

BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")


def download_file_from_s3(s3_key: str, local_path: str) -> bool:
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            s3.download_fileobj(BUCKET_NAME, s3_key, f)
        return True
    except botocore.exceptions.ClientError:
        return False


def upload_to_s3(key, file_obj):
    s3.upload_fileobj(
        Fileobj=file_obj,
        Bucket=BUCKET_NAME,
        Key=key,
        ExtraArgs={"ContentType": "image/jpeg"},
    )
