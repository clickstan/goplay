from sqlalchemy import Column, Integer, Numeric, String, Boolean,\
                       PickleType, Enum,\
                       ForeignKey, CheckConstraint

from .user import User

from ..db import Base, uses_session

from exception import GameException

# preventing circular import when executing script/*_tables.py
import sys
if not sys.argv[0].endswith('_tables.py'):
    from ..game.data import GameConfig

from helper.threads import to_thread


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    
    #config
    white_name = Column(String(20), ForeignKey('users.name'))
    black_name = Column(String(20), ForeignKey('users.name'))
    size = Column(Integer, CheckConstraint('size>0'))
    komi = Column(Numeric, CheckConstraint('komi>=0'))
    handicap = Column(Integer, CheckConstraint('handicap>=0'))
    timed_game = Column(Boolean, nullable=False)
    main_time = Column(Numeric, CheckConstraint('main_time>0'))
    byo_yomi = Column(Boolean, nullable=False)
    
    #moves
    moves_all = Column(PickleType(mutable=False))
    moves_handicap = Column(PickleType(mutable=False))
    resigned = Column(Enum('black', 'white', name='resigned'), nullable=True)

    def __init__(self):
        pass

    def __repr__(self):
       return "<Game({0})>".format(self.id)
   
    def setConfig(self, game_config):
        self.white_name = game_config.white
        self.black_name = game_config.black
        self.size = game_config.size
        self.komi = game_config.komi
        self.handicap = game_config.handicap
        self.timed_game = game_config.timed_game
        self.main_time = game_config.main_time
        self.byo_yomi = game_config.byo_yomi
        
        if self.white_name == self.black_name:
            raise GameException("db.models.game: Game.setConfig: \
                                 white and black can't be the same user")
    
    def getConfig(self):
        return GameConfig(self.white_name, self.black_name, self.size,
                          self.komi, self.handicap, self.timed_game,
                          self.main_time, self.byo_yomi)
        
    @staticmethod
    def create(game_config, create_callback):
        @to_thread(create_callback)
        @uses_session
        def f(session):    
            try:
                game = Game()
                session.add(game)
                game.setConfig(game_config)
                session.commit()
                return game.id
            except:
                session.rollback()
                session.close()
                raise
                return None
        f()
        
    @staticmethod
    def destroy(game_id):
        if game_id is None:
            return     
        @to_thread()
        @uses_session
        def f(session):    
            try:
                game = session.query(Game).get(game_id)
                if game is not None:
                    session.delete(game)
                    session.commit()
            except:
                session.rollback()
        f()