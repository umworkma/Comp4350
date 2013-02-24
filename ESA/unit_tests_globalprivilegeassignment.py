#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class GlobalPrivilegeAssignmentTestCase(TestCase):
    database_uri = "sqlite:///gpa_unittest.db"
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


    """ Test that global privilege assignments are defined and the model represents them correctly. """
    def test_globalPrivilegeAssignment_model(self):
        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 1)
        self.assertEqual(current.personentityFK, 3)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 4)
        self.assertEqual(current.personentityFK, 3)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=3).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 3)
        self.assertEqual(current.personentityFK, 4)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=4).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 4)
        self.assertEqual(current.personentityFK, 4)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=5).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 2)
        self.assertEqual(current.personentityFK, 5)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=6).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 4)
        self.assertEqual(current.personentityFK, 5)


    """ Test that we can retieve a privilege from the global privilege assignment relationship. """
    def test_gpa_privilege_relationship(self):
        # Define prerequisite data.
        privKey = 4
        gpaKey = 2

        # Retrieve the target object directly.
        direct = models.Privilege.query.filter_by(pk=privKey).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, privKey)

        # Retrieve the containing object.
        host = models.GlobalPrivilegeAssignment.query.filter_by(pk=gpaKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.privilegeFK, direct.pk)

        # Retrieve the target object through the containing object.
        target = host.privilege
        self.assertIsNotNone(target)
        self.assertEqual(target.pk, direct.pk)
        self.assertEqual(target.privilege, direct.privilege)
    """ Test that we can retieve a global privilege assignment from a privilege relationship. """
    def test_privilege_gpa_relationship(self):
        # Define prerequisite data.
        gpaKey = 3
        privKey = 4

        # Retrieve all objects associated with the containing object directly.
        directList = models.GlobalPrivilegeAssignment.query.filter_by(privilegeFK=privKey)
        self.assertIsNotNone(directList)

        # Retrieve the containing object.
        host = models.Privilege.query.filter_by(pk=privKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, privKey)

        # Retrieve all associated objects through the containing object.
        targetList = host.privilegedGlobalPeople
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.personentityFK, ti.personentityFK)
            self.assertEqual(di.privilegeFK, ti.privilegeFK)
        self.assertGreater(resultCount, 0)


    """ Test that we can retieve a person from the global privilege assignment. """
    def test_gpa_person_relationship(self):
        direct = models.Person.query.filter_by(entityFK=5).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.entityFK, 5)

        host = models.GlobalPrivilegeAssignment.query.filter_by(pk=5).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.personentityFK, direct.entityFK)

        target = host.person
        self.assertIsNotNone(target)
        self.assertEqual(target.entityFK, direct.entityFK)
        self.assertEqual(target.firstname, direct.firstname)
        self.assertEqual(target.lastname, direct.lastname)
    """ Test that we can retieve global privilege assignments from a person. """
    def test_person_gpa_relationship(self):
        directList = models.GlobalPrivilegeAssignment.query.filter_by(personentityFK=5)
        self.assertIsNotNone(directList)

        host = models.Person.query.filter_by(entityFK=5).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, 5)

        targetList = host.personGlobalPrivileges
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.personentityFK, ti.personentityFK)
            self.assertEqual(di.privilegeFK, ti.privilegeFK)
        self.assertGreater(resultCount, 0)


    """ Test adding a global privilege assignment to the database """
    def test_gpa_add(self):
        # Define prerequisite data.
        personKey = 5
        privKey = 1
        target = models.GlobalPrivilegeAssignment(privilegeFK=privKey, personentityFK=personKey)

        # Verify that the data does not already exist.
        fetched = models.GlobalPrivilegeAssignment.query.filter_by(privilegeFK=privKey, personentityFK=personKey).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.GlobalPrivilegeAssignment.query.filter_by(privilegeFK=privKey, personentityFK=personKey)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.personentityFK, personKey)
            self.assertEqual(item.privilegeFK, privKey)
            count += 1
        self.assertEqual(count, 1)


    """ Test deleting a global privilege assignment. """
    def test_gpa_delete(self):
        # Define required test data.
        personKey = 3
        privKey = 1

        # Verify that prerequisite data exists.
        target = models.GlobalPrivilegeAssignment.query.filter_by(privilegeFK=privKey, personentityFK=personKey).first()
        self.assertIsNotNone(target)

        # Perform the operation.
        self.db.session.delete(target)
        self.db.session.commit()

        # Verify that the record has been removed.
        target = models.GlobalPrivilegeAssignment.query.filter_by(privilegeFK=privKey, personentityFK=personKey).first()
        self.assertIsNone(target)

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(GlobalPrivilegeAssignmentTestCase('test_globalPrivilegeAssignment_model'))
    suite.addTest(GlobalPrivilegeAssignmentTestCase('test_gpa_privilege_relationship'))
    suite.addTest(GlobalPrivilegeAssignmentTestCase('test_privilege_gpa_relationship'))
    suite.addTest(GlobalPrivilegeAssignmentTestCase('test_gpa_person_relationship'))
    suite.addTest(GlobalPrivilegeAssignmentTestCase('test_person_gpa_relationship'))
    suite.addTest(GlobalPrivilegeAssignmentTestCase('test_gpa_add'))

    # Tests that must be run last b/c they delete from the DB.
    # Since we aren't resetting, they might remove info other tests need.
    # If we chose to call resetDB() after any of these tests, they
    # could be moved up to the previous section, but they would
    # take a little bit longer to run.
    suite.addTest(GlobalPrivilegeAssignmentTestCase('test_gpa_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
