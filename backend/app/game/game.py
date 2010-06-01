from twisted.internet import reactor

from db import uses_session
from db.models.game import Game as DBGame

from chat import Chat

from protocol.client import Game as ClientGameCommand

from exception import GameException

from data import GameConfig, GameMoves



from engine import config as engine_config
_temp = __import__('engine.'+engine_config['engine'],
                   globals(), locals(),
                   ['EngineProcessProtocol'], -1)
EngineProcessProtocol = _temp.EngineProcessProtocol

from helper.threads import to_thread


class Game:
    __games__ = {}  # {id : game_instance}

    @classmethod
    def add(cls, game):
        if game.id not in cls.__games__:
            cls.__games__[game.id] = game

    @classmethod
    def remove(cls, game):
        try:
            del cls.__games__[game.id]
        except KeyError:
            pass

    def __init__(self):
        """game still must be initialized after instantiation."""
        self.id = None              # client side component and database has same id
        self._config = None
        self._moves = None
        self.roomname = None
        self.chat = Chat()
        self.broadcast_to = set()   # ConnectedUser set (not chat broadcast)
        
    def initialize(self, done_callback, game_config=None, id=None):
        """Create a new game:
            pass only GameConfig instance as parameter
        Retrieve game from database:
            pass only 'id' as parameter"""

        if self.id is not None:
            return
        self.roomname = game_config.roomname
        if self.roomname is None:
            print "roomname es None"
        self._moves = GameMoves()
        
        if (id is None) and (game_config is not None):
            self._create(game_config, done_callback)
        elif (id is not None) and (game_config is None):
            self._retrieve_from_db(id, done_callback)
        else:
            raise GameException("Couldn't initialize game, \
                                 pass either a GameConfig instance or 'id' of \
                                 existing game in database, not both")
         
    def _create(self, game_config, done_callback):
        """success: deferred returns id
        error: deferred returns None"""
        self._config = game_config
        
        def _create_callback(game_id):
            self.id = game_id
            
            self.engine = EngineProcessProtocol(self)
            
            params = [engine_config['executable']]
            params.extend(engine_config['params'])
            
            reactor.spawnProcess(self.engine, engine_config['full-path'], params)
            Game.add(self)
            
            done_callback()
        
        DBGame.create(game_config, _create_callback) 
    
    def _retrieve_from_db(self, id, done_callback):
        """success: returns id
        error: returns None"""
        raise NotImplementedError
        #self._config = dbgame.getConfig()
        #return dbgame.id
    
    def _store_to_db(self):
        if self.id is None:
            return
        raise NotImplementedError

    def destroy(self, clear_all_traces=False):
        if clear_all_traces:
            DBGame.destroy(self.id)
        else:
            #self._store_to_db()
            pass
        self.engine.stop()
        Game.remove(self)
        
    @classmethod
    def getGameById(cls, game_id):
        return cls.__games__.get(game_id)

    @to_thread()
    def broadcast(self, cmd, sender=None, exclude=None):
        """"cmd:  result of a ClientGameCommand staticmethod"""
        if exclude is None:
            exclude = []

        if sender is not None:
            _sender = sender.db_tuple.name
        else:
            _sender = None
            
        if _sender is not None:
            cmd['sender'] = _sender

        for user in self.broadcast_to.copy():
            if (user != sender) and (user not in exclude):
                reactor.callFromThread(user.conn.send, cmd)

    def addSpectator(self, user):
        user.conn.send(ClientGameCommand.initialize(self))
        self.broadcast_to.add(user)

    def removeSpectator(self, user):
        try:
            self.broadcast_to.remove(user)
        except KeyError:
            pass

    def play(self, move, callback1, genmove=False):
        """callback1 is called whith a True or False parameter
        when able to notify success or error"""
        if self._moves.finished():
            if not genmove:
                callback1(False)
            return
        
        color = self._moves.turn()
        
        def callback3(score):
            """called when final score is calculated"""
            self._moves._score = score
            self.broadcast(ClientGameCommand.\
                                    final_score(self.id, self._moves.score()))
        
        def callback2(valid):
            """called when move is executed and validated in the engine"""
            if valid:
                self._moves.play(move)
                self.broadcast(ClientGameCommand.play(self.id, color, move))
                if self._moves.finished():
                    self.engine.final_score(callback3)
                else:
                    if ((color == "black") and (self._config.white == "GNUGo")) or\
                       ((color == "white") and (self._config.black == "GNUGo")):
                            self.play(None, lambda: None, genmove=True)
            
            callback1(valid)
            
        def callback2_genmove(move):
            """called when move is executed using genmove"""
            self._moves.play(move)
            self.broadcast(ClientGameCommand.play(self.id, color, move))
            if self._moves.finished():
                self.engine.final_score(callback3)
        
        if not genmove:
            self.engine.play(color, move, callback2)
        else:
            self.engine.genmove(color, callback2_genmove)
            
    def resign(self, player):
        color = self._config.getColorByPlayer(player)
        
        if color is not None:
            if self._moves.resign(color):
                lista = self.__class__.Room.__rooms__.get(self.roomname).public_games
                for i in range(len(lista)):
                    if lista[i].get('gameid') == self.id:
                        lista[i]['status']="finished"
                self.broadcast(ClientGameCommand.\
                                final_score(self.id, self._moves.score()))
                return True
        return False