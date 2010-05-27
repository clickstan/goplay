from twisted.internet import reactor

from chat import Chat

from cuser import ConnectedUser

from protocol.client import Room as ClientRoomCommand

from helper.threads import to_thread


class Room:
    __rooms__ = {}  # {'name' : room_instance}
    
    @classmethod
    def add(cls, room):
        if room.name not in cls.__rooms__:
            cls.__rooms__[room.name] = room
        #else:
        #    raise ValueError("Room 'name' already in use")

    @classmethod
    def remove(cls, room):
        try:
            del cls.__rooms__[room.name]
        except KeyError:
            pass

    @to_thread()
    def __init__(self, name):
        self.name = name
        Room.add(self)

        self.chat = Chat()
        self.users = {}     # {'name' : connected_user_instance}
        
        for cu in ConnectedUser.__users__.itervalues():
            reactor.callFromThread(cu.conn.send,
                                   ClientRoomCommand.created(self.name))

    @to_thread()
    def destroy(self):
        for cu in ConnectedUser.__users__.itervalues():
            reactor.callFromThread(cu.conn.send,
                                   ClientRoomCommand.destroyed(self.name))
        
        Room.remove(self)

    @to_thread()
    def addUser(self, user):
        username = user.db_tuple.name
        
        for user_in_room in self.users.itervalues():
            reactor.callFromThread(user_in_room.conn.send,
                                   ClientRoomCommand.adduser(self.name, username))
            
        self.users[username] = user

    @to_thread()
    def removeUser(self, user):
        username = user.db_tuple.name
        
        try:
            del self.users[username]
        except KeyError:
            pass
        
        for user_in_room in self.users.itervalues():
            reactor.callFromThread(user_in_room.conn.send,
                                   ClientRoomCommand.removeuser(self.name, username))

def get_all_rooms(conn, trans=None):
    conn.send({'rooms':Room.__rooms__.keys()}, trans)

def getUsersFromRoom(conn, name, trans=None):
    room = Room.__rooms__.get(name)
    if room:
        response = room.users.keys()
    else:
        response = []
    conn.send({'users':response}, trans)

def createRoom(conn, name, trans=None):
    Room(name)
    conn.send({'name':name},trans)
    
def openRoom(conn, name, trans=None):
    user = conn.data['user']
    user.enterRoom(Room.__rooms__.get(name))
    conn.send({'name':name},trans)
    
def getChatId(conn, roomName, trans=None):
    thisRoom = Room.__rooms__.get(roomName)
    conn.send({'id':thisRoom.chat.id}, trans)