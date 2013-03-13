#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class EntityTestCase(TestCase):
    database_uri = "sqlite:///entity_unittest.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.entity_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.entity_test_data)
        self.db = models.init_app(self.app)


    """ Test that entites are defined and the model represents them correctly. """
    def test_entity_model(self):
        for idx in range(1,3):
            org = models.Entity.query.filter_by(pk=idx).first()
            self.assertEqual(org.type, models.TYPE_ORGANIZATION)

        for idx in range(3,6):
            emp = models.Entity.query.filter_by(pk=idx).first()
            self.assertEqual(emp.type, models.TYPE_EMPLOYEE)


    """ Test that addresses can be retrieved from the entity relationship. """
    def test_entity_address_relationship_1(self):
        # Define prerequisite data.
        entityKey = 1
        # Retrieve the target object directly.
        directList = models.Address.query.filter_by(entityFK=entityKey).order_by(models.Address.isprimary)
        self.assertIsNotNone(directList)
        # Retrieve the containing object.
        host = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, entityKey)
        self.assertEqual(host.type, models.TYPE_ORGANIZATION)
        # Retrieve the target object through the containing object.
        targetList = host.addresses
        self.assertIsNotNone(targetList)
        count = 0
        for di,ti in zip(directList,targetList):
            self.assertEqual(di.__repr__(), ti.__repr__())
            count += 1
        self.assertEqual(count, 1)
    """ Test that addresses can be retrieved from the entity relationship. """
    def test_entity_address_relationship_2(self):
        # Define prerequisite data.
        entityKey = 2
        # Retrieve the target object directly.
        directList = models.Address.query.filter_by(entityFK=entityKey).order_by(models.Address.isprimary)
        self.assertIsNotNone(directList)
        # Retrieve the containing object.
        host = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, entityKey)
        self.assertEqual(host.type, models.TYPE_ORGANIZATION)
        # Retrieve the target object through the containing object.
        targetList = host.addresses
        self.assertIsNotNone(targetList)
        count = 0
        for di,ti in zip(directList,targetList):
            self.assertEqual(di.__repr__(), ti.__repr__())
            count += 1
        self.assertEqual(count, 1)


    """ Test that contacts can be retrieved from the entity relationship. """
    def test_entity_contact_relationship_1(self):
        # Define prerequisite data.
        entityKey = 3
        # Retrieve the target object directly.
        directList = models.Contact.query.filter_by(entityFK=entityKey).order_by(models.Contact.isprimary, models.Contact.type)
        self.assertIsNotNone(directList)
        # Retrieve the containing object.
        host = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, entityKey)
        self.assertEqual(host.type, models.TYPE_EMPLOYEE)
        # Retrieve the target object through the containing object.
        targetList = host.contacts
        self.assertIsNotNone(targetList)
        count = 0
        for di,ti in zip(directList,targetList):
            self.assertEqual(di.__repr__(), ti.__repr__())
            count += 1
        self.assertEqual(count, 3)


    """ Test that an organization can be retrieved from the entity relationship. """
    def test_entity_organization_relationship_1(self):
        # Define prerequisite data.
        entityKey = 2
        # Retrieve the target object directly.
        count = models.Organization.query.filter_by(entityFK=entityKey).count()
        self.assertEqual(count, 1)
        direct = models.Organization.query.filter_by(entityFK=entityKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, entityKey)
        self.assertEqual(host.type, models.TYPE_ORGANIZATION)
        # Retrieve the target object through the containing object.
        target = host.organization
        self.assertIsNotNone(target)
        self.assertEqual(target.entityFK, direct.entityFK)
        self.assertEqual(target.name, direct.name)
        self.assertEqual(target.description, direct.description)
        
    """ Test that a person can be retrieved from the entity relationship. """
    def test_entity_person_relationship_1(self):
        # Define prerequisite data.
        entityKey = 3
        # Retrieve the target object directly.
        count = models.Person.query.filter_by(entityFK=entityKey).count()
        self.assertEqual(count, 1)
        direct = models.Person.query.filter_by(entityFK=entityKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, entityKey)
        self.assertEqual(host.type, models.TYPE_EMPLOYEE)
        # Retrieve the target object through the containing object.
        target = host.person
        self.assertIsNotNone(target)
        self.assertEqual(target.entityFK, direct.entityFK)
        self.assertEqual(target.firstname, direct.firstname)
        self.assertEqual(target.lastname, direct.lastname)


    """ Test deleting an entity. """
    def test_entity_delete_org(self):
        # Verify state of related tables before operation.
        entityCount = models.Entity.query.count()
        orgCount = models.Organization.query.count()
        personCount = models.Person.query.count()
        addrCount = models.Address.query.count()
        contactCount = models.Contact.query.count()

        # Define prerequisite data.
        key = 2

        # Verify that the data exists.
        fetched = models.Entity.query.filter_by(pk=key).first()
        self.assertIsNotNone(fetched)

        # Perform the operation.
        self.db.session.delete(fetched)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        count = models.Entity.query.filter_by(pk=key).count()
        self.assertEqual(count, 0)

        # Verify state of related tables after the operation.
        entityCountAfter = models.Entity.query.count()
        orgCountAfter = models.Organization.query.count()
        personCountAfter = models.Person.query.count()
        addrCountAfter = models.Address.query.count()
        contactCountAfter = models.Contact.query.count()
        
        self.assertTrue(entityCountAfter == entityCount - 1)
        self.assertTrue(orgCountAfter == orgCount - 1)
        self.assertTrue(personCountAfter == personCount)
        self.assertTrue(addrCountAfter == addrCount - 1)
        self.assertTrue(contactCountAfter == contactCount - 1)
    
        #self.resetDB()
    def test_entity_delete_person(self):
        # Verify state of related tables before operation.
        entityCount = models.Entity.query.count()
        orgCount = models.Organization.query.count()
        personCount = models.Person.query.count()
        addrCount = models.Address.query.count()
        contactCount = models.Contact.query.count()

        # Define prerequisite data.
        key = 3

        # Verify that the data exists.
        fetched = models.Entity.query.filter_by(pk=key).first()
        self.assertIsNotNone(fetched)

        # Perform the operation.
        self.db.session.delete(fetched)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        count = models.Entity.query.filter_by(pk=key).count()
        self.assertEqual(count, 0)

        # Verify state of related tables after the operation.
        entityCountAfter = models.Entity.query.count()
        orgCountAfter = models.Organization.query.count()
        personCountAfter = models.Person.query.count()
        addrCountAfter = models.Address.query.count()
        contactCountAfter = models.Contact.query.count()

        self.assertTrue(entityCountAfter == entityCount - 1)
        self.assertTrue(orgCountAfter == orgCount)
        self.assertTrue(personCountAfter == personCount - 1)
        self.assertTrue(addrCountAfter == addrCount - 2)
        self.assertTrue(contactCountAfter == contactCount - 3)

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(EntityTestCase('test_entity_model'))
    suite.addTest(EntityTestCase('test_entity_address_relationship_1'))
    suite.addTest(EntityTestCase('test_entity_address_relationship_2'))
    suite.addTest(EntityTestCase('test_entity_contact_relationship_1'))
    suite.addTest(EntityTestCase('test_entity_organization_relationship_1'))
    suite.addTest(EntityTestCase('test_entity_person_relationship_1'))
    suite.addTest(EntityTestCase('test_entity_delete_org'))
    suite.addTest(EntityTestCase('test_entity_delete_person'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

