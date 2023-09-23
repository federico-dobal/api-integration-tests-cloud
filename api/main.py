from fastapi import FastAPI, APIRouter, status
from fastapi.responses import JSONResponse
from utils.api_helper import API_helper
from cloud_adapters.aws_adapter import AWS_Dynamodb_Adapter, AWS_S3_Adapter
from utils.logger import setup_logger
from utils.utils import format_return, ApiException
from utils.models import Workspace

API = API_helper(AWS_Dynamodb_Adapter, AWS_S3_Adapter)

logger = setup_logger("aws_adapter")

def api_resonse(status_code, content={}, message=None):
    if message:
        content["message"] = message

    return JSONResponse(status_code=status_code, content=content)


def create_api():
        
    app = FastAPI(
        title="Cloud integration API", openapi_url="/openapi.json"
    )

    @app.get("/address/{id}")
    def get_item(id: str) -> dict:
        """
            Get address
        """
        try: 
        
            if not id:
                logger.error(f"ERROR: id was not provided")
                return api_resonse(
                        status.HTTP_400_BAD_REQUEST,
                        message="ERROR: mandatory data not provided",
                )
            
            address_in_db = API.get_address_with_name(id)
            print(address_in_db)
            if not address_in_db:
                logger.error(f"ERROR: address not found {id}")
                return api_resonse(
                        status.HTTP_404_NOT_FOUND,
                        message='ERROR: address not found',
                )
            else:
                
                return api_resonse(
                            status.HTTP_200_OK,
                            content=address_in_db,
                    )
        except ApiException as e:
            logger.error(f"API Exception: {e.body}")
            return api_resonse(
                            status.e.status_code,
                            message=e.body,
                    )


    @app.post("/workspace")
    def create_workspace(
        id: Workspace,
    ):
        try:
            if not id:
                return format_return(status_code=400, body={'message': 'ERROR: mandatory data not provided'})
            
            API.create_student_workspace(id.id)
            return api_resonse(200, 'Workspace created successfully')
        except ApiException as e:
            logger.error(f"API Exception: {e.body}")
            return api_resonse(e.status_code, e.body)
            #return format_return(status_code=e.status_code, body=e.body)
        
        


    return app

app = create_api()

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")