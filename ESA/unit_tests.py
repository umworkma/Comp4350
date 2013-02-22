#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class ESATestCase(TestCase):

    database_uri = "sqlite:///test.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    
    
    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.all_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

     
    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.all_data)
        self.db = models.init_app(self.app)
    

    
    """ Test that entites are defined and the model represents them correctly. """
    def test_entity_model(self):
        for idx in range(1,3):
            org = models.Entity.query.filter_by(pk=idx).first()
            self.assertEquals(org.type, models.TYPE_ORGANIZATION)

        for idx in range(3,6):
            emp = models.Entity.query.filter_by(pk=idx).first()
            self.assertEquals(emp.type, models.TYPE_EMPLOYEE)

    
    """ Test that addresses are defined and the model represents them correctly. """
    def test_address_model(self):
        aikonPrimaryAddress = models.Address.query.filter_by(entityFK=1, isprimary=1).first()
        self.assertEquals(aikonPrimaryAddress.entityFK, 1)
        self.assertEquals(aikonPrimaryAddress.isprimary, 1)
        self.assertEquals(aikonPrimaryAddress.address1, '123 Vroom Street')
        self.assertEquals(aikonPrimaryAddress.city, 'Winnipeg')
        self.assertEquals(aikonPrimaryAddress.province, 'Manitoba')
        self.assertEquals(aikonPrimaryAddress.country, 'Canada')
        self.assertEquals(aikonPrimaryAddress.postalcode, 'A1A1A1')

        uOfMPrimaryAddress = models.Address.query.filter_by(entityFK=2, isprimary=1).first()
        self.assertEquals(uOfMPrimaryAddress.entityFK, 2)
        self.assertEquals(uOfMPrimaryAddress.isprimary, 1)
        self.assertEquals(uOfMPrimaryAddress.address1, '66 Chancellors Circle')
        self.assertEquals(uOfMPrimaryAddress.city, 'Winnipeg')
        self.assertEquals(uOfMPrimaryAddress.province, 'Manitoba')
        self.assertEquals(uOfMPrimaryAddress.country, 'Canada')
        self.assertEquals(uOfMPrimaryAddress.postalcode, 'R3T2N2')


    """ Test that contacts are defined and the model represents them properly. """
    def test_contact_model(self):
        aikonContactEmail1 = models.Contact.query.filter_by(entityFK = 1, type = 2, isprimary = 1).first()
        self.assertEquals(aikonContactEmail1.entityFK, 1)
        self.assertEquals(aikonContactEmail1.type, 2)
        self.assertEquals(aikonContactEmail1.value, 'info@ai-kon.org')
        self.assertEquals(aikonContactEmail1.isprimary, 1)

        uOfMContactPhone1 = models.Contact.query.filter_by(entityFK = 2, type = 1, isprimary = 1).first()
        self.assertEquals(uOfMContactPhone1.entityFK, 2)
        self.assertEquals(uOfMContactPhone1.type, 1)
        self.assertEquals(uOfMContactPhone1.value, '18004321960')
        self.assertEquals(uOfMContactPhone1.isprimary, 1)

    
    """ Test that an address can be retrieved from the entity relationship. """
    def test_entity_address_relationship(self):
        aikonAddressDirect = models.Address.query.filter_by(entityFK=1).first()
        self.assertEquals(aikonAddressDirect.address1, '123 Vroom Street')
        aikonEntity = models.Entity.query.filter_by(pk = 1).first()
        self.assertEquals(aikonEntity.type, models.TYPE_ORGANIZATION)
        aikonAddressByEntity = aikonEntity.addresses[0]
        self.assertEquals(aikonAddressByEntity.address1, '123 Vroom Street')
        self.assertEquals(aikonAddressByEntity, aikonAddressDirect)

        uOfMAddressDirect = models.Address.query.filter_by(entityFK=2).first()
        self.assertEquals(uOfMAddressDirect.address1, '66 Chancellors Circle')
        uOfMEntity = models.Entity.query.filter_by(pk = 2).first()
        self.assertEquals(uOfMEntity.type, models.TYPE_ORGANIZATION)
        uOfMAddressByEntity = uOfMEntity.addresses[0]
        self.assertEquals(uOfMAddressByEntity.address1, '66 Chancellors Circle')
        self.assertEquals(uOfMAddressByEntity, uOfMAddressDirect)

    
    """ Test that we can retrieve an entity from the organization relationship. """
    def test_organization_entity_relationship(self):
        aikonEntityDirect = models.Entity.query.filter_by(pk = 1).first()
        self.assertEquals(aikonEntityDirect.type, models.TYPE_ORGANIZATION)
        aikonOrg = models.Organization.query.filter_by(entityFK = 1).first()
        self.assertEquals(aikonOrg.name, 'Ai-Kon')
        aikonEntityByOrg = aikonOrg.entity
        self.assertEquals(aikonEntityByOrg.type, models.TYPE_ORGANIZATION)
        self.assertEquals(aikonEntityDirect, aikonEntityByOrg)

        uOfMEntityDirect = models.Entity.query.filter_by(pk = 2).first()
        self.assertEquals(uOfMEntityDirect.type, models.TYPE_ORGANIZATION)
        uOfMOrg = models.Organization.query.filter_by(entityFK = 2).first()
        self.assertEquals(uOfMOrg.name, 'University of Manitoba')
        uOfMEntityByOrg = uOfMOrg.entity
        self.assertEquals(uOfMEntityByOrg.type, models.TYPE_ORGANIZATION)
        self.assertEquals(uOfMEntityDirect, uOfMEntityByOrg)
    
    
    """ Test that we can retrieve an address from the organization relationship """
    def test_organization_address_relationship(self):
        aikonOrg = models.Organization.query.filter_by(entityFK = 1).first()
        self.assertEquals(aikonOrg.entity.addresses[0].address1, '123 Vroom Street')

        uOfMOrg = models.Organization.query.filter_by(entityFK = 2).first()
        self.assertEquals(uOfMOrg.entity.addresses[0].address1, '66 Chancellors Circle')

    
    """ Test that we can get contacts from an entity """
    def test_entity_contact_relationship(self):
        entity = models.Entity.query.filter_by(pk = 1).first()
        self.assertEquals(entity.contacts[0].value, 'info@ai-kon.org')

        entity = models.Entity.query.filter_by(pk = 2).first()
        self.assertEquals(entity.contacts[0].value, '18004321960')

    
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
        """ Test that our organization exists prior to deleting. """
        org2 = models.Organization.query.filter_by(entityFK=1).first()
        self.assertNotEquals(org2, None)

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

        """ Reset the DB for other tests, since we removed data other tests may depend on. """
        self.resetDB()
    

if __name__ == "__main__":
    unittest.main()
