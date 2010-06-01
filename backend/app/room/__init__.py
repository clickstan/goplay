from twisted.internet import reactor

from chat import Chat

from cuser import ConnectedUser, setroomingame

import cuser

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
        self.public_games = []
        
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
        remove_game_requests(user.conn, username,self.name)
        try:
            del self.users[username]
        except KeyError:
            pass
        
        for user_in_room in self.users.itervalues():
            reactor.callFromThread(user_in_room.conn.send,
                                   ClientRoomCommand.removeuser(self.name, username))

    def add_game(self, conn, wplayer, bplayer,size,gameid, trans=None):
        gameroom = self
 
        if gameid == -1:
            status = "waiting"
        else:
            status = "started"
 
        gameroom.public_games.append({
                  'white_plyr':wplayer,
                  'black_plyr':bplayer,
                  'size':size,
                  'status':status,
                  'gameid':gameid})
        
        resp={'command':'game.new_public_game_request',
                  'white_plyr_a':wplayer,
                  'black_plyr_a':bplayer,
                  'size_a':size,
                  'status_a':status,
                  'gameid_a':gameid}
        
        for user_in_room in gameroom.users.itervalues():
            reactor.callFromThread(user_in_room.conn.send,
                               resp)


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



def remove_game_requests(conn, username, room, trans=None):
    
    
    gameroom = Room.__rooms__.get(room)
    
    if gameroom is None:
        return
    
    for queue in gameroom.public_games:

        if (queue['white_plyr'] == username or\
                                        queue['black_plyr'] == username) and\
                                        queue['gameid'] == -1:
            resp=queue
            resp = {'command':'room.remove_public_game_request',
                         'room':gameroom.name,
                         'white_plyr':queue['white_plyr'],
                         'black_plyr':queue['black_plyr'],
                         'gameid':queue['gameid']}
            

            for user_in_room in gameroom.users.itervalues():
                
                reactor.callFromThread(user_in_room.conn.send,
                                   resp)

            gameroom.public_games.remove(queue)


def get_public_games_list(conn,room, trans=None):
    gameroom = Room.__rooms__.get(room)
    conn.send({"lista":gameroom.public_games},trans)




def request_public_game(conn,room, color, size, trans=None):
    """Se le habisa a todos los players del room que alguien solicita un juego\
    publico para que lo agreguen a su lista y se guarda en memoria del server"""
    username = conn.data['user'].db_tuple.name
    gameroom = Room.__rooms__.get(room)
    newGameQueue = None
    wplayer = None
    bplayer = None
    ##check if this game request has a match    
    for queue in gameroom.public_games:
        #if the requested size match
        if queue['size'] == size and queue['gameid'] == -1:
            #check if the color is right
            accept_request = (color == "black" and queue['black_plyr'] == "" \
                                        and queue['white_plyr'] != username) \
                                or (color == "white" \
                                    and queue['white_plyr'] == "" \
                                    and queue['black_plyr'] != username)
                                
            ##if the request is accepted tell all room players to remove 
            #the gamequeue
            if accept_request == False:
                continue
            
            resp = {'command':'room.remove_public_game_request',
                 'room':gameroom.name,
                 'white_plyr':queue['white_plyr'],
                 'black_plyr':queue['black_plyr'],
                 'gameid':queue['gameid']}

            for user_in_room in gameroom.users.itervalues():                
                 reactor.callFromThread(user_in_room.conn.send,resp)
            #mark the queue as accepted or started
            if(color == "black"):
                queue['black_plyr'] = username
            else:
                queue['white_plyr'] = username
            queue['status']="started"
            
            #  
            if color == 'black':
                otheruser = queue['white_plyr']
            else:
                otheruser = queue['black_plyr']
            gameroom.public_games.remove(queue)
            cuser.start_game(conn, otheruser, color,gameroom.name, size,None, True)
            return
            #print "el id es ",gameid
            #
            #for user in gameroom.users.itervalues():
            #    resp={'command':'game.new_public_game_request',
            #          'white_plyr_a': queue['white_plyr'],
            #          'black_plyr_a': queue['black_plyr'],
            #          'size_a':size,
            #          'status_a': queue['status'],
            #          'gameid_a':-1}
            #    user.conn.send(resp,None)
            #return

    if newGameQueue is None:
        if color=='black':
            bplayer = username
            wplayer = ""
        else:
            wplayer = username
            bplayer = ""
        
        newGameQueue = {
              'white_plyr':wplayer,
              'black_plyr':bplayer,
              'size':size,
              'status':"waiting",
              'gameid':-1}
        
        if newGameQueue in gameroom.public_games:
            return;
    
    gameid = -1;
    gameroom.add_game(conn, wplayer, bplayer,size,gameid)
    
setroomingame(Room)