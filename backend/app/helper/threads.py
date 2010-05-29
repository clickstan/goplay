from twisted.internet.threads import deferToThread


def to_thread(f_callback=None):
    """Decorated function will run in a separate thread.

    Optionally, when finished,  the return value will be passed to the
    callback function, if specified.
    """
    def decorator(f):
        def wrapper(*args, **kw):
            d = deferToThread(f, *args, **kw)
            if f_callback is not None:
                d.addCallback(f_callback)
        return wrapper
    return decorator


def to_thread__2_callback_args(f_callback=None):
    """Decorated function will run in a separate thread.

    Optionally, when finished,  the return value will be passed to the
    specified callback function, if specified.

    Optional parameters that will be passed only to the callback function:
        1) "result from wrapped function"
        2) conn (usually used for an instance of a twisted Protocol)
        3) trans=None (usually used for transaction number)

    Optional parameters that are None, won't be passed to the callback
    function.

    Other *args and *kwargs will be passed only to the decorated
    function.
    """
    def decorator(f):
        def wrapper(conn=None, trans=None, *args, **kw):
            d = deferToThread(f, *args, **kw)
            if f_callback is not None:
                callback_kw = {'conn' : conn, 'trans' : trans}
                for k,v in callback_kw.copy().iteritems():
                    if v is None:
                        del callback_kw[k]
                d.addCallback(f_callback, **callback_kw)
        return wrapper
    return decorator
