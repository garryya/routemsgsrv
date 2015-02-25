#!/usr/bin/python

import httplib2
import simplejson

def buildURL(server, path):
    return 'http://%s:8080/%s' % (server, path)


def request(server, path, data):
    url = buildURL(server, path)
    jsondata = simplejson.dumps(data)
    h = httplib2.Http()
    try:
        resp, content = h.request(url,
                                  'POST',
                                  jsondata,
                                  headers={'Content-Type': 'application/json'})
        return simplejson.loads(content)
    except:
        assert 0, 'Failed connecting to the server: %s' % url

def test_POS_greedy_1recipient(server):

    data = {
            "message": "SendHub Rocks",
            "recipients": ["111-222-3333"]
    }
    content = request(server, 'greedy', data)
    assert 'error' not in content
    assert len(content['result']['routes']) == 1
    assert content['result']['routes'][0]['recipients'][0] == data['recipients'][0]

def test_POS_greedy_2recipients(server):

    data = {
            "message": "SendHub Rocks",
            "recipients": ["111-222-3333","111-222-4444"]
    }
    content = request(server, 'greedy', data)
    assert 'error' not in content
    assert len(content['result']['routes']) == 1
    assert len(content['result']['routes'][0]['recipients']) == len(data['recipients'])
    for i in range(len(data['recipients'])):
        assert content['result']['routes'][0]['recipients'][i] == data['recipients'][i]

def test_POS_greedy_12recipients(server):

    data = {
            "message": "SendHub Rocks",
            "recipients": [
                "650-556-6501","650-556-6502","650-556-6503","650-556-6504","650-556-6505","650-556-6506",
                "650-556-6511","650-556-6512","650-556-6513","650-556-6514","650-556-6515","650-556-6516",
            ]
    }
    content = request(server, 'greedy', data)
    assert 'error' not in content
    nroutes = len(content['result']['routes'])
    assert nroutes == 2
    nrecipients = 0
    for i in range(nroutes):
        rr = content['result']['routes'][i]['recipients']
        nrecipients += len(rr)
        for r in rr:
            assert r in data['recipients']
    assert nrecipients == len(data['recipients'])

def test_POS_greedy2_1recipient(server):

    data = {
            "message": "SendHub Rocks",
            "recipients": ["111-222-3333"]
    }
    content = request(server, 'greedy2', data)
    assert 'error' not in content
    assert len(content['result']['routes']) == 1
    assert content['result']['routes'][0]['recipients'][0] == data['recipients'][0]

def test_POS_greedy2_many_recipient(server):

    data = {
            "message": "SendHub Rocks",
            "recipients": []
    }
    nrecipients = 111
    for i in range(nrecipients):
        data['recipients'].append('111-222-0%03d' %i)

    content = request(server, 'greedy2', data)
    assert 'error' not in content
    nroutes = len(content['result']['routes'])
    assert nroutes == 3
    nrecipients = 0
    for i in range(nroutes):
        rr = content['result']['routes'][i]['recipients']
        nrecipients += len(rr)
        for r in rr:
            assert r in data['recipients']
    assert nrecipients == len(data['recipients'])

def test_NEG_greedy_badnumber(server):

    data = {
            "message": "SendHub Rocks",
            "recipients": ["+15555555556"]
    }
    content = request(server, 'greedy', data)
    assert 'error' in content
