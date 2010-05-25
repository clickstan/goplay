from helper.protocol import addtrans


class Chat:

    @staticmethod
    @addtrans
    def call_into(sender, chat_id):
        return {'command' : 'chat.call_into',
                'chat_id' : chat_id,
                'sender' : sender}

    @staticmethod
    #@addtrans
    def broadcast(sender, chat_id, msg):
        return {'command' : 'chat.broadcast',
                'chat_id' : chat_id,
                'sender' : sender,
                'msg' : msg}


class Game:

    @staticmethod
    @addtrans
    def call_into(sender, game_id):
        return {'command' : 'game.call_into',
                'game_id' : game_id,
                'sender' : sender}
        
    @staticmethod
    #@addtrans
    def initialize(game):
        return {'command' : 'game.initialize',
                'game_id' : game.id,
                'chat_id' : game.chat.id, 
                # config
                'black' : game._config.black,
                'white' : game._config.white,
                'size' : game._config.size,
                'komi' : game._config.komi,
                'handicap' : game._config.handicap,
                'timed_game' : game._config.timed_game,
                'main_time' : game._config.main_time,
                'byo_yomi' : game._config.byo_yomi,
                # moves
                'moves_handicap' : game._moves._handicap,
                'moves_all' : game._moves._all,
                'resigned' : game._moves._resigned,
                'score' : game._moves._score}
        
    @staticmethod
    #@addtrans
    def play(game_id, color, move):
        """color : ('black'|'white')
        move: ('A1'..'T19'|'PASS')
        """
        return {'command' : 'game.play',
                'game_id' : game_id,
                'color' : color,
                'move' : move}
        
    @staticmethod
    #@addtrans
    def final_score(game_id, score):
        """the game is finished
        score: ('W'|'B')+(points_difference|'R')
        
        examples: score = 'W+8.5'    # white wins by 8.5 points
                  score = 'B+R'      # black wins, black resigned
        """
        return {'command' : 'game.final_score',
                'game_id' : game_id,
                'score' : score}