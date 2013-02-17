<<<<<<< HEAD
#from sqlalchemy import *
#from sqlalchemy.orm import mapper, relation
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

#from database import DbInstance

=======
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
>>>>>>> db_restructure

# Globals
TYPE_ORGANIZATION   = 1
TYPE_EMPLOYEE       = 2

<<<<<<< HEAD
# DB Initialization
#database = DbInstance()
db = SQLAlchemy()
=======
TYPE_PHONE          = 1
TYPE_EMAIL          = 2
>>>>>>> db_restructure

# DB Initialization
db = SQLAlchemy()

def init_app(app):
    """Initializes Flassk app."""
    db.app = app
    db.init_app(app)
    return db
<<<<<<< HEAD

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

=======
>>>>>>> db_restructure

def create_tables(app):
    "Create tables, and return engine"
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine

# Class definition
class Entity(db.Model):
    __tablename__ = 'entity'
    pk = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    addresses = db.relationship('Address')
    contacts = db.relationship('Contact')
    
    def __init__(self, type=None):
        self.type = type
        
    def __repr__(self):
        return "<Entity('%s','%s')>" % (self.pk, self.type)

<<<<<<< HEAD
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
=======
class Address(db.Model):
    __tablename__ = 'address'
    pk = db.Column(db.Integer, primary_key=True)
    address1 = db.Column(db.String(45))
    address2 = db.Column(db.String(45))
    address3 = db.Column(db.String(45))
    city = db.Column(db.String(45))
    province = db.Column(db.String(45))
    postalcode = db.Column(db.String(45))
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk))
    isprimary = db.Column(db.Boolean)

    def __init__(self, address1=None, address2=None, address3=None, city=None, province=None, postalcode=None, entityFK=None, isprimary=None):
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.city = city
        self.province = province
>>>>>>> db_restructure
        self.postalcode = postalcode
        self.entityFK = entityFK
        self.isprimary = isprimary

    def __repr__(self):
        return "<Address('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.pk, self.entityFK, self.address1, self.address2, self.address3, self.city, self.province, self.country, self.postalcode, self.isprimary)

<<<<<<< HEAD
    def getAddressByEntityID(self, entityid):
        return database.session.query(Address).filter_by(entityFK=entityid)

=======
class Contact(db.Model):
    __tablename__ = 'contact'
    pk = db.Column(db.Integer, primary_key=True)
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk))
    type = db.Column(db.Integer)
    value = db.Column(db.String(45))
    isprimary = db.Column(db.Boolean)
>>>>>>> db_restructure

    def __repr__(self):
        return "<Contact('%s','%s','%s','%s','%s')>" % (self.pk, self.entityFK, self.type, self.value, self.isprimary)
    
class Organization(db.Model):
    __tablename__ = 'organization'
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk), primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    entity = db.relationship('Entity',uselist=False)

<<<<<<< HEAD
# Relationships
entitymapper = mapper(Entity, entities)
organizationmapper = mapper(Organization, organizations, properties={
    'entity': relation(Entity, backref='organization'),
})
addressmapper = mapper(Address, addresses, properties={
    'entity': relation(Entity, backref='addresses'),
})
'''
=======
    def __repr__(self):
        return "<Organization('%s','%s','%s')>" % (self.EntityFK, self.name, self.description)
>>>>>>> db_restructure
