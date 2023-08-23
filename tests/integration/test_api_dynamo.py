from api.get_item_db import lambda_handler
import unittest
import testutils
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
        
    
    def tearDown(self):
        """
        Removes the address from the table
        """
        testutils.delete_address({"street_name": {"S": STREET_NAME}})


    def test_get_address_exists(self):
        # GIVEN an street name that is already in the DB
        event = {'id': STREET_NAME}

        # WHEN the Lambda function is executed
        address = lambda_handler(event=event, context=None)

        # THEN it returns the right record
        response_body = json.loads(address.get('body'))
        self.assertEqual(response_body.get('street_name'), STREET_NAME)
        self.assertEqual(response_body.get('number'), STREET_NUMBER)
        self.assertEqual(response_body.get('postal_code'), STREET_POSTAL_CODE)

    def test_get_address_not_exists(self):
        # GIVEN an street name that is NOT in the DB
        event = {'id': 'name'}

        # WHEN the Lambda function is executed
        address = lambda_handler(event=event, context=None)

        # THEN it does not retrieve any record
        self.assertIsNone(address.get('street_name'))
        
        