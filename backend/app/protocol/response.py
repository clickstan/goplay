def error(code, detail):
    return {'status' : 'error',
            'code'   : code,
            'detail' : detail}

def ok(code, detail):
    return {'status' : 'ok',
            'code'   : code,
            'detail' : detail}


class ServerError:

    @staticmethod
    def limit_reached():
        return error(100, 'limit reached')

    @staticmethod
    def not_implemented():
        return error(101, 'not implemented')


class ProtocolError:

    @staticmethod
    def invalid_message():
        return error(200, 'invalid message')

    @staticmethod
    def unknown_command():
        return error(201, 'unknown command')

    @staticmethod
    def missing_parameter():
        return error(202, 'command has a missing parameter')

    @staticmethod
    def unexpected_parameter():
        return error(203, 'command has an unexpected parameter')

    @staticmethod
    def not_logged_in():
        return error(204, 'not logged in')

    @staticmethod
    def already_logged_in():
        return error(205, 'already logged in')

    @staticmethod
    def permission_denied():
        return error(206, 'permission denied')



class UserOk:

    @staticmethod
    def login():
        return ok(300, 'logged in')

    @staticmethod
    def register():
        return ok(301, 'new user registered')

    @staticmethod
    def logout():
        return ok(302, 'logged out')

    @staticmethod
    def startchat_accepted(chat_id, sender, user):
        response = ok(303, 'chat accepted')
        response.update({'chat_id':chat_id, 'sender':sender, 'user':user})
        return response

    @staticmethod
    def startchat_not_accepted():
        return ok(304, 'chat not accepted')
    
    @staticmethod
    def startgame_accepted(game_id):
        response = ok(305, 'game accepted')
        response.update({'game_id':game_id})
        return response

    @staticmethod
    def startgame_not_accepted():
        return ok(306, 'game not accepted')


class UserError:

    @staticmethod
    def login_failed():
        return error(350, 'login failed')

    @staticmethod
    def register_failed():
        return error(351, 'register failed')

    @staticmethod
    def register_username_taken():
        return error(352, 'username already taken')

    @staticmethod
    def user_is_already_logged_in():
        return error(353, 'user is already logged in')

    @staticmethod
    def user_not_connected():
        return error(354, 'specified user isn\'t connected')

    @staticmethod
    def startchat_cannot_chat_with_yourself():
        return error(355, 'you can\'t start a chat with yourself')
    
    @staticmethod
    def startgame_cannot_play_with_yourself():
        return error(356, 'you can\'t start a game with yourself')



class ChatOk:

    @staticmethod
    def broadcast_started():
        return ok(400, 'broadcast started')

class ChatError:

    @staticmethod
    def user_doesnt_know_chat_id():
        return error(450, "user doesn't know chat id")
    

    
class GameOk:
    
    @staticmethod
    def ok_move():
        response = ok(500, "ok move")
        #response.update({'game_id':game_id})
        return response
    
    @staticmethod
    def you_can_watch():
        return ok(501, "you can watch")
    
    @staticmethod
    def you_are_already_in_the_game():
        return ok(502, "you are already in the game")
    
    @staticmethod
    def ok_resign():
        return ok(503, "ok resigning")


class GameError:

    @staticmethod
    def user_doesnt_know_game_id():
        return error(550, "user doesn't know game id")
    
    @staticmethod
    def init_failed():
        return error(551, "game initialization failed")
    
    @staticmethod
    def not_your_game():
        return error(552, "you are not playing in this game, just watch")
    
    @staticmethod
    def not_your_turn():
        return error(553, "wait for your turn")
    
    @staticmethod
    def invalid_move():
        return error(554, "invalid move")
    
    @staticmethod
    def game_not_found():
        return error(555, 'game not found anywhere')
    
    @staticmethod
    def error_resign():
        return error(556, "error resigning")