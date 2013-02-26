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
        direct = models.Privilege.query.filter_by(pk=5).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, 5)

        host = models.PrivilegePersonAssignment.query.filter_by(pk=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.privilegeFK, direct.pk)

        target = host.privilege
        self.assertIsNotNone(target)
        self.assertEqual(target.pk, direct.pk)
        self.assertEqual(target.privilege, direct.privilege)
    """ Test that we can retieve a person-assignments from a privilege. """
    def test_privilege_ppa_relationship(self):
        directList = models.PrivilegePersonAssignment.query.filter_by(privilegeFK=5)
        self.assertIsNotNone(directList)

        host = models.Privilege.query.filter_by(pk=5).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, 5)

        targetList = host.ppaList
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.memberFK, ti.memberFK)
            self.assertEqual(di.privilegeFK, ti.privilegeFK)
        self.assertGreater(resultCount, 0)


    """ Test that we can retieve a member from the person-assignment. """
    def test_ppa_member_relationship(self):
        direct = models.Member.query.filter_by(pk=1).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, 1)

        host = models.PrivilegePersonAssignment.query.filter_by(pk=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.memberFK, direct.pk)

        target = host.member
        self.assertIsNotNone(target)
        self.assertEqual(target.pk, direct.pk)
        self.assertEqual(target.personentityFK, direct.personentityFK)
        self.assertEqual(target.organizationentityFK, direct.organizationentityFK)
    """ Test that we can retieve a person-assignments from a member. """
    def test_member_ppa_relationship(self):
        directList = models.PrivilegePersonAssignment.query.filter_by(memberFK=1)
        self.assertIsNotNone(directList)

        host = models.Member.query.filter_by(pk=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, 1)

        targetList = host.memberPrivileges
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.memberFK, ti.memberFK)
            self.assertEqual(di.privilegeFK, ti.privilegeFK)
        self.assertGreater(resultCount, 0)


    """ Test adding a Privilege to the database """
    def test_ppa_add(self):
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


    """ Test deleting a privilege. """
    def test_ppa_delete(self):
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

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(PrivilegePersonAssignmentTestCase('test_privilegePersonAssignment_model'))
    suite.addTest(PrivilegePersonAssignmentTestCase('test_ppa_privilege_relationship'))
    suite.addTest(PrivilegePersonAssignmentTestCase('test_privilege_ppa_relationship'))
    suite.addTest(PrivilegePersonAssignmentTestCase('test_ppa_member_relationship'))
    suite.addTest(PrivilegePersonAssignmentTestCase('test_member_ppa_relationship'))
    suite.addTest(PrivilegePersonAssignmentTestCase('test_ppa_add'))

    # Tests that must be run last b/c they delete from the DB.
    # Since we aren't resetting, they might remove info other tests need.
    # If we chose to call resetDB() after any of these tests, they
    # could be moved up to the previous section, but they would
    # take a little bit longer to run.
    suite.addTest(PrivilegePersonAssignmentTestCase('test_ppa_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
