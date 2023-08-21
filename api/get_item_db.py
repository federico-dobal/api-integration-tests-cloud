
from utils.api_helper import API_helper
from cloud_adapters.aws_adapter import AWS_Dynamodb_Adapter, AWS_S3_Adapter
from utils.logger import setup_logger
from utils.utils import format_return, ApiException

API = API_helper(AWS_Dynamodb_Adapter, AWS_S3_Adapter)

logger = setup_logger("aws_adapter")

def lambda_handler(event, context):
    try:
        if 'id' not in event:
            return format_return(status_code=400, body={'message': 'ERROR: mandatory data not provided'})
        
        street_name = event.get('id')
        return API.get_address_with_name(street_name)
    except ApiException as e:
        logger.error(f"API Exception: {e.body}")
        return format_return(status_code=e.status_code, body=e.body)
