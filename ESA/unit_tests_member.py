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
        fixtures.install(self.app, *fixtures.member_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.member_test_data)
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
        # Define prerequisite data.
        memberKey = 3
        orgKey = 2
        name = 'Ai-Kon'
        # Retrieve the target object directly.
        direct = models.Organization.query.filter_by(entityFK=orgKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Member.query.filter_by(pk=memberKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, memberKey)
        self.assertEqual(host.organizationentityFK, orgKey)
        # Retrieve the target object through the containing object.
        target = host.organization
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())


    """ Test that we can retrieve a person from a member. """
    def test_member_person_relationship(self):
        # Define prerequisite data.
        memberKey = 4
        personKey = 5
        fname = 'Dan'
        lname = 'Nelson'
        # Retrieve the target object directly.
        direct = models.Person.query.filter_by(entityFK=personKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Member.query.filter_by(pk=memberKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, memberKey)
        self.assertEqual(host.personentityFK, personKey)
        # Retrieve the target object through the containing object.
        target = host.person
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())
        
        
    """ Test that we can retieve a person-assignments from a member. """
    def test_member_ppa_relationship(self):
        # Define prerequisite data.
        key = 4
        # Retrieve the target object directly.
        directList = models.PrivilegePersonAssignment.query.filter_by(memberFK=key)
        self.assertIsNotNone(directList)
        # Retrieve the containing object.
        host = models.Member.query.filter_by(pk=key).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, key)
        # Retrieve the target object through the containing object.
        targetList = host.ppaList
        self.assertIsNotNone(targetList)
        count = 0
        for di,ti in zip(directList, targetList):
            count += 1
            self.assertEqual(di.__repr__(), ti.__repr__())
        self.assertEqual(count, 2)


    """ Test adding a Member (linking a person to an organization). """
    def test_member_add(self):
        # Verify state of related tables before operation.
        personCount = models.Person.query.count()
        orgCount = models.Organization.query.count()
        memberCount = models.Member.query.count()
        
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
        
        # Verify state of related tables after operation.
        personCountAfter = models.Person.query.count()
        orgCountAfter = models.Organization.query.count()
        memberCountAfter = models.Member.query.count()
        self.assertEqual(personCount, personCountAfter)
        self.assertEqual(orgCount, orgCountAfter)
        self.assertTrue(memberCountAfter == memberCount + 1)


    """ Test deleting a member. """
    def test_member_delete(self):
        # Verify state of related tables before operation.
        personCount = models.Person.query.count()
        orgCount = models.Organization.query.count()
        memberCount = models.Member.query.count()
        
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
        
        # Verify state of related tables after operation.
        personCountAfter = models.Person.query.count()
        orgCountAfter = models.Organization.query.count()
        memberCountAfter = models.Member.query.count()
        self.assertEqual(personCount, personCountAfter)
        self.assertEqual(orgCount, orgCountAfter)
        self.assertTrue(memberCountAfter == memberCount - 1)

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(MemberTestCase('test_member_model'))
    suite.addTest(MemberTestCase('test_member_organization_relationship'))
    suite.addTest(MemberTestCase('test_member_person_relationship'))
    suite.addTest(MemberTestCase('test_member_ppa_relationship'))
    suite.addTest(MemberTestCase('test_member_add'))
    suite.addTest(MemberTestCase('test_member_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

