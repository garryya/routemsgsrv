#!/usr/bin/python

import httplib2
import simplejson
import argparse
import socket

defaultTestDATA = {
        "message": "SendHub Rocks",
        "recipients": [
            "650-556-6501","650-556-6502","650-556-6503","650-556-6504","650-556-6505",
            "650-556-6511","650-556-6512","650-556-6513","650-556-6514","650-556-6515",
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
try:
    resp, content = h.request(url,
                              rap.command,
                              jsondata,
                              headers={'Content-Type': 'application/json'})
    print url
    print content
except socket.error:
    print 'Failed connecting to the server:', url