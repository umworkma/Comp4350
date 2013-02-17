#from sqlalchemy import *
#from sqlalchemy.orm import mapper, relation
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

#from database import DbInstance


# Globals
TYPE_ORGANIZATION   = 1
TYPE_EMPLOYEE       = 2

# DB Initialization
#database = DbInstance()
db = SQLAlchemy()


def init_app(app):
    """Initializes Flassk app."""
    db.app = app
    db.init_app(app)
    return db

def create_tables(app):
    "Create tables, and return engine"
    #engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    engine = create_engine(app.config['mysql://comp4350app:comp4350app@localhost/appdb'])
    db.metadata.create_all(engine)
    return engine


# Class definition
class Entity(db.Model):
    __tablename__ = 'entity'
    pk = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)

    def __repr__(self):
        return "<Entity('%s','%s')>" % (self.pk, self.type)

class Organization(db.Model):
    __tablename__ = 'organization'
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk), primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.String(500))

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Organization('%s','%s','%s')>" % (self.entityFK, self.name, self.description)

    @property
    def serialize(self):
        return {
            'id'            : self.entityFK,
            'name'          : self.name,
            'description'   : self.description
        }

    def getAll(self):
        return Organization.query.order_by(Organization.name)
        #return database.session.query(Organization).order_by(Organization.name)

    def getByID(self, entityid):
        return Organization.query.filter_by(entityFK=entityid).first()
        #return database.session.query(Organization).filter_by(entityFK=entityid)

    def update(self, entityid, name, description):
        result = False
        target = Organization()
        target = target.getByID(entityid)
        if(target.entityid == entityid):
            target.name = name
            target.description = description
            result = database.session.commit()
        return result_by(Organization.name)

class Address(db.Model):
    __tablename__ = 'address'
    pk = db.Column(db.Integer, primary_key=True)
    address1 = db.Column(db.String(45))
    address2 = db.Column(db.String(45))
    address3 = db.Column(db.String(45))
    city = db.Column(db.String(45))
    province = db.Column(db.String(45))
    country = db.Column(db.String(45))
    postalcode = db.Column(db.String(45))
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk))
    isprimary = db.Column(db.Integer)
    
    def __init__(self, address1=None, address2=None, address3=None, city=None,
                 province=None, country=None, postalcode=None, isprimary=None):
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.city = city
        self.province = province
        self.country = country
        self.postalcode = postalcode
        self.isprimary = isprimary
        
    def __repr__(self):
        return "<Address('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.pk, self.entityFK, self.address1, self.address2, self.address3, self.city, self.province, self.country, self.postalcode, self.isprimary)

    def getByEntity(self, entityid):
        return database.session.query(Address).filter_by(entityFK=entityid)

'''
# Link variables to DB tables via SQLAlchemy.
entities      = Table('entity', database.metadata, autoload=True)
organizations = Table('organization', database.metadata, autoload=True)
addresses     = Table('address', database.metadata, autoload=True)



# Class definition
class Entity(object):
    def __repr__(self):
        return "<Entity('%s','%s')>" % (self.pk, self.type)

class Organization(object):
    def __init__(self, entityid=None, name=None, description=None):
        self.entityid = entityid
        self.name = name
        self.description = description
    def __repr__(self):
        return "<Organization('%s','%s','%s')>" % (self.entityFK, self.name, self.description)

    @property
    def serialize(self):
        return {
            'id'            : self.entityFK,
            'name'          : self.name,
            'description'   : self.description
        }

    def getAll(self):
        return database.session.query(Organization).order_by(Organization.name)

    def getByID(self, entityid):
        return database.session.query(Organization).filter_by(entityFK=entityid)

    def update(self, entityid, name, description):
        result = False
        target = Organization()
        target = target.getByID(entityid)
        if(target.entityid == entityid):
            target.name = name
            target.description = description
            result = database.session.commit()
        return result
        

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

    def getAddressByEntityID(self, entityid):
        return database.session.query(Address).filter_by(entityFK=entityid)



# Relationships
entitymapper = mapper(Entity, entities)
organizationmapper = mapper(Organization, organizations, properties={
    'entity': relation(Entity, backref='organization'),
})
addressmapper = mapper(Address, addresses, properties={
    'entity': relation(Entity, backref='addresses'),
})
'''
