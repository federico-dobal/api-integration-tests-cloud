from api.main import create_api
import unittest
import testutils
from fastapi.testclient import TestClient
import json


STREET_NAME = "address-A"
STREET_NUMBER = "1234"
STREET_POSTAL_CODE = "9876"

class TestLambdaGetAddress(unittest.TestCase):
    
    def setUp(self):
        """
        Adds an address into the table
        """
        
        testutils.add_address(
            {
                "street_name": {"S": STREET_NAME},
                "number": {"S": STREET_NUMBER},
                "postal_code": {"S": STREET_POSTAL_CODE}
            }
        )

        app = create_api()
        self.client = TestClient(app)
        
    
    def tearDown(self):
        """
        Removes the address from the table
        """
        testutils.delete_address({"street_name": {"S": STREET_NAME}})

    def test_get_address_successful(self):
        # GIVEN the API is configured(in the setUp method)
        
        # WHEN the GET endpoint is executed
        response = self.client.get("/address/address-A")
        
        # THEN the response is successfull
        self.assertEqual(response.status_code, 200)
        
        # AND the data details is the right one
        response = json.loads(response.content)
        self.assertEqual(response.get('number'), '1234')
        self.assertEqual(response.get('postal_code'), '9876')
        self.assertEqual(response.get('street_name'), 'address-A')

    
    def test_get_address_not_exists(self):
        # GIVEN the API is configured(in the setUp method)
        
        # WHEN the GET endpoint is executed with invalid address id
        response = self.client.get("/address/address-Z")
        
        # THEN the response is not found
        self.assertEqual(response.status_code, 404)
    

        
        