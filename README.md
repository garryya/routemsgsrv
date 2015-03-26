# routemsgsrv

## Messaging

The message routing problem reminds a wellknown change-making one which can be solved using various dynamic programming or greedy methods.
Currently the **greedy** and improved **greedy2** methods are implemented.
The greedy method may fail to give an optimal solution and it's complexity is O(N) where N is number of recipients.  

The REST server is implemented as twisted non-blocking webserver and running on AWS micro instance and can be tested by running the following tests:

```
./routemsgsrv_mantest.py --server-ip=54.158.140.192 --path=greedy
./routemsgsrv_mantest.py --server-ip=54.158.140.192 --path=greedy2
```

or running command line test tool : 
```
./routemsgsrv-test.sh greedy2
```

or using CURL from command line: 
```
curl -X POST -H "Content-Type: application/json" -d '{"message": "SendHub Rocks", "recipients": ["111-111-1111"]}' http://54.158.140.192:8080/greedy
curl -X POST -H "Content-Type: application/json" -d '{"message": "SendHub Rocks", "recipients": ["111-111-1111"]}' http://54.158.140.192:8080/greedy2
```

or unit test:
```
py.test --server=54.158.140.192
```

**TODO**
* add more optimal DP-based routing method (+unittest)
* improve error handling, e.g. for invalid numbers replace too much detailed with short and infomative 
* authentication maybe...
