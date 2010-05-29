_trans = 0

def _nextTrans():
    global _trans
    _trans += 1
    return _trans

def addtrans(f):
    """Decorates a function thar returns a dictionary.
    If the dictionary doesn't have a key 'trans', it adds one
    with a value of _nextTrans()"""
    def wrapper(*args, **kw):
        result = f(*args, **kw)
        if 'trans' not in result.keys():
            result['trans'] = _nextTrans()
        return result
    return wrapper
