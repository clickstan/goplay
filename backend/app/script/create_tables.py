#!/usr/bin/python

import sys
import hashlib

sys.path.extend(['../', './'])

import db
from db.models import *


@db.uses_session
def setDefaults(session):
    roles = {'privileged-client' : 'The GoPlay Original Frontend',
             'admin' : 'An administrator of the GoPlay server',
             'player' : 'Just a player'}

    roles = [user.Role(name, description)
                for name, description
                    in roles.iteritems()]

    session.add_all(roles)

    privileged_client_role = None
    for role in roles:
        if role.name == 'privileged-client':
            privileged_client_role = role

    # ---

    privileged_user = user.User(
                        'tgpof',
                        hashlib.sha256('#sp1-goplay').hexdigest(),
                        'The GoPlay Original Frontend')

    privileged_user.role = privileged_client_role

    session.add(privileged_user)

    # ---

    session.commit()


def main():
    db.Base.metadata.drop_all(db.engine)
    db.Base.metadata.create_all(db.engine)
    setDefaults()

if __name__ == "__main__":
    main()
