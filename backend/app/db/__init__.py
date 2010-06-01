__all__ = ['engine', 'Session', 'Base', 'uses_session']

import os

import logging
import logging.handlers

def enableLogger(logger):
    _logger = logging.getLogger(logger)

    try:
        os.mkdir('log')
    except OSError:
        pass

    handler = logging.handlers.RotatingFileHandler(
                "./log/{0}".format(logger), maxBytes=1024, backupCount=5)

    _logger.setLevel(logging.DEBUG)
    _logger.addHandler(handler)

loggers = ['sqlalchemy.engine',
           'sqlalchemy.dialects.postgresql',
           'sqlalchemy.pool',
           'sqlalchemy.orm',
           'sqlalchemy.orm.attributes',
           'sqlalchemy.orm.mapper',
           'sqlalchemy.orm.unitofwork',
           'sqlalchemy.orm.strategies',
           'sqlalchemy.orm.sync']

#for logger in loggers:
#    enableLogger(logger)

# =====================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
            "postgresql+psycopg2://netto:netto@127.0.0.1:5432/goplay",
            echo=False)

Session = sessionmaker(bind=engine)

Base = declarative_base()

# =====================================================================

def uses_session(f):
    """Decorates a function to automatically create and close a session"""
    def wrapper(*args, **kw):
        session = Session()
        result = None
        try:
            result = f(session=session, *args, **kw)
        except Exception:
            raise
        finally:
            session.close()
        return result
    return wrapper
