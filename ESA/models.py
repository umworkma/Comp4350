from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# Globals
TYPE_ORGANIZATION   = 1
TYPE_EMPLOYEE       = 2

TYPE_PHONE          = 1
TYPE_EMAIL          = 2

ORGANIZATION_NAME_KEY = 'org_name'
ORGANIZATION_DESCRIPTION_KEY = 'org_desc'

ADDRESS_ADDRESS1_KEY = 'address1'
ADDRESS_ADDRESS2_KEY = 'address2'
ADDRESS_ADDRESS3_KEY = 'address3'
ADDRESS_CITY_KEY = 'city'
ADDRESS_PROVINCE_KEY = 'province'
ADDRESS_COUNTRY_KEY = 'country'
ADDRESS_POSTALCODE_KEY = 'postalcode'

CONTACT_EMAIL_KEY = 'email'
CONTACT_PHONE_KEY = 'phone'


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
    addresses = db.relationship('Address', cascade='all, delete')
    contacts = db.relationship('Contact', cascade='all, delete')
    
    def __init__(self, type=None):
        self.type = type
        
    def __repr__(self):
        return "<Entity('%s','%s')>" % (self.pk, self.type)

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
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk, ondelete='cascade'))
    isprimary = db.Column(db.Boolean)

    def __init__(self, address1=None, address2=None, address3=None, city=None, province=None, postalcode=None, entityFK=None, isprimary=None):
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.city = city
        self.province = province
        self.postalcode = postalcode
        self.entityFK = entityFK
        self.isprimary = isprimary

    def __repr__(self):
        return "<Address('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.pk, self.entityFK, self.address1, self.address2, self.address3, self.city, self.province, self.country, self.postalcode, self.isprimary)

class Contact(db.Model):
    __tablename__ = 'contact'
    pk = db.Column(db.Integer, primary_key=True)
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk, ondelete='cascade'))
    type = db.Column(db.Integer)
    value = db.Column(db.String(45))
    isprimary = db.Column(db.Boolean)

    def __repr__(self):
        return "<Contact('%s','%s','%s','%s','%s')>" % (self.pk, self.entityFK, self.type, self.value, self.isprimary)
    
class Organization(db.Model):
    __tablename__ = 'organization'
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk, ondelete='cascade'), primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    entity = db.relationship('Entity',uselist=False, cascade='all, delete')

    def __repr__(self):
        return "<Organization('%s','%s','%s')>" % (self.entityFK, self.name, self.description)

    def getAll(self):
        return Organization.query.all()

    def serialize(self):
        return jsonify(self)

