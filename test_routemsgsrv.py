#!/usr/bin/python

import httplib2
import simplejson

def buildURL(server, path):
    return 'http://%s:8080/%s' % (server, path)


def test_pos_route1(server):

    data = {
            "message": "SendHub Rocks",
            "recipients": ["+15555555556"]
    }

    url = buildURL(server, 'greedy')
    jsondata = simplejson.dumps(data)
    h = httplib2.Http()
    try:
        resp, content = h.request(url,
                                  'POST',
                                  jsondata,
                                  headers={'Content-Type': 'application/json'})
        print url
        print content
    except:
        assert 0, 'Failed connecting to the server: %s' % server
