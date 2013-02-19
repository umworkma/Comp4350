from sqlalchemy import *
from sqlalchemy.orm import mapper, relation

import database

# Link variables to DB tables via SQLAlchemy.
entities      = Table('entity', database.metadata, autoload=True)

# Class definition
class Entity(object):
    def __repr__(self):
        return "<Entity('%s','%s')>" % (self.pk, self.type)


# Relationships
entitymapper = mapper(Entity, entities)
