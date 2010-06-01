class GameConfig:
    def __init__(self, white, black,gameroom,
                       size=19, komi=6.5, handicap=0, timed_game=False,
                       main_time=30, byo_yomi=False):
        self.white = white      # username
        self.black = black      # username
        self.roomname = gameroom
        self.size = size
        self.komi = komi if handicap == 0 else 0.5
        self.handicap = handicap
        self.timed_game = timed_game
        self.main_time = main_time
        self.byo_yomi = byo_yomi
        
    def getColorByPlayer(self, player):
        if player.db_tuple.name == self.black:
            return 'black'
        elif player.db_tuple.name == self.white:
            return 'white'
        else:
            return None
             
        

class GameMoves:
    """Contains list of moves in an ongoing or finished game.
    Example:
        self._handicap = ['D4', 'D10', 'K4', 'K10']
        self._all = ['A1', 'K7', 'D8', 'PASS', 'PASS']
        
        if len(self._handicap) > 0:
            self._all[0] is a white play
        else:
            black starts
            
        A game is finished if the players PASS consecutively. Or if
        one of the players resign.
    """
    def __init__(self):
        self._handicap = []     # only black moves
        self._all = []
        self._resigned = None   # None, "black" or "white"
        self._score = None
    
    def finished(self):
        """Is the game finished? (True|False)"""
        if self._resigned is not None:
            return True
        
        if len(self._all) >= 2:
            if (self._all[-1] == self._all[-2]) and (self._all[-1] == 'PASS'):
                return True
        
        return False
        
    def black_first_move(self):
        """returns index of self._all that corresponds to black's first move
        returns (0|1)"""
        return 1 if len(self._handicap) > 0 else 0
    
    def white_first_move(self):
        """returns index of self._all that corresponds to white's first move
        returns (0|1)"""
        return 0 if len(self._handicap) > 0 else 1
    
    def turn(self):
        """returns ('black'|'white')"""
        if len(self._all)%2 == 0:
            return 'white' if len(self._handicap) > 0 else 'black'
        else:
            return 'black' if len(self._handicap) > 0 else 'white'
    
    def list_handicap(self):
        return self._handicap[:]
    
    def list_moves(self, color=None):
        result = []
        
        if color is None:
            result = self._all[:]
        elif color == 'black':
            for i in range(self.black_first_move(), len(self._all), 2):
                result.append(self._all[i])
        elif color == 'white':
            for i in range(self.white_first_move(), len(self._all), 2):
                result.append(self._all[i])
        else:
            raise Exception("list what?")
        
        return result
    
    def list_black_moves(self):
        return self.list_moves('black')
     
    def list_white_moves(self):
        return self.list_moves('white')

    def play_handicap(self, pos):
        """returns:
            True: sucess
            False: error
        """
        if (not self.finished) and (len(self._all) == 0):
            if isinstance(pos, list):
                self._handicap.extend(pos)
            else:
                self._handicap.append(pos)
            return True
        else:
            return False
        
    def play(self, move):
        """returns:
            True: sucess
            False: error
        """        
        if (not self.finished()):
            self._all.append(move)
            return True
        else:
            return False
        
    def resign(self, color):
        """returns:
            True: sucess
            False: error
        """
        if (self._resigned is None) and (not self.finished()):
            if (color == 'black') or (color == 'white'):
                self._resigned = color
                return True
            else:
                raise Exception("Invalid color")
        else:
            return False
        
    def score(self):
        if self._score is not None:
            return self._score
        
        if (self._resigned is None) and (not self.finished()):
            return None
        
        if self._resigned == 'black':
            self._score = 'W+R'
        elif self._resigned == 'white':
            self._score = 'B+R'
        
        return self._score