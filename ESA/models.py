from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime

# Globals
TYPE_ORGANIZATION   = 1
TYPE_EMPLOYEE       = 2

TYPE_PHONE          = 1
TYPE_EMAIL          = 2

ENTITY_PK_KEY = 'entity_pk'
ENTITY_TYPE_KEY = 'entity_type'

ORGANIZATION_ENTITYFK_KEY = 'org_entityfk'
ORGANIZATION_NAME_KEY = 'org_name'
ORGANIZATION_DESCRIPTION_KEY = 'org_desc'

EMPLOYEE_ENTITYFK_KEY = 'emp_entityfk'
EMPLOYEE_USER_NAME_KEY = 'username'
EMPLOYEE_FIRST_NAME_KEY = 'firstname'
EMPLOYEE_LAST_NAME_KEY = 'lastname'
EMPLOYEE_PASSWORD_KEY = 'password'

ADDRESS_ENTITYFK_KEY = 'addr_entityfk'
ADDRESS_ADDRESS1_KEY = 'address1'
ADDRESS_ADDRESS2_KEY = 'address2'
ADDRESS_ADDRESS3_KEY = 'address3'
ADDRESS_CITY_KEY = 'city'
ADDRESS_PROVINCE_KEY = 'province'
ADDRESS_COUNTRY_KEY = 'country'
ADDRESS_POSTALCODE_KEY = 'postalcode'
ADDRESS_ISPRIMARY_KEY = 'isprimary'

CONTACT_ENTITYFK_KEY = 'contact_entityfk'
CONTACT_EMAIL_KEY = 'email'
CONTACT_PHONE_KEY = 'phone'
CONTACT_TYPE_KEY = 'type'
CONTACT_VALUE_KEY = 'value'
CONTACT_ISPRIMARY_KEY = 'isprimary'

EVENT_PK_KEY = 'event_pk'
EVENT_NAME_KEY = 'event_name'
EVENT_DESC_KEY = 'event_desc'
EVENT_START_KEY = 'event_start'
EVENT_END_KEY = 'event_end'
EVENT_ORGFK_KEY = 'event_orgfk'

SHIFT_PK_KEY = 'shift_pk'
SHIFT_EVENTFK_KEY = 'shift_eventfk'
SHIFT_START_KEY = 'shift_start'
SHIFT_END_KEY = 'shift_end'
SHIFT_LOCATION_KEY = 'shift_location'
SHIFT_MINWORKERS_KEY = 'shift_minworkers'
SHIFT_MAXWORKERS_KEY = 'shift_maxworkers'

SHIFTPERSON_SHIFT_KEY = 'shiftperson_shiftfk'
SHIFTPERSON_PERSON_KEY = 'shiftperson_personfk'

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
    addresses = db.relationship('Address', order_by='Address.isprimary', cascade='all, delete-orphan', backref='entity')
    contacts = db.relationship('Contact', order_by='Contact.isprimary, Contact.type', cascade='all, delete-orphan', backref='entity')
    organization = db.relationship('Organization', uselist=False, cascade='all,delete-orphan')
    person = db.relationship('Person', uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, type=None):
        self.type = type
        
    def __repr__(self):
        return "<Entity('%s','%s')>" % (self.pk, self.type)


class Privilege(db.Model):
    __tablename__ = 'privilege'
    pk = db.Column(db.Integer, primary_key=True)
    privilege = db.Column(db.String(255))
    ppaList = db.relationship('PrivilegePersonAssignment', cascade='all,delete-orphan', backref='privilege')
    gpaList = db.relationship('GlobalPrivilegeAssignment', cascade='all, delete-orphan', backref='privilege')
    
    def __init__(self, privilege=None):
        self.privilege = privilege
        
    def __repr__(self):
        return "<Privilege('%s','%s')>" % (self.pk, self.privilege)


class Address(db.Model):
    __tablename__ = 'address'
    pk = db.Column(db.Integer, primary_key=True)
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk, ondelete='cascade'))
    address1 = db.Column(db.String(45))
    address2 = db.Column(db.String(45))
    address3 = db.Column(db.String(45))
    city = db.Column(db.String(45))
    province = db.Column(db.String(45))
    country = db.Column(db.String(45))
    postalcode = db.Column(db.String(45))
    isprimary = db.Column(db.Boolean)

    def __init__(self, address1=None, address2=None, address3=None, city=None, province=None, country=None, postalcode=None, entityFK=None, isprimary=None):
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.city = city
        self.province = province
        self.country = country
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

    def __init__(self, type=None, value=None, entityFK=None, isprimary=None):
        self.type = type
        self.value = value
        self.entityFK = entityFK
        self.isprimary = isprimary

    def __repr__(self):
        return "<Contact('%s','%s','%s','%s','%s')>" % (self.pk, self.entityFK, self.type, self.value, self.isprimary)


class Organization(db.Model):
    __tablename__ = 'organization'
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk, ondelete='cascade'), primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    entity = db.relationship('Entity', uselist=False, cascade='all,delete')
    employees = db.relationship('Member', cascade='all, delete-orphan', backref='organization')
    events = db.relationship('Event', cascade='all, delete-orphan', backref='organization')

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
        #self.entity = models.Entity()  # This doesn't work for some unknowable pythonic reason. Grrr.
        #self.entity.type = models.TYPE_ORGANIZATION

    def __repr__(self):
        return "<Organization('%s','%s','%s')>" % (self.entityFK, self.name, self.description)


