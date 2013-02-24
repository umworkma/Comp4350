#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class MemberTestCase(TestCase):
    database_uri = "sqlite:///member_unittest.db"
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


    """ Test that members are defined and the model represents them correctly. """
    def test_member_model(self):
        current = models.Member.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.personentityFK, 3)
        self.assertEqual(current.organizationentityFK, 1)

        current = models.Member.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.personentityFK, 4)
        self.assertEqual(current.organizationentityFK, 1)

        current = models.Member.query.filter_by(pk=3).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.personentityFK, 4)
        self.assertEqual(current.organizationentityFK, 2)

        current = models.Member.query.filter_by(pk=4).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.personentityFK, 5)
        self.assertEqual(current.organizationentityFK, 2)


    """ Test that we can retrieve an organzation from a member. """
    def test_member_organization_relationship(self):
        direct = models.Organization.query.filter_by(entityFK=1).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.name, 'Ai-Kon')
        host = models.Member.query.filter_by(pk=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.organizationentityFK, 1)
        target = host.organization
        self.assertIsNotNone(target)
        self.assertEqual(target.entityFK, direct.entityFK)
        self.assertEqual(target.name, direct.name)
    """ Test that we can retrieve members from an organization. """
    def test_organization_member_relationship(self):
        directList = models.Member.query.filter_by(organizationentityFK=1)
        self.assertIsNotNone(directList)

        host = models.Organization.query.filter_by(entityFK=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, 1)

        targetList = host.employees
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.personentityFK, ti.personentityFK)
            self.assertEqual(di.organizationentityFK, ti.organizationentityFK)
        self.assertGreater(resultCount, 0)


    """ Test that we can retrieve a person from a member. """
    def test_member_person_relationship(self):
        direct = models.Person.query.filter_by(entityFK=4).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.firstname, 'Ryoji')
        host = models.Member.query.filter_by(pk=3).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.personentityFK, 4)
        target = host.person
        self.assertIsNotNone(target)
        self.assertEqual(target.entityFK, direct.entityFK)
        self.assertEqual(target.firstname, direct.firstname)
        self.assertEqual(target.lastname, direct.lastname)
    """ Test that we can retrieve members from a person. """
    def test_person_member_relationship(self):
        directList = models.Member.query.filter_by(personentityFK=4)
        self.assertIsNotNone(directList)

        host = models.Person.query.filter_by(entityFK=4).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, 4)

        targetList = host.memberships
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.personentityFK, ti.personentityFK)
            self.assertEqual(di.organizationentityFK, ti.organizationentityFK)
        self.assertGreater(resultCount, 0)


    """ Test adding a Member (linking a person to an organization). """
    def test_member_add(self):
        # Define prerequisite data.
        personKey = 5
        orgKey = 1
        target = models.Member(personentityFK=personKey, organizationentityFK=orgKey)

        # Verify that the data does not already exist.
        fetched = models.Member.query.filter_by(personentityFK=personKey, organizationentityFK=orgKey).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.Member.query.filter_by(personentityFK=personKey, organizationentityFK=orgKey)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.personentityFK, personKey)
            self.assertEqual(item.organizationentityFK, orgKey)
            count += 1
        self.assertEqual(count, 1)


    """ Test deleting a member. """
    def test_member_delete(self):
        # Define required test data.
        personKey = 4
        orgKey = 1
        target = models.Member(personentityFK=personKey, organizationentityFK=orgKey)

        # Verify that prerequisite data exists.
        target = models.Member.query.filter_by(personentityFK=personKey, organizationentityFK=orgKey).first()
        self.assertIsNotNone(target)

        # Perform the operation.
        self.db.session.delete(target)
        self.db.session.commit()

        # Verify that the record has been removed.
        target = models.Member.query.filter_by(personentityFK=personKey, organizationentityFK=orgKey).first()
        self.assertIsNone(target)

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(MemberTestCase('test_member_model'))
    suite.addTest(MemberTestCase('test_member_organization_relationship'))
    suite.addTest(MemberTestCase('test_organization_member_relationship'))
    suite.addTest(MemberTestCase('test_member_person_relationship'))
    suite.addTest(MemberTestCase('test_person_member_relationship'))
    suite.addTest(MemberTestCase('test_member_add'))

    # Tests that must be run last b/c they delete from the DB.
    # Since we aren't resetting, they might remove info other tests need.
    # If we chose to call resetDB() after any of these tests, they
    # could be moved up to the previous section, but they would
    # take a little bit longer to run.
    suite.addTest(MemberTestCase('test_member_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

