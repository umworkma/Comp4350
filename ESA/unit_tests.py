#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class ESATestCase(TestCase):

    database_uri = "sqlite:///test.db"

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    def setUp(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.all_data)
        self.db = models.init_app(self.app)
        
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    """ Test that entites are defined and we can retrieve them """
    def test_entity(self):
        entity1 = models.Entity.query.first()
        self.assertEquals(entity1.type, models.TYPE_ORGANIZATION)

        entity2 = models.Entity.query.filter_by(pk=3).first()
        self.assertEquals(entity2.type, models.TYPE_EMPLOYEE)
        
    """ Test that address is defined and we can retrieve it """
    def test_address(self):
        address1 = models.Address.query.first()
        self.assertEquals(address1.address1, '123 Vroom Street')

    """ Test that an address can be retrieved from an entity
        using the entity relationship """
    def test_entity_address_relationship(self):
        address1 = models.Address.query.first()
        entity1 = models.Entity.query.first()
        address2 = entity1.addresses[0]
        self.assertEquals(address2, address1)

    """ Test that organization is defined and we can retrieve it """
    def test_organization(self):
        org1 = models.Organization.query.first()
        self.assertEquals(org1.name, 'Ai-Kon')

    """ Test that we can retrieve an entity from the organization relationship """
    def test_organization_entity_relationship(self):
        org1 = models.Organization.query.first()
        entity1 = models.Entity.query.first()
        self.assertEquals(org1.entity, entity1)

    """ Test that we can retrieve an address from the entity defined in
        an organization relationship """
    def test_organization_address_relationship(self):
        org1 = models.Organization.query.first()
        self.assertEquals(org1.entity.addresses[0].address1, '123 Vroom Street')

    """ Test that we can retrieve a contact from the database """
    def test_contact(self):
        contact1 = models.Contact.query.first()
        self.assertEquals(contact1.value, 'info@ai-kon.org')

    """ Test that we can get contacts from an entity """
    def test_entity_contact_relationship(self):
        entity1 = models.Entity.query.first()
        self.assertEquals(entity1.contacts[0].value, 'info@ai-kon.org')

    """ Test adding a complete organization to the database """
    def test_add_organization(self):
        """ Define the data objects to be added """
        org1 = models.Organization(name='Test Org',
                            description='This is a test organization')
        org1.entity = models.Entity(type=models.TYPE_ORGANIZATION)
        org1.entity.addresses.append(models.Address(address1='4350 University Drive', address2='Suite 350',
                           city='Winnipeg', province='Manitoba',
                           isprimary=True))
        org1.entity.contacts.append(models.Contact(type=models.TYPE_PHONE,
                                  value='(204) 555-1234', isprimary=True))

        """ Add the relationships """
        """entity1.addresses = [address1]
        entity1.contacts = [contact1]
        org1.entity = entity1"""
        
        """ Add the data objects """       
        self.db.session.add(org1)
        self.db.session.commit()

        """ Retrieve the organization and test that data matches """
        org2 = models.Organization.query.filter_by(name='Test Org').first()
        self.assertEquals(org2, org1)
        self.assertNotEquals(org2.entity, None)
        self.assertEquals(org2.entity.addresses[0].address1, '4350 University Drive')
        self.assertEquals(org2.entity.contacts[0].value, '(204) 555-1234')

        """ Try grabbing some of the sub-objects from the database """
        entity2 = models.Entity.query.filter_by(pk=org2.entity.pk).first()
        self.assertNotEquals(entity2, None)

        address2 = models.Address.query.filter_by(pk=org2.entity.addresses[0].pk).first()
        self.assertEquals(address2.address1, '4350 University Drive')

        contact2 = models.Contact.query.filter_by(pk=org2.entity.contacts[0].pk).first()
        self.assertEquals(contact2.value, '(204) 555-1234')

    def test_organization_delete(self):
        """ Delete Organization 1 """
        org1 = models.Organization.query.filter_by(entityFK=1).first()
        self.db.session.delete(org1)
        self.db.session.commit()

        """ Test that it has been deleted """
        org2 = models.Organization.query.filter_by(entityFK=1).first()
        self.assertEquals(org2, None)

        """ Check if the first entity is no longer entity.pk==1
            This will determine if entity was auto-deleted and that
            other entities still exist """
        entity1 = models.Entity.query.first()
        self.assertNotEquals(entity1, None)
        self.assertNotEquals(entity1.pk, 1)

        """ Test that the addresses and contacts have been deleted """
        address1 = models.Address.query.filter_by(entityFK=1).first()
        contact1 = models.Contact.query.filter_by(entityFK=1).first()
        self.assertEquals(address1, None)
        self.assertEquals(contact1, None)

if __name__ == "__main__":
    unittest.main()
