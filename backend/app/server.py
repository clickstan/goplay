#!/usr/bin/python

import yaml

from twisted.internet.protocol import Protocol, Factory, ServerFactory
from twisted.internet import reactor

import protocol
from protocol.response import ServerError

import cuser

from room import Room

from serialization import serialization_method


class GoPlayProtocol(Protocol):
    def connectionMade(self):
        self.factory.numConnections += 1
        if self.factory.numConnections > self.factory.config['max connections']:
            self.send(ServerError.limit_reached())
            self.transport.loseConnection()
        else:
            self.data = {'authenticated' : False,
                         'user' : None,
                         }

            self.response_callbacks = {}    # {trans : [callback]}

    def connectionLost(self, reason):
        if self.data['user'] is not None:
            cuser.logout(self, trans=None)

        self.factory.numConnections -= 1

    def dataReceived(self, data):
        for message in serialization_method.loads(data):

                mks = message.keys()

                if 'command' in mks:
                    protocol.process(self, message)
                elif 'trans' in mks:
                    trans = message['trans']
                    if trans in self.response_callbacks.keys():
                        for callback in self.response_callbacks[trans]:
                            callback(message)
                        del self.response_callbacks[trans]

    def send(self, data, trans=None):
        if trans is not None:
            data['trans'] = trans
        self.transport.write(serialization_method.dumps(data))

    def addResponseCallback(self, f, trans):
        """response will be the only parameter passed to the callbacks"""
        if trans in self.response_callbacks.keys():
            self.response_callbacks[trans].append(f)
        else:
            self.response_callbacks[trans] = [f]



class GoPlayFactory(ServerFactory):
    protocol = GoPlayProtocol
    numConnections = 0

    config = {}
    with open('config.yaml', 'r') as stream:
        config = yaml.load(stream)['server']

    main_room = Room('main')
    
    

class CrossDomainPolicyProtocol(Protocol):
    def dataReceived(self, data):
        if data == "<policy-file-request/>\0":
            with open("static/cross-domain-policy.xml") as policy: 
                self.transport.write(policy.read()+'\0')
        self.transport.loseConnection()



def main():
    gpf = GoPlayFactory()
    reactor.listenTCP(gpf.config['port'], gpf)
    
    cdpf = Factory()
    cdpf.protocol = CrossDomainPolicyProtocol
    reactor.listenTCP(843, cdpf)
    
    reactor.run()


if __name__ == "__main__":
    main()
