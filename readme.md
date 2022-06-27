MongoDB Microservice with gRPC - Server and Client APIs in Python
-

- Install requirements:

       pip install -r requirements.txt


- Environment variables:

       export PYTHONPATH="$PYTHONPATH:/path/to/grpc_project"
       export MONGODB_URI=mongodb://username:password@host:port


- Generate server and client protocol codes:

       python -m grpc_tools.protoc --proto_path=../protos/ --python_out=. --grpc_python_out=. db.proto


- Run server:

       python db_server.py


- Run client:

       python db_client.py


- Add indexes to your database for fast selections:

       python db_indexes.py


- Run tests for gRPC connection between the server and client APIs:

       python db_test.py

  
- Testing is completed successfully for all the operation requests and gRPC connections. Please check 'db_test.py' file in the 'tests' directory. 