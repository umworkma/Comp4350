#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class ContactTestCase(TestCase):
    database_uri = "sqlite:///contact_unittest.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.contact_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.contact_test_data)
        self.db = models.init_app(self.app)


    """ Test that contacts are defined and the model represents them properly. """
    def test_contact_model(self):
        aikonContactEmail1 = models.Contact.query.filter_by(entityFK = 1, type = 2, isprimary = 1).first()
        self.assertIsNotNone(aikonContactEmail1)
        self.assertEqual(aikonContactEmail1.entityFK, 1)
        self.assertEqual(aikonContactEmail1.type, 2)
        self.assertEqual(aikonContactEmail1.value, 'info@ai-kon.org')
        self.assertEqual(aikonContactEmail1.isprimary, 1)

        uOfMContactPhone1 = models.Contact.query.filter_by(entityFK = 2, type = 1, isprimary = 1).first()
        self.assertIsNotNone(uOfMContactPhone1)
        self.assertEqual(uOfMContactPhone1.entityFK, 2)
        self.assertEqual(uOfMContactPhone1.type, 1)
        self.assertEqual(uOfMContactPhone1.value, '18004321960')
        self.assertEqual(uOfMContactPhone1.isprimary, 1)
    

    """ Test that an entity can be retrieved from a contact relationship. """
    def test_contact_entity_relationship_1(self):
        # Define prerequisite data.
        entityKey = 3
        contactKey = 3
        contactValue = 'umworkma@cc.umanitoba.ca'
        isprimaryValue = True
        # Retrieve the target object directly.
        direct = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Contact.query.filter_by(pk=contactKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, contactKey)
        self.assertEqual(host.value, contactValue)
        self.assertEqual(host.isprimary, isprimaryValue)
        # Retrieve the target object through the containing object.
        target = host.entity
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())


    """ Test adding a Contact. """
    def test_contact_add(self):
        # Verify state of related tables before operation.
        contactsCount = models.Contact.query.count()
        entityCount = models.Entity.query.count()
        
        # Define prerequisite data.
        entityKey = 5
        contactType = models.TYPE_EMAIL
        contactValue = 'exhaustion@comp4350.ca'
        isprimaryValue = False
        target = models.Contact(contactType, contactValue, entityKey, isprimaryValue)

        # Verify that the data does not already exist.
        fetched = models.Contact.query.filter_by(entityFK=entityKey, type=contactType, value=contactValue, isprimary=isprimaryValue).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.Contact.query.filter_by(entityFK=entityKey, type=contactType, value=contactValue, isprimary=isprimaryValue)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.entityFK, target.entityFK)
            self.assertEqual(item.type, target.type)
            self.assertEqual(item.value, target.value)
            self.assertEqual(item.isprimary, target.isprimary)
            count += 1
        self.assertEqual(count, 1)

        # Verify state of related tables after the operation.
        contactsCountAfter = models.Contact.query.count()
        entityCountAfter = models.Entity.query.count()
        self.assertEqual(entityCount, entityCountAfter)
        self.assertTrue(contactsCountAfter == contactsCount + 1)


    """ Test adding an Address. """
    def test_contact_update(self):
        # Verify state of related tables before operation.
        contactsCount = models.Contact.query.count()
        entityCount = models.Entity.query.count()
        
        # Define prerequisite data.
        contactKey = 3
        contactValue = 'new email'

        # Verify that the data exists.
        count = models.Contact.query.filter_by(pk=contactKey).count()
        self.assertEqual(count, 1)
        target = models.Contact.query.filter_by(pk=contactKey).first()
        self.assertIsNotNone(target)
        
        # Perform the operation.
        target.value = contactValue
        merged = self.db.session.merge(target)
        self.db.session.commit()

        # Verify that the data was updated.
        self.assertTrue(merged.__repr__() == target.__repr__())
        count = models.Contact.query.filter_by(pk=contactKey).count()
        self.assertEqual(count, 1)
        fetched = models.Contact.query.filter_by(pk=contactKey).first()
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.entityFK, target.entityFK)
        self.assertEqual(fetched.type, target.type)
        self.assertEqual(fetched.value, target.value)
        self.assertEqual(fetched.isprimary, target.isprimary)

        # Verify state of related tables after the operation.
        contactsCountAfter = models.Contact.query.count()
        entityCountAfter = models.Entity.query.count()
        self.assertEqual(entityCount, entityCountAfter)
        self.assertTrue(contactsCountAfter == contactsCount)

        #self.resetDB()


    """ Test deleting an address. """
    def test_contact_delete(self):
        # Verify state of related tables before operation.
        contactsCount = models.Contact.query.count()
        entityCount = models.Entity.query.count()
        
        # Define prerequisite data.
        key = 5

        # Verify that the data exists.
        fetched = models.Contact.query.filter_by(pk=key).first()
        self.assertIsNotNone(fetched)
        
        # Perform the operation.
        self.db.session.delete(fetched)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        count = models.Contact.query.filter_by(pk=key).count()
        self.assertEqual(count, 0)

        # Verify state of related tables after the operation.
        contactsCountAfter = models.Contact.query.count()
        entityCountAfter = models.Entity.query.count()
        self.assertEqual(entityCount, entityCountAfter)
        self.assertTrue(contactsCountAfter == contactsCount - 1)

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(ContactTestCase('test_contact_model'))
    suite.addTest(ContactTestCase('test_contact_entity_relationship_1'))
    suite.addTest(ContactTestCase('test_contact_add'))
    suite.addTest(ContactTestCase('test_contact_update'))
    suite.addTest(ContactTestCase('test_contact_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

