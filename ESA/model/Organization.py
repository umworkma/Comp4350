from sqlalchemy import *
from sqlalchemy.orm import mapper, relation

import database
import Entity

# Link variables to DB tables via SQLAlchemy.
organizations = Table('organization', database.metadata, autoload=True)


# Class definition.
class Organization(object):
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
    def __repr__(self):
        return "<Organization('%s','%s','%s','%s')>" % (self.pk, self.entityFK, self.name, self.description)

    def getAll(self):
        return database.session.query(Organization).order_by(Organization.name)



# Relationships
organizationmapper = mapper(Organization, organizations, properties={
    'entity': relation(Entity.Entity, backref='organization'),
})


# DEBUG: Test code
organization = Organization()
for org in organization.getAll():
    print "Organization: '%s'  - '%s'." % (org.name, org.description)

