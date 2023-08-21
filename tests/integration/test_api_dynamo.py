from api.get_item_db import lambda_handler
import unittest
import testutils

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
        event = {'id': STREET_NAME}
        address = lambda_handler(event=event, context=None)

        self.assertEqual(address.get('street_name'), STREET_NAME)
        self.assertEqual(address.get('number'), STREET_NUMBER)
        self.assertEqual(address.get('postal_code'), STREET_POSTAL_CODE)

        