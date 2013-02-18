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
        
if __name__ == "__main__":
    unittest.main()
