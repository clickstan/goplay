from sqlalchemy.exc import IntegrityError

from db import uses_session
from db.models.user import User as DBUser, Role

from protocol.client import Chat as ClientChatCommand
from protocol.client import Game as ClientGameCommand
from protocol.response import UserOk, UserError, ServerError, GameOk, GameError

from chat import Chat

from game.game import Game
from game.data import GameConfig

from helper.threads import to_thread__2_callback_args

class ConnectedUser:
    __users__ = {}  # {'name' : connected_user_instance}

    @classmethod
    def add(cls, user):
        if user.db_tuple.name not in cls.__users__:
            cls.__users__[user.db_tuple.name] = user
        else:
            raise ValueError("User 'name' already connected")

    @classmethod
    def remove(cls, user):
        try:
            del cls.__users__[user.db_tuple.name]
        except KeyError:
            pass

    def __init__(self, db_tuple, conn):
        """db_tuple:
            a namedtuple from db.models.user.User"""
        self.db_tuple = db_tuple
        ConnectedUser.add(self)

        self.conn = conn
        self.rooms = {} # {'name' : room_instance}
        self.chats = {} # {id : chat_instance}
        self.games = {} # {id : game_instance}

    def destroy(self):
        for room in self.rooms.copy().itervalues():
            self.exitRoom(room)

        for chat in self.chats.copy().itervalues():
            self.exitChat(chat)
            
        for game in self.games.copy().itervalues():
            self.exitGame(game)

        ConnectedUser.remove(self)

    def enterChat(self, chat):
        chat.addUser(self)
        self.chats[chat.id] = chat

    def exitChat(self, chat):
        chat.removeUser(self)
        try: del self.chats[chat.id]
        except: pass

    def enterRoom(self, room):
        if room.name not in self.rooms:
            room.addUser(self)
            self.rooms[room.name] = room
            self.enterChat(room.chat)

    def exitRoom(self, room):
        room.removeUser(self)
        try: del self.rooms[room.name]
        except: pass
        self.exitChat(room.chat)
        
    def enterGame(self, game):
        game.addSpectator(self)
        self.games[game.id] = game
        self.enterChat(game.chat)

    def exitGame(self, game):
        game.removeSpectator(self)
        try: del self.games[game.id]
        except: pass
        self.exitChat(game.chat)
    
    def getChatById(self, id):
        return self.chats.get(id)
    
    def getGameById(self, id):
        return self.games.get(id)

    def callIntoChat(self, sender, chat_id, sender_callback):
        """another user may use this to request a chat with
        this user

        sender:  ConnectedUser instance that wants to chat
        chat_id: Chat instance created by the sender
        sender_callback: function to be called when a response
                         is obtained from the user, accepts one
                         parameter 'accepted' as True or False"""
        def response_callback(response):
            """expects response to be a dict with a key 'accepted'
            and boolean value"""
            if response['accepted']:
                self.enterChat(sender.getChatById(chat_id))
            sender_callback(response['accepted'])

        command = ClientChatCommand.call_into(sender.db_tuple.name, chat_id)

        self.conn.addResponseCallback(response_callback, command['trans'])
        self.conn.send(command)
        
    def callIntoGame(self, sender, game_id, sender_callback):
        """another user may use this to request a game with
        this user

        sender:  ConnectedUser instance that wants to play
        game_id: Game instance created by the sender
        sender_callback: function to be called when a response
                         is obtained from the user, accepts one
                         parameter 'accepted' as True or False"""
        def response_callback(response):
            """expects response to be a dict with a key 'accepted'
            and boolean value"""
            if response['accepted']:
                self.enterGame(sender.getGameById(game_id))
            sender_callback(response['accepted'])

        command = ClientGameCommand.call_into(sender.db_tuple.name, game_id)

        self.conn.addResponseCallback(response_callback, command['trans'])
        self.conn.send(command)



