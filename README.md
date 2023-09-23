## Execute integration tests locally
In order to execute the integration tests locally the following commands have to be executed:

* Install dependencies

      $ pip install -r tests/integration/requirements.txt
    

* Start Localstack
  
      $ EXTRA_CORS_ALLOWED_ORIGINS=http://localhost:3000,DEBUG=1,DYNAMODB_SHARE_DB=1 localstack --debug start -d

* Configure environment variables

      $ source tests/integration/scripts/build_env.sh
      
      $ sh tests/integration/scripts/build_env.sh

* Deploy infrastructure

       $ cd infrastructure/
       $ tflocal init
       $ tflocal apply

* Execute the tests   

      $ PYTHONPATH="$PYTHONPATH:./api" pytest tests/integration/

* Destroy infrastructure

       $ cd infrastructure/
       $ tflocal destroy

* Stop Localstack

       $ localstack stop
      

## API description

### How to start the API locally?

The following command has to be executed:

        $ cd api
        $ uvicorn main:app --reload

The API documentation can be accessed [here](http://127.0.0.1:8000/docs)

The API is composed of 2 endpoints:

- address: integrates with AWS DynamoDB to store addresses information such as street name, postal code, number, etc.
- workspace: integrates with AWS S3 in order to create buckets to store files associated with a given _id_.   