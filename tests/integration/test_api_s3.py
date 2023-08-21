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
        event = {'id': STUDENT_ID}

        address = lambda_handler(event=event, context=None)

        assert address.get('statusCode') == 200
        assert json.loads(address.get('body')).get('message') == 'Workspace created successfully'

        assert testutils.bucket_exists(STUDENT_ID)
        assert not testutils.bucket_exists(STUDENT_ID + '-1')

    def test_student_workspace_not_exists(self):
        event = {'id': STUDENT_ID + '-1'}

        address = lambda_handler(event=event, context=None)

        assert address.get('statusCode') == 200
        assert json.loads(address.get('body')).get('message') == 'Workspace created successfully'        
        
        assert testutils.bucket_exists(STUDENT_ID)
        assert testutils.bucket_exists(STUDENT_ID + '-1')