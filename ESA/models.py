from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# Globals
TYPE_ORGANIZATION   = 1
TYPE_EMPLOYEE       = 2

# DB Initialization
db = SQLAlchemy()

def init_app(app):
    """Initializes Flassk app."""
    db.app = app
    db.init_app(app)
    return db

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

    def __repr__(self):
        return "<Entity('%s','%s')>" % (self.pk, self.type)

class Organization(object):
    __tablename__ = 'organization'
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk), primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.String(500))

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Organization('%s','%s','%s')>" % (self.entityFK, self.name, self.description)

    def getAll(self):
        return database.session.query(Organization).order_by(Organization.name)

class Address(object):
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

