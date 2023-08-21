## Execute integration tests locally
In order to execute the integration tests locally the following commands have to be executed:

* Install dependencies

      $ pip install -r tests/integration/requirements.txt
    

* Start Localstack
  
      $ EXTRA_CORS_ALLOWED_ORIGINS=http://localhost:3000,DEBUG=1,DYNAMODB_SHARE_DB=1 localstack --debug start -d

* Configure environment variables

      $ source tests/integration/scripts/build_test_env.sh
      
      $ sh tests/integration/scripts/build_test_env.sh

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
      
