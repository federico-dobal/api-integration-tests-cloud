
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
        
        student_id = event.get('id')
        API.create_student_workspace(student_id)
        return format_return(status_code=200, body={'message': 'Workspace created successfully'})
    except ApiException as e:
        logger.error(f"API Exception: {e.body}")
        return format_return(status_code=e.status_code, body=e.body)
