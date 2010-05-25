from collections import namedtuple

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from ..db import Base


UserTuple = namedtuple('UserTuple',
                       ['id', 'name', 'password', 'fullname', 'role'])


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
       return "<Role('{0}', '{1}')>".format(self.name, self.description)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    fullname = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship(Role, backref=backref('users', order_by=id))

    def __init__(self, name, password, fullname):
        self.name = name
        self.password = password
        self.fullname = fullname

    def __repr__(self):
       return "<User('{0}', '{1}')>".format(self.name, self.role)

    def namedtuple(self):
        return UserTuple(self.id, self.name, self.password,
                         self.fullname, self.role)
