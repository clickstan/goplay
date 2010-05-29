#!/usr/bin/python

import json

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.error import ReactorNotRunning

from protocol import Send


class TestConsoleClient(Protocol):
    def connectionMade(self):
        pSend = Send(self)
        reactor.callInThread(console_loop, pSend)

    def dataReceived(self, data):
        for message in data.split('\0'):
            print 'received:', message

    def send(self, json_serializable):
        message = json.dumps(json_serializable)
        self.transport.write(message+'\0')
        return message


class TestConsoleClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return TestConsoleClient()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        reactor.stop()



def console_loop(pSend):
    while True:
        try:
            s = raw_input()
        except EOFError:
            try:
                reactor.stop()
            except ReactorNotRunning:
                pass
            finally:
                break

        if s.strip() != '':
            reactor.callFromThread(process_input, pSend, s)

def process_input(pSend, s):
    s = [' '.join(w.split('+')) for w in s.split()]
    command = s[0]
    if command == 'send':
        kw = {}
        for k,v in [e.split(':') for e in s[1:]]:
            kw[k] = v
        pSend.send(**kw)
    else:
        args = s[1:]
        if command == 'broadcast':
            try:
                args[0] = int(args[0])
            except (IndexError, ValueError):
                print 'check documentation for "broadcast"'

        try:
            eval('pSend.'+command+'(*args)')
        except AttributeError:
            print 'undefined command'
        except TypeError:
            print 'check documentation for "{0}"'.format(command)


def main():
    reactor.connectTCP('localhost', 7777, TestConsoleClientFactory())
    reactor.run()


if __name__ == "__main__":
    main()
