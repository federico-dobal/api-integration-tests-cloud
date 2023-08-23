from api.post_student_workspace import lambda_handler
import unittest
import testutils
import json

STUDENT_ID = "lopez-antonio-23456"

class TestLambdaWorkspace(unittest.TestCase):

    def setUp(self):
        """
            Creates a bucket for the student id
        """
        
        testutils.create_bucket(
            STUDENT_ID
        )
        
    
    def tearDown(self):
        """
            Removes the bucket
        """
        testutils.delete_bucket(STUDENT_ID)
        testutils.delete_bucket(STUDENT_ID + '-1')


    def test_student_workspace_exists(self):
        # GIVEN an study ID whose workspace exists
        event = {'id': STUDENT_ID}
        self.assertTrue(testutils.bucket_exists(STUDENT_ID))

        # WHEN the Lambda function is executed
        address = lambda_handler(event=event, context=None)

        # THEN it is successfully retrieved
        self.assertEqual(address.get('statusCode'), 200)
        self.assertEqual(json.loads(address.get('body')).get('message'), 'Workspace created successfully')
        
        # AND the bucket associated with it still exists
        self.assertTrue(testutils.bucket_exists(STUDENT_ID))
        self.assertFalse(testutils.bucket_exists(STUDENT_ID + '-1'))

    def test_student_workspace_not_exists(self):
        # GIVEN an study ID whose workspace does NOT exist
        event = {'id': STUDENT_ID + '-1'}

        # WHEN the Lambda function is executed
        address = lambda_handler(event=event, context=None)

        # THEN it is successfully created and retrieved
        self.assertEqual(address.get('statusCode'), 200)
        self.assertEqual(json.loads(address.get('body')).get('message'), 'Workspace created successfully')        
        
        # AND the bucket associated with it exists afterwards
        self.assertTrue(testutils.bucket_exists(STUDENT_ID))
        self.assertTrue(testutils.bucket_exists(STUDENT_ID + '-1'))