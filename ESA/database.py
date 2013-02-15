# Connects to the database.

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

DB_USER = 'comp4350app'
DB_PWD  = 'comp4350app'
DB_SCHEMA = 'appdb'
engine = None # = create_engine('mysql://comp4350app:comp4350app@localhost/appdb')
metadata = None # = MetaData(engine)

#Session # = sessionmaker(bind=engine)
session = None # = Session()

class DbInstance(object):
    engine = None;
    metadata = None
    session = None
    
    def __init__(self, user=DB_USER, pwd=DB_PWD, schema=DB_SCHEMA):
        self.setEngine(user, pwd, schema)
        self.metadata = MetaData(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def setEngine(self, user, pwd, schema):
        self.engine = create_engine('mysql://' + user + ':' + pwd + '@localhost/' + schema)

