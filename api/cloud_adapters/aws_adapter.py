import boto3
import botocore
from utils.logger import setup_logger
from utils.utils import ApiException
from utils.config import REGION, STAGE, LOCALSTACK_URL
from typing import Dict
import os

log = setup_logger("lambda.gwas_batch_post")

if STAGE == 'integration-tests':
    DYNAMODB_ENDPOINT_URL = LOCALSTACK_URL
    _DYNAMODB_CLIENT = boto3.resource("dynamodb", region_name=REGION, endpoint_url=DYNAMODB_ENDPOINT_URL)
    _S3_CLIENT = boto3.client('s3', region_name=REGION, endpoint_url=DYNAMODB_ENDPOINT_URL)
else:
    dynamodb_client = boto3.resource("dynamodb")
    _DYNAMODB_CLIENT = boto3.resource("dynamodb", region_name=REGION)
    _S3_CLIENT = boto3.client('s3', region_name=REGION)

logger = setup_logger("aws_adapter")

def _get_entry(db_table: str, keys: dict) -> Dict:
    """
    Get single entry by key from DynamoDB
    """
    try:
        table = _DYNAMODB_CLIENT.Table(db_table)
        response = table.get_item(Key=keys)
    except botocore.exceptions.ClientError as err:
        message = {
            "message": f"Error getting entry from table: {db_table}, keys: {keys}",
            "context": str(err.response),
        }
        raise ApiException(status_code=500, body=message) from err
    return response.get("Item", {})

def _bucket_exists(bucket: str):
    """ Check whether bucket exists """
    try:
        _S3_CLIENT.head_bucket(
            Bucket=bucket
        )
    except botocore.exceptions.ClientError as ex:
        raise ApiException(status_code=400,
                            body={"message": f"S3 bucket not found ({bucket})"})
        
class AWS_Dynamodb_Adapter():
    
    def get_entry_dynamodb_table(self, db_table: str, keys: dict):
        return _get_entry(db_table, keys)

class AWS_S3_Adapter():
    
    def bucket_exists(self, bucket: str):
        try:
            _bucket_exists(bucket=bucket)
            return True
        except ApiException as e:
            return False

    def create_bucket(self, bucket: str):
        _S3_CLIENT.create_bucket(ACL='private', 
                                 CreateBucketConfiguration={"LocationConstraint": "eu-central-1"},
                                 Bucket=bucket)

