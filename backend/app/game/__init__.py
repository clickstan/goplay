from protocol.response import GameOk, GameError


def play(conn, game_id, move, trans=None):
    player = conn.data['user']
    game = player.getGameById(game_id)
    
    if game is not None:
        if game._moves.turn() == 'black':
            player_to_play = game._config.black
        else:
            player_to_play = game._config.white
            
        player_name = player.db_tuple.name
        
        if player_name in [game._config.black, game._config.white]:
            if player_name == player_to_play:
                def callback(valid):
                    if valid:
                        response = GameOk.ok_move()
                    else:
                        response = GameError.invalid_move()
                    conn.send(response, trans)
                    
                game.play(move, callback)
                response = None
            else:
                response = GameError.not_your_turn()
        else:
            response = GameError.not_your_game()
    else:
        response = GameError.user_doesnt_know_game_id()
    
    if response is not None:
        conn.send(response, trans)
    

def resign(conn, game_id, trans=None):
    player = conn.data['user']
    game = player.getGameById(game_id)
    
    if game is not None:
        player_name = player.db_tuple.name
        
        if player_name in [game._config.black, game._config.white]:
            if game.resign(player):
                response = GameOk.ok_resign()
            else:
                response = GameError.error_resign()
        else:
            response = GameError.not_your_game()
    else:
        response = GameError.user_doesnt_know_game_id()
    
    conn.send(response, trans)