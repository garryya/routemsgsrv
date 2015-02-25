# routemsgsrv

The message routing problem reminds a wellknown change-making one which can be solved using various dynamic programming or greedy methods.
Currently the greedy method is implemented only.
The REST server is running on AWS micro instance and can be tested by running the following tests:

```
./routemsgsrv_mantest.py --server-ip=54.158.140.192 --path=greedy
```

or using CURL: 
```
curl -X POST -H "Content-Type: application/json" -d '{"message": "SendHub Rocks", "recipients": ["111-111-1111"]}' http://54.158.140.192:8080/greedy
```


**TODO**
* optimize, add more efficient routing method
* improve error handling, e.g. for invalid numbers replace too much detailed with short and infomative 
* authentication maybe...
