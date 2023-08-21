import os

ADDRESS_TABLE_NAME=os.environ.get('ADDRESS_TABLE', "address")
REGION=os.environ.get('REGION', "eu-central-1")
STAGE=os.environ.get('STAGE', "integration-tests")
LOCALSTACK_URL=os.environ.get('LOCALSTACK_URL', "http://localhost:4566")

