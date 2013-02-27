#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class OrganizationTestCase(TestCase):
    database_uri = "sqlite:///organization_unittest.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.organization_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.organization_test_data)
        self.db = models.init_app(self.app)


    """ Test that organizations are defined and the model represents them correctly. """
    def test_organization_model(self):
        aikon = models.Organization.query.filter_by(entityFK=1).first()
        self.assertIsNotNone(aikon)
        self.assertEqual(aikon.entityFK, 1)
        self.assertEqual(aikon.name, 'Ai-Kon')
        self.assertEqual(aikon.description, 'Ai-Kon Anime Convention')

        uOfM = models.Organization.query.filter_by(entityFK=2).first()
        self.assertIsNotNone(uOfM)
        self.assertEqual(uOfM.entityFK, 2)
        self.assertEqual(uOfM.name, 'University of Manitoba')
        self.assertEqual(uOfM.description, 'The University of Manitoba, is a public university in the province of Manitoba, Canada. Located in Winnipeg, it is Manitoba\'s largest, most comprehensive, and only research-intensive post-secondary educational institution.')
    
    
    """ Test that an entity can be retrieved from an organization relationship. """
    def test_organization_entity_relationship_1(self):
        # Define prerequisite data.
        entityKey = 2
        orgName = 'University of Manitoba'
        orgDescription = 'The University of Manitoba, is a public university in the province of Manitoba, Canada. Located in Winnipeg, it is Manitoba\'s largest, most comprehensive, and only research-intensive post-secondary educational institution.'
        # Retrieve the target object directly.
        direct = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Organization.query.filter_by(entityFK=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, entityKey)
        self.assertEqual(host.name, orgName)
        self.assertEqual(host.description, orgDescription)
        # Retrieve the target object through the containing object.
        target = host.entity
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())\
        
        
    """ Test that a member can be retrieved from an organization relationship. """
    def test_organization_member_relationship_1(self):
        # Define prerequisite data.
        entityKey = 1
        # Retrieve the target object directly.
        directList = models.Member.query.filter_by(organizationentityFK=entityKey)
        self.assertIsNotNone(directList)
        # Retrieve the containing object.
        host = models.Organization.query.filter_by(entityFK=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, entityKey)
        # Retrieve the target object through the containing object.
        targetList = host.employees
        self.assertIsNotNone(targetList)
        count = 0
        for di,ti in zip(directList,targetList):
            count += 1
            self.assertEqual(di.__repr__(), ti.__repr__())
        self.assertEqual(count, 2)
    

    """ Test adding an Organization. """
    def test_organization_add(self):
        # Verify state of related tables before operation.
        orgCount = models.Organization.query.count()
        entityCount = models.Entity.query.count()
        
        # Define prerequisite data.
        name = 'new org'
        desc = 'new description'
        target = models.Organization(name, desc)
        target.entity = models.Entity(models.TYPE_ORGANIZATION)

        # Verify that the data does not already exist.
        fetched = models.Organization.query.filter_by(name=name, description=desc).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.Organization.query.filter_by(name=name, description=desc)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.name, target.name)
            self.assertEqual(item.description, target.description)
            count += 1
        self.assertEqual(count, 1)

        # Verify state of related tables after the operation.
        orgCountAfter = models.Organization.query.count()
        entityCountAfter = models.Entity.query.count()
        self.assertTrue(orgCountAfter == orgCount + 1)
        self.assertTrue(entityCountAfter == entityCount + 1)


    """ Test updating an Organization. """
    def test_organization_update(self):
        # Verify state of related tables before operation.
        orgCount = models.Organization.query.count()
        entityCount = models.Entity.query.count()
        
        # Define prerequisite data.
        key = 1
        name = 'new email'

        # Verify that the data exists.
        count = models.Organization.query.filter_by(entityFK=key).count()
        self.assertEqual(count, 1)
        target = models.Organization.query.filter_by(entityFK=key).first()
        self.assertIsNotNone(target)
        
        # Perform the operation.
        target.name = name
        merged = self.db.session.merge(target)
        self.db.session.commit()

        # Verify that the data was updated.
        self.assertTrue(merged.__repr__() == target.__repr__())
        count = models.Organization.query.filter_by(entityFK=key).count()
        self.assertEqual(count, 1)
        fetched = models.Organization.query.filter_by(entityFK=key).first()
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.entityFK, target.entityFK)
        self.assertEqual(fetched.name, target.name)
        self.assertEqual(fetched.description, target.description)

        # Verify state of related tables after the operation.
        orgCountAfter = models.Organization.query.count()
        entityCountAfter = models.Entity.query.count()
        self.assertEqual(entityCount, entityCountAfter)
        self.assertTrue(orgCountAfter == orgCount)

        #self.resetDB()


    """ Test deleting an organization. """
    def test_organization_delete(self):
        # Verify state of related tables before operation.
        orgCount = models.Organization.query.count()
        entityCount = models.Entity.query.count()
        
        # Define prerequisite data.
        key = 2

        # Verify that the data exists.
        fetched = models.Organization.query.filter_by(entityFK=key).first()
        self.assertIsNotNone(fetched)
        
        # Perform the operation.
        self.db.session.delete(fetched)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        count = models.Organization.query.filter_by(entityFK=key).count()
        self.assertEqual(count, 0)

        # Verify state of related tables after the operation.
        orgCountAfter = models.Organization.query.count()
        entityCountAfter = models.Entity.query.count()
        self.assertTrue(entityCountAfter == entityCount - 1)
        self.assertTrue(orgCountAfter == orgCount - 1)

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(OrganizationTestCase('test_organization_model'))
    suite.addTest(OrganizationTestCase('test_organization_entity_relationship_1'))
    suite.addTest(OrganizationTestCase('test_organization_member_relationship_1'))
    suite.addTest(OrganizationTestCase('test_organization_add'))
    suite.addTest(OrganizationTestCase('test_organization_update'))
    suite.addTest(OrganizationTestCase('test_organization_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

