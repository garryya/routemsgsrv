#!/usr/bin/python

import httplib2
from datetime import datetime
import simplejson
import argparse

#defaultTestDATA = {'woggle': {'version': 1234, 'updated': str(datetime.now()),}}
defaultTestDATA = {
        "message": "SendHub Rocks",
        "recipients": [
            "+15555555556", "+15555555555", "+15555555554", "+15555555553","+15555555552", "+15555555551",
            "+15555555156", "+15555555155", "+15555555154", "+15555555153","+15555555152", "+15555555151",
        ]
}

ap = argparse.ArgumentParser()
ap.add_argument('--command', action='store', dest='command', default='POST')
ap.add_argument('--path', action='store', dest='path', default='')
ap.add_argument('--data', action='store', dest='data', default=defaultTestDATA)
ap.add_argument('--server-ip', action='store', dest='server_ip', default='localhost')
rap = ap.parse_args()

url = 'http://%s:8080/%s' % (rap.server_ip, rap.path)

jsondata = simplejson.dumps(rap.data)
h = httplib2.Http()
resp, content = h.request(url,
                          rap.command,
                          jsondata,
                          headers={'Content-Type': 'application/json'})
print url
print content