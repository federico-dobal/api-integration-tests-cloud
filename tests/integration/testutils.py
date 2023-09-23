import boto3, botocore
import os

LOCALSTACK_URL = os.environ["LOCALSTACK_URL"]
ADDRESS_TABLE = os.environ.get("ADDRESS_TABLE", "eu-central-1")
REGION = os.environ.get("REGION", "")


def _get_dynamo_client():
    return boto3.client(
        "dynamodb",
        region_name=REGION,
        endpoint_url=LOCALSTACK_URL,
    )


def _get_s3_client():
    return boto3.client(
        "s3",
        region_name=REGION,
        endpoint_url=LOCALSTACK_URL,
    )


def add_address(address):
    dynamo_client = _get_dynamo_client()
    result = dynamo_client.put_item(TableName=ADDRESS_TABLE, Item=address)
    return result


def delete_address(address):
    dynamo_client = _get_dynamo_client()
    result = dynamo_client.delete_item(TableName=ADDRESS_TABLE, Key=address)
    return result


def create_bucket(bucket_name):
    s3_client = _get_s3_client()

    try:
        s3_client.head_bucket(
            Bucket=bucket_name,
        )
    except botocore.exceptions.ClientError as e:
        # Only create the bucket if it does not exists
        if "404" in str(e):
            result = s3_client.create_bucket(
                Bucket=bucket_name,
                ACL="private",
                CreateBucketConfiguration={"LocationConstraint": "eu-central-1"},
            )
            return result
        
def delete_bucket(bucket_name):
    s3_client = _get_s3_client()

    if bucket_exists(bucket=bucket_name):
        s3_client.delete_bucket(
            Bucket=bucket_name,
        )
    
def bucket_exists(bucket: str):
    """ Check whether bucket exists """
    try:
        _get_s3_client().head_bucket(
            Bucket=bucket
        )
        return True
    except botocore.exceptions.ClientError as ex:
        return False