class Person(db.Model):
    __tablename__ = 'person'
    entityFK = db.Column(db.Integer, db.ForeignKey(Entity.pk, ondelete='cascade'), primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(45))
    firstname = db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    entity = db.relationship('Entity', uselist=False, cascade='all, delete')
    memberships = db.relationship('Member', cascade='all, delete-orphan', backref='person')
    gpaList = db.relationship('GlobalPrivilegeAssignment', cascade='all, delete-orphan', backref='person')
    
    def __init__(self, fname=None, lname=None, username=None, passwd=None):
        self.firstname = fname
        self.lastname = lname
        self.username = username
        self.password = passwd
        #self.entity = Entity(TYPE_EMPLOYEE)    # Stoopid python...

    # require by login manager
    def is_authenticated(self):
        return True

    # require by login manager
    def is_active(self):
        return True

    # require by login manager
    def is_anonymous(self):
        return False

    # require by login manager
    def get_id(self):
        return unicode(self.entityFK)

    def __repr__(self):
        return "<Person('%s', '%s', '%s')>" % (self.entityFK, self.firstname, self.lastname)


class Member(db.Model):
    __tablename__ = 'member'
    pk = db.Column(db.Integer, primary_key=True)
    personentityFK = db.Column(db.Integer, db.ForeignKey(Person.entityFK, ondelete='cascade'))
    organizationentityFK = db.Column(db.Integer, db.ForeignKey(Organization.entityFK, ondelete='cascade'))
    ppaList = db.relationship('PrivilegePersonAssignment', cascade='all,delete-orphan', backref='member')

    def __init__(self, personentityFK=None, organizationentityFK=None):
        self.personentityFK = personentityFK
        self.organizationentityFK = organizationentityFK
        
    def __repr__(self):
        return "<Member('%s','%s','%s')>" % (self.pk, self.personentityFK, self.organizationentityFK)


class PrivilegePersonAssignment(db.Model):
    __tablename__='privilege_member_bridge'
    pk = db.Column(db.Integer, primary_key=True)
    memberFK = db.Column(db.Integer, db.ForeignKey(Member.pk, ondelete='cascade')) 
    privilegeFK = db.Column(db.Integer, db.ForeignKey(Privilege.pk, ondelete='cascade'))

    def __init__(self, privilegeFK=None, memberFK=None):
        self.privilegeFK = privilegeFK
        self.memberFK = memberFK
        
    def __repr__(self):
        return "<Privilege('%s','%s','%s')>" % (self.pk, self.privilegeFK, self.memberFK)


class GlobalPrivilegeAssignment(db.Model):
    __tablename__='privilege_person_bridge'
    pk = db.Column(db.Integer, primary_key=True)
    privilegeFK = db.Column(db.Integer, db.ForeignKey(Privilege.pk, ondelete='cascade'))
    personentityFK = db.Column(db.Integer, db.ForeignKey(Person.entityFK, ondelete='cascade'))

    def __init__(self, privilegeFK=None, personentityFK=None):
        self.privilegeFK = privilegeFK
        self.personentityFK = personentityFK
        
    def __repr__(self):
        return "<Privilege('%s','%s','%s')>" % (self.pk, self.privilegeFK, self.personentityFK)

class Event(db.Model):
    __tablename__ = 'event'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    startdate = db.Column(db.DateTime, default=datetime.now)
    enddate = db.Column(db.DateTime, default=datetime.now)
    organizationFK = db.Column(db.Integer, db.ForeignKey(Organization.entityFK, ondelete='cascade'))
    shifts = db.relationship('Shift', cascade='all,delete-orphan', backref='event')

    def __init__(self, name=None, description=None, startdate=None, enddate=None, organizationFK=None):
        self.name = name
        self.description = description
        self.startdate = startdate
        self.enddate = enddate
        self.organizationFK = organizationFK
        
    def __repr__(self):
        return "<Event('%s','%s', '%s', '%s', '%s', '%s')>" % (self.pk, self.name, self.description, self.startdate, self.enddate, self.organizationFK)


class Shift(db.Model):
    __tablename__ = 'shift'
    pk = db.Column(db.Integer, primary_key=True)
    eventFK = db.Column(db.Integer, db.ForeignKey(Event.pk, ondelete='cascade'))
    startdatetime = db.Column(db.DateTime)
    enddatetime = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    minWorkers = db.Column(db.Integer)
    maxWorkers = db.Column(db.Integer)

    def __init__(self, eventFK=None, startdatetime=None, enddatetime=None, location=None, minWorkers=None, maxWorkers=None):
        self.eventFK = eventFK
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime
        self.location = location
        self.minWorkers = minWorkers
        self.maxWorkers = maxWorkers

    def __repr__(self):
        return "<Shift('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.pk, self.eventFK, self.startdatetime, self.enddatetime, self.location, self.minWorkers, self.maxWorkers)


class ShiftPerson(db.Model):
    __tablename__ = 'shift_person_bridge'
    pk = db.Column(db.Integer, primary_key=True)
    shiftFK = db.Column(db.Integer, db.ForeignKey(Shift.pk, ondelete='cascade'))
    personFK = db.Column(db.Integer, db.ForeignKey(Person.entityFK, ondelete='cascade'))

    def __init__(self, shiftFK=None, personFK=None):
        self.shiftFK = shiftFK
        self.personFK = personFK

    def __repr__(self):
        return "<Shift('%s', '%s', '%s')>" % (self.pk, self.shiftFK, self.personFK)
