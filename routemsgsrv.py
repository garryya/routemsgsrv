#!/usr/bin/python


from twisted.web import server, resource
from twisted.internet import reactor, defer
import logging
import time
import sys
import argparse
import simplejson
import jsonschema


LOG = logging.getLogger("routemsg")

relays = {
    'small': {'name': 'Small', 'subnet': '10.0.1.0/24', 'throughput': 1, 'cost': 0.01},
    'medium': {'name': 'Medium', 'subnet': '10.0.2.0/24', 'throughput': 5, 'cost': 0.05},
    'large': {'name': 'Large', 'subnet': '10.0.3.0/24', 'throughput': 10, 'cost': 0.1},
    'super': {'name': 'Super', 'subnet': '10.0.4.0/24', 'throughput': 25, 'cost': 0.25},
}

json_schema = None

class WBSRouteMsgRoot(resource.Resource):

    def getChild(self, name, request):
        LOG.debug('getting child: %s' % name)
        if not name:
            return self
        return resource.Resource.getChild(self, name, request)

    def _handleRequest(self, data):
        return 'Hello from ROOT'

    def handleRequest(self, request):
        data = simplejson.loads(request.content.read())
        #TODO - complete input validation

        jsonschema.validate(data, json_schema)

        LOG.debug('%s:handling request: %s', self.__class__.__name__, data)
        result = simplejson.dumps({'result':self._handleRequest(data)})
        return result

    def render_POST(self, request):
        LOG.debug('render_GET: uri=%s', request.uri)
        d = defer.maybeDeferred(self.handleRequest, request)
        d.addCallback(self._ready, request)
        d.addErrback(self._error, request)
        return server.NOT_DONE_YET

    def _ready(self, result, request):
        LOG.debug('\tresult --> %s', result)
        request.write(result)
        request.finish()

    def _error(self, failure, request):
        LOG.debug('\t--> %s', failure)
        failure = {'error':str(failure.value)}
        request.write(simplejson.dumps(failure))
        request.finish()


class WBSRouteMsgGreedy(WBSRouteMsgRoot):
    isLeaf = True

    def _dogreedy(self, recipient, relays_subset, routes, recipients):
        for relay in relays_subset:
            if recipient >= len(recipients):
                break
            LOG.debug('relay %s (rp=%d)', relay, recipient)
            throughput = relay['throughput']
            if relay['subnet'] not in routes:
                routes[relay['subnet']] = {'ip':relay['subnet'], 'recipients':[]}
            routes[relay['subnet']]['recipients'] += recipients[recipient:recipient+throughput]
            recipient += throughput
        return recipient

    def _handleRequest(self, data):
        recipients = data['recipients']
        LOG.debug('recipients: %s', recipients)
        messages_number = len(recipients)
        relays_subset = { k:d for k,d in relays.items() if d['throughput'] <= messages_number}
        relays_subset = sorted(relays_subset.values(), key=lambda x:x['throughput'], reverse=True)
        routes = {}
        recipient = 0
        while recipient < messages_number:
            recipient = self._dogreedy(recipient, relays_subset, routes, recipients)
        result = {'message': 'SendHub Rocks Back','routes': routes.values()}
        return result

class WBSRouteMsgGreedy2(WBSRouteMsgRoot):
    isLeaf = True

    def _handleRequest(self, data):
        recipients = data['recipients']
        LOG.debug('recipients: %s', recipients)
        messages_number = len(recipients)
        relays_subset = { k:d for k,d in relays.items() if d['throughput'] <= messages_number}
        relays_subset = sorted(relays_subset.values(), key=lambda x:x['throughput'], reverse=True)
        routes = {}
        recipient = 0
        for relay in relays_subset:
            if recipient >= len(recipients):
                break
            throughput = relay['throughput']
            nblocks = messages_number / throughput
            if nblocks:
                LOG.debug('relay %s (rp=%d, throuput=%d, nblocks=%d)', relay, recipient, throughput, nblocks)
                if relay['subnet'] not in routes:
                    routes[relay['subnet']] = {'ip':relay['subnet'], 'recipients':[]}
                nmessages = throughput*nblocks
                routes[relay['subnet']]['recipients'] += recipients[recipient:recipient+nmessages]
                recipient += nmessages
                messages_number -= nmessages
        result = {'message': 'SendHub Rocks Back','routes': routes.values()}
        return result


ap = argparse.ArgumentParser()
ap.add_argument('--debug', action='store_const', dest='isDebug', const=True, default=False)
rap = ap.parse_args()
if rap.isDebug:
    print 'Debug mode is ON'

if __name__ == '__main__':

    filename = __file__[:__file__.rfind('.')+1]

    FMT = "%(asctime)s - %(name)-6s - %(levelname)-6s - [%(filename)s:%(lineno)d] - %(message)s"
    logging.basicConfig(filename=filename+'log',
                        level=logging.DEBUG if rap.isDebug else logging.INFO,
                        format=(FMT))
    if rap.isDebug:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter(FMT))
        LOG.addHandler(ch)

    json_schema = simplejson.loads(open(filename +'json','r').read())

    LOG.info('Starting service...')
    root = WBSRouteMsgRoot()
    root.putChild('greedy', WBSRouteMsgGreedy())
    root.putChild('greedy2', WBSRouteMsgGreedy2())
    site = server.Site(root)
    reactor.listenTCP(8080,site)
    reactor.run()



