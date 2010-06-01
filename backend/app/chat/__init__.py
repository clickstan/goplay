from twisted.internet import reactor

from protocol.client import Chat as ClientChatCommand
from protocol.response import ChatOk, ChatError

from helper.threads import to_thread


_id_counter = -1

def _nextId():
    global _id_counter
    _id_counter += 1
    return _id_counter


class Chat:

    def __init__(self):
        self.id = _nextId()         # client side component has same id
        self.broadcast_to = set()   # ConnectedUser set

    @to_thread()
    def broadcast(self, msg, sender=None, exclude=None):
        if exclude is None:
            exclude = []

        if sender is not None:
            _sender = sender.db_tuple.name
        else:
            _sender = None

        for user in self.broadcast_to.copy():
            if user not in exclude:
                reactor.callFromThread(user.conn.send,
                                       ClientChatCommand.broadcast(_sender, self.id, msg))

    def addUser(self, user):
        self.broadcast_to.add(user)
        self.broadcast('{0} joined the chat'.format(user.db_tuple.name),
                       exclude=[user])

    def removeUser(self, user):
        try:
            self.broadcast_to.remove(user)
            self.broadcast('{0} left the chat'.format(user.db_tuple.name),
                           exclude=[user])
        except KeyError:
            pass


def broadcast(conn, chat_id, msg, trans=None):
    """handler: client -> server"""
    sender = conn.data['user']
    chat = sender.getChatById(chat_id)

    if chat is not None:
        chat.broadcast(msg, sender)
        response = ChatOk.broadcast_started()
    else:
        response = ChatError.user_doesnt_know_chat_id()

    conn.send(response, trans)
