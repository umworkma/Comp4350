#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class PrivilegeTestCase(TestCase):
    database_uri = "sqlite:///privilege_unittest.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.privilege_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.privilege_test_data)
        self.db = models.init_app(self.app)


    """ Test that privileges are defined and the model represents them correctly. """
    def test_privilege_model(self):
        current = models.Privilege.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilege, 'REGISTER_NEW_ORGANIZATION')

        current = models.Privilege.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilege, 'MODIFY_ORGANIZATION')

        current = models.Privilege.query.filter_by(pk=3).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilege, 'DELETE_ORGANIZATION')

        current = models.Privilege.query.filter_by(pk=4).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilege, 'VIEW_ALL_ORGANIZATIONS')

        current = models.Privilege.query.filter_by(pk=5).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilege, 'VIEW_ALL_EMPLOYEES_IN_ORG')

        current = models.Privilege.query.filter_by(pk=6).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilege, 'ASSIGN_EMPS_TO_SHIFTS')

        current = models.Privilege.query.filter_by(pk=7).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilege, 'SOME_OTHER_EMP_PRIVILEGE')

        current = models.Privilege.query.filter_by(pk=8).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilege, 'YET_ANOTHER_EMP_PRIVILEGE')
        
        
    """ Test that we can retieve a person-assignments from a privilege. """
    def test_privilege_ppa_relationship(self):
        # Define prerequisite data.
        key = 5
        # Retrieve the target object directly.
        directList = models.PrivilegePersonAssignment.query.filter_by(privilegeFK=key)
        self.assertIsNotNone(directList)
        # Retrieve the containing object.
        host = models.Privilege.query.filter_by(pk=key).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, key)
        # Retrieve the target object through the containing object.
        targetList = host.ppaList
        count = 0
        for di,ti in zip(directList, targetList):
            count += 1
            self.assertEqual(di.__repr__(), ti.__repr__())
        self.assertEqual(count, 2)
        
        
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
        targetList = host.gpaList
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.personentityFK, ti.personentityFK)
            self.assertEqual(di.privilegeFK, ti.privilegeFK)
        self.assertGreater(resultCount, 0)

    
    """ Test adding a Privilege to the database """
    def test_privilege_add(self):
        # Verify state of related tables before operation.
        privilegeCount = models.Privilege.query.count()
        ppaCount = models.PrivilegePersonAssignment.query.count()
        gpaCount = models.GlobalPrivilegeAssignment.query.count()
        
        # Define prerequisite data.
        key = 'Test Priv add'
        target = models.Privilege(privilege=key)

        # Verify that the data does not already exist.
        fetched = models.Privilege.query.filter_by(privilege=key).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.Privilege.query.filter_by(privilege=key)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.privilege, key)
            count += 1
        self.assertEqual(count, 1)

        # Verify state of related tables before operation.
        privilegeCountAfter = models.Privilege.query.count()
        self.assertTrue(privilegeCountAfter == privilegeCount + 1)
        ppaCountAfter = models.PrivilegePersonAssignment.query.count()
        self.assertTrue(ppaCountAfter == ppaCount)
        gpaCountAfter = models.GlobalPrivilegeAssignment.query.count()
        self.assertTrue(gpaCountAfter == gpaCountAfter)
    

    
    """ Test updating an existing record. """
    def test_privilege_update(self):
        # Verify state of related tables before operation.
        privilegeCount = models.Privilege.query.count()
        ppaCount = models.PrivilegePersonAssignment.query.count()
        gpaCount = models.GlobalPrivilegeAssignment.query.count()
        
        # Define the required test data.
        keyBefore = 'SOME_OTHER_EMP_PRIVILEGE'
        keyAfter  = 'SOME_OTHER_EMP_PRIVILEGE after'

        # Verify the data exists.
        target = models.Privilege.query.filter_by(privilege=keyBefore).first()
        self.assertIsNotNone(target)
        self.assertEqual(target.privilege, keyBefore)

        # Update the key value
        target.privilege = keyAfter
        self.db.session.commit()

        # Verify that the data has changed.
        target = models.Privilege.query.filter_by(privilege=keyAfter).first()
        self.assertIsNotNone(target)
        self.assertEqual(target.privilege, keyAfter)

        # Verify that the original record does not exist.
        target = models.Privilege.query.filter_by(privilege=keyBefore).first()
        self.assertIsNone(target)

        # Verify state of related tables before operation.
        privilegeCountAfter = models.Privilege.query.count()
        self.assertTrue(privilegeCountAfter == privilegeCount)
        ppaCountAfter = models.PrivilegePersonAssignment.query.count()
        self.assertTrue(ppaCountAfter == ppaCount)
        gpaCountAfter = models.GlobalPrivilegeAssignment.query.count()
        self.assertTrue(gpaCountAfter == gpaCountAfter)
    
    
    """ Test deleting a privilege. """
    def test_privilege_delete(self):
        # Verify state of related tables before operation.
        privilegeCount = models.Privilege.query.count()
        ppaCount = models.PrivilegePersonAssignment.query.count()
        gpaCount = models.GlobalPrivilegeAssignment.query.count()
        
        # Define required test data.
        key = 'YET_ANOTHER_EMP_PRIVILEGE'
        target = models.Privilege(privilege=key)

        # Verify that prerequisite data exists.
        target = models.Privilege.query.filter_by(privilege=key).first()
        self.assertIsNotNone(target)

        # Perform the operation.
        self.db.session.delete(target)
        self.db.session.commit()

        # Verify that the record has been removed.
        target = models.Privilege.query.filter_by(privilege=key).first()
        self.assertIsNone(target)

        # Verify state of related tables before operation.
        privilegeCountAfter = models.Privilege.query.count()
        self.assertTrue(privilegeCountAfter == privilegeCount - 1)
        ppaCountAfter = models.PrivilegePersonAssignment.query.count()
        self.assertTrue(ppaCountAfter == ppaCount - 1)
        gpaCountAfter = models.GlobalPrivilegeAssignment.query.count()
        self.assertTrue(gpaCountAfter == gpaCountAfter)

        #self.resetDB()
    

def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(PrivilegeTestCase('test_privilege_model'))
    
    suite.addTest(PrivilegeTestCase('test_privilege_ppa_relationship'))
    suite.addTest(PrivilegeTestCase('test_privilege_gpa_relationship'))
    
    suite.addTest(PrivilegeTestCase('test_privilege_add'))
    suite.addTest(PrivilegeTestCase('test_privilege_update'))
    suite.addTest(PrivilegeTestCase('test_privilege_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
