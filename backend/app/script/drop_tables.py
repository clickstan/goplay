#!/usr/bin/python

import sys

sys.path.extend(['../', './'])

import db
from db.models import *


def main():
    db.Base.metadata.drop_all(db.engine)

if __name__ == "__main__":
    main()
