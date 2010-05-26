from response import ProtocolError

import cuser
import chat
import game
import room

server_commands =\
    {'user.login'      : {'handler'  : cuser.login,
                          'requires' : ['username', 'password']},

     'user.logout'     : {'handler'  : cuser.logout,
                          'requires' : []},

     'user.register'   : {'handler'  : cuser.register,
                          'requires' : ['username', 'password', 'fullname', 'role'],
                          'roles'    : ['privileged-client']},

     'user.start_chat' : {'handler'  : cuser.start_chat,
                          'requires' : ['username']},

     'user.start_game' : {'handler'  : cuser.start_game,
                          'requires' : ['username', 'color'],
                          'optional' : ['size']},
                          
     'user.watch_game' : {'handler'  : cuser.watch_game,
                          'requires' : ['game_id']},

     'chat.broadcast'  : {'handler'  : chat.broadcast,
                          'requires' : ['chat_id', 'msg']},
     
     'game.play'       : {'handler'  : game.play,
                          'requires' : ['game_id', 'move']},
                          
     'game.resign'     : {'handler'  : game.resign,
                          'requires' : ['game_id']},
                          
    'room.get_all_rooms'      :{'handler'  : room.get_all_rooms,
                              'requires'  : []},
                              
    'room.getUsersFromRoom'   : {'handler' : room.getUsersFromRoom,
                             'requires'  : ['name']},
    }



def process(conn, message):

    trans = message.get('trans')
    message['trans'] = trans

    if 'command' not in message.keys():
        conn.send(ProtocolError.invalid_message(), trans)
        return

    command = message['command']

    del message['command']
    kwargs = {}
    for k, v in message.iteritems():
        if isinstance(v, unicode):
            kwargs[str(k)] = str(v)
        else:
            kwargs[str(k)] = v

    if command in server_commands:
        for required in server_commands[command]['requires']:
            if required not in message:
                conn.send(ProtocolError.missing_parameter(), trans)
                return

        del message['trans']
        for k in message.keys():
            if (k not in server_commands[command]['requires']) and\
               (k not in server_commands[command]['optional']):
                conn.send(ProtocolError.unexpected_parameter(), trans)
                return
        message['trans'] = trans
    else:
        conn.send(ProtocolError.unknown_command(), trans)
        return

    if command == 'user.login':
        if conn.data['authenticated']:
            conn.send(ProtocolError.already_logged_in(), trans)
            return

    if not conn.data['authenticated']:
        if command != 'user.login':
            conn.send(ProtocolError.not_logged_in(), trans)
            return

    command = server_commands[command]

    if 'roles' in command:
        if conn.data['user'].db_tuple.role.name not in command['roles']:
            conn.send(ProtocolError.permission_denied(), trans)
            return

    command['handler'](conn, **kwargs)
