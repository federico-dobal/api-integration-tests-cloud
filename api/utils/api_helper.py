from cloud_adapters.aws_adapter import AWS_Dynamodb_Adapter, AWS_S3_Adapter
from utils.config import ADDRESS_TABLE_NAME
from utils.utils import ApiException

class API_helper():

    def __init__(self, aws_dynamodb_adapter: AWS_Dynamodb_Adapter, aws_s3_Adapter: AWS_S3_Adapter):
        self.aws_dynamodb_adapter = aws_dynamodb_adapter 
        self.aws_s3_Adapter = aws_s3_Adapter   
    
    def get_address_with_name(self, street_name: str):
        return self.aws_dynamodb_adapter.get_entry_dynamodb_table(self, db_table=ADDRESS_TABLE_NAME, keys={"street_name": street_name})
    

    def create_student_workspace(self, bucket_name: str):
        
        if not self.aws_s3_Adapter.bucket_exists(self, bucket=bucket_name):
            self.aws_s3_Adapter.create_bucket(self,bucket=bucket_name)
        else:
            raise ApiException(status_code=400, message='Workspace already exists')


