from  typing import Dict, Union, Any
import json

class ApiException(Exception):
    """
    Generic Exception

    """

    def __init__(self, message: str = "", status_code: int = 400, body: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = {"message": message} if body is None else body


def format_return(
    status_code: int = 200, body: Union[dict, None] = None
) -> Dict[str, Any]:
    """Wrap return messages in a dict for sending back through lambda function"""
    if body is None:
        body = {}
    if not isinstance(status_code, int):
        raise TypeError("status_code: Only integer is allowed")
    if not isinstance(body, dict):
        raise TypeError("body: Only Dict is allowed")
    if "message" in body:
        print(body["message"])
    if "context" in body:
        print(body["context"])
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"},
    }