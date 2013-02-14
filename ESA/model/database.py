# Connects to the database.

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://comp4350app:comp4350app@localhost/appdb')
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)
session = Session()