def _login_callback(user_tuple, conn, trans=None):
    if user_tuple is not None:
        try:
            cu = ConnectedUser(user_tuple, conn)
        except ValueError:
            # this user is already logged in
            conn.send(UserError.user_is_already_logged_in(), trans)
            return

        conn.data['authenticated'] = True
        conn.data['user'] = cu

        cu.enterRoom(conn.factory.main_room)

        response = UserOk.login()
    else:
        response = UserError.login_failed()

    conn.send(response, trans)

@to_thread__2_callback_args(_login_callback)
@uses_session
def login(session, username, password):
    dbuser = session.query(DBUser).filter(DBUser.name == username).first()

    if (dbuser is not None) and (dbuser.password == password):
        user_tuple = dbuser.namedtuple()
    else:
        user_tuple = None

    return user_tuple


def logout(conn, trans=None):
    conn.data['user'].destroy()
    conn.data['user'] = None
    conn.send(UserOk.logout(), trans)
    conn.transport.loseConnection()


@to_thread__2_callback_args(lambda res, conn, trans: conn.send(res, trans))
@uses_session
def register(session, username, password, fullname, role):
    try:
        dbuser = DBUser(username, password, fullname)
        session.add(dbuser)
        dbuser.role = session.query(Role).filter(Role.name == role).one()
        session.commit()
        response = UserOk.register()
    except IntegrityError:
        session.rollback()
        response = UserError.register_username_taken()
    except:
        session.rollback()
        response = UserError.register_failed()

    return response


def start_chat(conn, username, trans=None):
    """first part of message interchange for starting a one-to-one
    conversation"""
    user = ConnectedUser.__users__.get(username)
    sender = conn.data['user']

    if sender is user:
        conn.send(UserError.startchat_cannot_chat_with_yourself(), trans)
        return

    chat = Chat()

    def callback(accepted):
        if accepted:
            conn.send(UserOk.startchat_accepted(chat.id), trans)
        else:
            sender.exitChat(chat)
            conn.send(UserOk.startchat_not_accepted(), trans)

    if user is not None:
        sender.enterChat(chat)
        user.callIntoChat(sender, chat.id, callback)
    else:
        conn.send(UserError.user_not_connected(), trans)


def start_game(conn, username, color, size=None, trans=None):
    """first part of message interchange for starting a game
    
    color: 'white' or 'black'  (game starter will get this color)
    
    # TODO: faltan otras opciones de juego a configurar
    """
    user = ConnectedUser.__users__.get(username)
    sender = conn.data['user']

    if sender is user:
        conn.send(UserError.startgame_cannot_play_with_yourself(), trans)
        return
    
    if user is None:
        conn.send(UserError.user_not_connected(), trans)
        return

    game = Game()
    
    def call_into_callback(accepted):
        if accepted:
            conn.send(UserOk.startgame_accepted(), trans)
        else:
            sender.exitGame(game)
            game.destroy(clear_all_traces=True)
            conn.send(UserOk.startgame_not_accepted(), trans)
    
    def game_init_done_callback():
        if game.id is None:
            conn.send(GameError.init_failed(), trans)
        else:
            sender.enterGame(game)
            user.callIntoGame(sender, game.id, call_into_callback)
    
    if color == 'white':
        white = sender.db_tuple.name
        black = user.db_tuple.name
    else:
        black = sender.db_tuple.name
        white = user.db_tuple.name
        
    kwarg = {}
    
    if isinstance(size, int):
        kwarg['size'] = size
    
    game_config = GameConfig(white, black, **kwarg)
        
    game.initialize(game_init_done_callback, game_config=game_config)


def watch_game(conn, game_id, trans=None):
    user = conn.data['user']
    game = Game.getGameById(game_id)

    # TODO: what if game is not in memory, but in the database?
    
    if user.getGameById(game_id) is None:
        if game is not None:
            user.enterGame(game)
            response = GameOk.you_can_watch()
        else:
            response = GameError.game_not_found()
    else:
        response = GameOk.you_are_already_in_the_game()
        
    conn.send(response, trans)

