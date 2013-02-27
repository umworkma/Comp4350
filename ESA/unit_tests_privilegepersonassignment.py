#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class PrivilegePersonAssignmentTestCase(TestCase):
    database_uri = "sqlite:///ppa_unittest.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.ppa_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.ppa_test_data)
        self.db = models.init_app(self.app)


    """ Test that privileges are defined and the model represents them correctly. """
    def test_privilegePersonAssignment_model(self):
        current = models.PrivilegePersonAssignment.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 5)
        self.assertEqual(current.memberFK, 1)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 6)
        self.assertEqual(current.memberFK, 1)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=3).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 7)
        self.assertEqual(current.memberFK, 2)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=4).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 8)
        self.assertEqual(current.memberFK, 3)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=5).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 5)
        self.assertEqual(current.memberFK, 4)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=6).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 6)
        self.assertEqual(current.memberFK, 4)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=7).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 7)
        self.assertEqual(current.memberFK, 3)


    """ Test that we can retieve a permission from the person-assignment. """
    def test_ppa_privilege_relationship(self):
        # Define prerequisite data.
        key = 5
        ppaKey = 1
        # Retrieve the target object directly.
        direct = models.Privilege.query.filter_by(pk=key).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, key)
        # Retrieve the containing object.
        host = models.PrivilegePersonAssignment.query.filter_by(pk=ppaKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.privilegeFK, direct.pk)
        # Retrieve the target object through the containing object.
        target = host.privilege
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())
    


    """ Test that we can retieve a member from the person-assignment. """
    def test_ppa_member_relationship(self):
        # Define prerequisite data.
        key = 1
        # Retrieve the target object directly.
        direct = models.Member.query.filter_by(pk=key).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, key)
        # Retrieve the containing object.
        host = models.PrivilegePersonAssignment.query.filter_by(pk=key).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.memberFK, direct.pk)
        # Retrieve the target object through the containing object.
        target = host.member
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())


    """ Test adding a Privilege to the database """
    def test_ppa_add(self):
        # Verify state of related tables before operation.
        privilegeCount = models.Privilege.query.count()
        ppaCount = models.PrivilegePersonAssignment.query.count()
        #gpaCount = models.GlobalPrivilegeAssignment.query.count()
        memberCount = models.Member.query.count()
        
        # Define prerequisite data.
        memberKey = 4
        privKey = 7
        target = models.PrivilegePersonAssignment(privilegeFK=privKey, memberFK=memberKey)

        # Verify that the data does not already exist.
        fetched = models.PrivilegePersonAssignment.query.filter_by(privilegeFK=privKey, memberFK=memberKey).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.PrivilegePersonAssignment.query.filter_by(privilegeFK=privKey, memberFK=memberKey)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.memberFK, memberKey)
            self.assertEqual(item.privilegeFK, privKey)
            count += 1
        self.assertEqual(count, 1)
        
        # Verify state of related tables before operation.
        privilegeCountAfter = models.Privilege.query.count()
        ppaCountAfter = models.PrivilegePersonAssignment.query.count()
        #gpaCountAfter = models.GlobalPrivilegeAssignment.query.count()
        memberCountAfter = models.Member.query.count()
        self.assertTrue(privilegeCountAfter == privilegeCount)        
        self.assertTrue(ppaCountAfter == ppaCount + 1)        
        #self.assertTrue(gpaCountAfter == gpaCountAfter)
        self.assertEqual(memberCount, memberCountAfter)


    """ Test deleting a privilege. """
    def test_ppa_delete(self):
        # Verify state of related tables before operation.
        privilegeCount = models.Privilege.query.count()
        ppaCount = models.PrivilegePersonAssignment.query.count()
        #gpaCount = models.GlobalPrivilegeAssignment.query.count()
        memberCount = models.Member.query.count()
        
        # Define required test data.
        memberKey = 4
        privKey = 5

        # Verify that prerequisite data exists.
        target = models.PrivilegePersonAssignment.query.filter_by(privilegeFK=privKey, memberFK=memberKey).first()
        self.assertIsNotNone(target)

        # Perform the operation.
        self.db.session.delete(target)
        self.db.session.commit()

        # Verify that the record has been removed.
        target = models.PrivilegePersonAssignment.query.filter_by(privilegeFK=privKey, memberFK=memberKey).first()
        self.assertIsNone(target)
        
        # Verify state of related tables before operation.
        privilegeCountAfter = models.Privilege.query.count()
        ppaCountAfter = models.PrivilegePersonAssignment.query.count()
        #gpaCountAfter = models.GlobalPrivilegeAssignment.query.count()
        memberCountAfter = models.Member.query.count()
        self.assertTrue(privilegeCountAfter == privilegeCount)        
        self.assertTrue(ppaCountAfter == ppaCount - 1)        
        #self.assertTrue(gpaCountAfter == gpaCountAfter)
        self.assertEqual(memberCount, memberCountAfter)

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(PrivilegePersonAssignmentTestCase('test_privilegePersonAssignment_model'))
    suite.addTest(PrivilegePersonAssignmentTestCase('test_ppa_privilege_relationship'))
    suite.addTest(PrivilegePersonAssignmentTestCase('test_ppa_member_relationship'))
    suite.addTest(PrivilegePersonAssignmentTestCase('test_ppa_add'))
    suite.addTest(PrivilegePersonAssignmentTestCase('test_ppa_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
