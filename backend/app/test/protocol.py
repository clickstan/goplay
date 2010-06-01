import hashlib


trans = 0

def nextTrans():
    global trans
    trans += 1
    return trans


class Send:

    def __init__(self, conn):
        self.conn = conn

    def send(self, trans=None, **kw):
        if trans is not None:
            if trans == 'auto':
                kw['trans'] = nextTrans()
            else:
                try:
                    kw['trans'] = int(trans)
                except ValueError:
                    pass
        
        to_int = ['size']        
        
        for k,v in kw.iteritems():
            if (k.endswith('_id')) or (k in to_int):
                try:
                    kw[k] = int(v)
                except ValueError:
                    pass
            else:
                try:
                    int(v)
                    print "warning: parameter '{0}' was encoded as string".format(k)
                except ValueError:
                    pass

        if 'accepted' in kw.keys():
            kw['accepted'] =  kw['accepted'] == 'True'

        return self.conn.send(kw)

    def login(self, username='', password=''):
        return self.conn.send({'command'  : 'user.login',
                               'username' : username,
                               'password' : hashlib.sha256(password).hexdigest(),
                               'trans'    : nextTrans()}
                        )

    def register(self, username='', password='', fullname='', role=''):
        return self.conn.send({'command'  : 'user.register',
                               'username' : username,
                               'password' : hashlib.sha256(password).hexdigest(),
                               'fullname' : fullname,
                               'role'     : role,
                               'trans'    : nextTrans()}
                        )

    def logout(self):
        return self.conn.send({'command' : 'user.logout',
                               'trans'   : nextTrans()})

    def broadcast(self, chat_id, msg):
        return self.conn.send({'command' : 'chat.broadcast',
                               'chat_id' : chat_id,
                               'msg' : msg,
                               'trans' : nextTrans()})


class Receive:

    def __init__(self, conn):
        self.conn = conn
