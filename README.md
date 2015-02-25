# routemsgsrv

The routing REST server implements greedy change-making method.
The server is running on AWS and can be tested by running manual test:

./routemsgsrv_mantest.py --server-ip=54.158.140.192 --path=greedy

or 

curl -X POST -H "Content-Type: application/json" -d '{"message": "SendHub Rocks", "recipients": ["111-111-1111"]}' http://54.158.140.192:8080/greedy



