from sqlalchemy import *
from sqlalchemy.orm import mapper, relation

import database
import Entity

# Link variables to DB tables via SQLAlchemy.
addresses     = Table('address', database.metadata, autoload=True)


# Class definition.
class Address(object):
    def __init__(self, address1=None, address2=None, address3=None, city=None,
                 province=None, country=None, postalcode=None, isprimary=None):
        self.address1   = address1
        self.address2   = address2
        self.address3   = address3
        self.city       = city
        self.province   = province
        self.country    = country
        self.postalcode = postalcode
        self.isprimary  = isprimary
    def __repr__(self):
        return "<Address('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.pk, self.entityFK, self.address1, self.address2, self.address3, self.city, self.province, self.country, self.postalcode, self.isprimary)

    def getByEntity(self, entityid):
        return database.session.query(Address).filter_by(entityFK=entityid)



# Relationships
addressmapper = mapper(Address, addresses, properties={
    'entity': relation(Entity.Entity, backref='addresses'),
})
