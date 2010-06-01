#!/usr/bin/python

import json

from twisted.internet import reactor, task
from twisted.internet.protocol import Protocol, ClientFactory

from protocol import Send


def prints(x):
    print 'sent:{0}\n'.format(x)


class TestClient(Protocol):
    def connectionMade(self):
        pSend = Send(self)
        d = task.deferLater(reactor, 0, pSend.login, 'tgpof', '#sp1-goplay')
        d.addCallback(prints)

        d = task.deferLater(reactor, 1, pSend.register, 'asdf', 'asdf', 'asdf-san', 'player')
        d.addCallback(prints)
        
        d = task.deferLater(reactor, 2, pSend.register, 'qwer', 'qwer', 'qwerty', 'player')
        d.addCallback(prints)
        
        d = task.deferLater(reactor, 3, pSend.register, 'zxcv', 'zxcv', 'zxcv!', 'player')
        d.addCallback(prints)

        d = task.deferLater(reactor, 4, pSend.logout)
        d.addCallback(prints)

    def dataReceived(self, data):
        for message in data.split('\0'):
            print 'received:', message

    def send(self, json_serializable):
        message = json.dumps(json_serializable)
        self.transport.write(message+'\0')
        return message



class TestClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return TestClient()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        reactor.stop()


def main():
    reactor.connectTCP('localhost', 7777, TestClientFactory())
    reactor.run()


if __name__ == "__main__":
    main()
