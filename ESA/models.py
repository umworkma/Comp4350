from sqlalchemy import *
from sqlalchemy.orm import mapper, relation

from database import DbInstance


# Globals
TYPE_ORGANIZATION   = 1
TYPE_EMPLOYEE       = 2

# DB Initialization
database = DbInstance()


# Link variables to DB tables via SQLAlchemy.
entities      = Table('entity', database.metadata, autoload=True)
organizations = Table('organization', database.metadata, autoload=True)
addresses     = Table('address', database.metadata, autoload=True)



# Class definition
class Entity(object):
    def __repr__(self):
        return "<Entity('%s','%s')>" % (self.pk, self.type)

class Organization(object):
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
    def __repr__(self):
        return "<Organization('%s','%s','%s')>" % (self.entityFK, self.name, self.description)

    def getAll(self):
        return database.session.query(Organization).order_by(Organization.name)

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
entitymapper = mapper(Entity, entities)
organizationmapper = mapper(Organization, organizations, properties={
    'entity': relation(Entity, backref='organization'),
})
addressmapper = mapper(Address, addresses, properties={
    'entity': relation(Entity, backref='addresses'),
})
