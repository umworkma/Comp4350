#!../venv/bin/python
import unittest
import json

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models
import controller_privileges


class ControllerPrivilegesTestCase(TestCase):
    database_uri = "sqlite:///controller_privileges_unittest.db"
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


    def test__getPrivilegesForPerson(self):
        # Define prerequisite data.
        personKey = 3
        organizationKey = 1
        # Get the result of the tested method.
        privileges = controller_privileges._getPrivilegesForPerson(personKey, organizationKey)
        # Validate the result.
        self.assertIsNotNone(privileges)
        count = 0
        for priv in privileges:
            count += 1
            self.assertTrue(priv.pk is 5 or priv.pk is 6)
            self.assertTrue(priv.privilege == 'VIEW_ALL_EMPLOYEES_IN_ORG' or
                            priv.privilege == 'ASSIGN_EMPS_TO_SHIFTS')
        self.assertEqual(count, 2)



    def test__getOrgsWithPrivilegesForPerson(self):
        # Define prerequisite data.
        personKey = 4
        # Get the result of the tested method.
        orgKeys = controller_privileges._getOrgsWithPrivilegesForPerson(personKey=personKey)
        # Validate the result.
        self.assertIsNotNone(orgKeys)
        count = 0
        for value in orgKeys:
            count += 1
            self.assertTrue(value == 1 or value == 2)
        self.assertEqual(count, 2)



    def test__getGlobalPrivilegesForPerson(self):
        # Define prerequisite data.
        personKey = 3
        # Get the result of the tested method.
        privileges = controller_privileges._getGlobalPrivilegesForPerson(personKey)
        # Validate the result.
        self.assertIsNotNone(privileges)
        count = 0
        for priv in privileges:
            count += 1
            self.assertTrue(priv.pk is 1 or priv.pk is 4)
            self.assertTrue(priv.privilege == 'REGISTER_NEW_ORGANIZATION' or
                            priv.privilege == 'VIEW_ALL_ORGANIZATIONS')
        self.assertEqual(count, 2)



    def test__getOrgsWithPersonPrivilege(self):
        # Define prerequisite data.
        personKey = 4
        privilegeKey = 7
        # Get the restult of the tested method.
        orgKeys = controller_privileges._getOrgsWithPersonPrivilege(personKey=personKey,privilegeKey=privilegeKey)
        # Validate the result.
        self.assertIsNotNone(orgKeys)
        count = 0
        for value in orgKeys:
            count += 1
            self.assertTrue(value == 1 or value == 2)
        self.assertEqual(count, 2)



    def test__grantPrivilegeToPerson_Global(self):
        #self.resetDB()

        # Sub-Test 1: Invalid person key.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 9999
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 2: Invalid privilege key.
        # Define prerequisite data.
        privilegeKey = 9999
        personKey = 5
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 3: Valid execution.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 5
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 4: Duplicate permission.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 5
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertTrue(result)

    def test__grantPrivilegeToPerson_Person(self):
        #self.resetDB()

        # Sub-Test 1: Invalid person key.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 9999
        organizationKey = 1
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 2: Invalid privilege key.
        # Define prerequisite data.
        privilegeKey = 9999
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 3: Invalid organization key.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 4
        organizationKey = 9999
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 4: Valid execution.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 5: Duplicate permission.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 6: Duplicate permission, but different organization.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 4
        organizationKey = 2
        # Get the result of the tested method.
        result = controller_privileges._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

    def test__revokePrivilegeForPerson_Global(self):
        # Sub-Test 1: Invalid person key.
        # Define prerequisite data.
        privilegeKey = 4
        personKey = 9999
        # Get the result of the tested method.
        result = controller_privileges._revokePrivilegeForPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 2: Invalid privilege key.
        # Define prerequisite data.
        privilegeKey = 9999
        personKey = 4
        # Get the result of the tested method.
        result = controller_privileges._revokePrivilegeForPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 3: Valid execution.
        # Define prerequisite data.
        privilegeKey = 4
        personKey = 4
        # Get the result of the tested method.
        result = controller_privileges._revokePrivilegeForPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 4: Duplicate permission.
        # Define prerequisite data.
        privilegeKey = 4
        personKey = 4
        # Get the result of the tested method.
        result = controller_privileges._revokePrivilegeForPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertTrue(result)

        #self.resetDB()

    def test__revokePrivilegeForPerson_Person(self):
        # Sub-Test 1: Invalid person key.
        # Define prerequisite data.
        privilegeKey = 7
        personKey = 9999
        organizationKey = 1
        # Get the result of the tested method.
        result = controller_privileges._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 2: Invalid privilege key.
        # Define prerequisite data.
        privilegeKey = 9999
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controller_privileges._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 3: Invalid organization key.
        # Define prerequisite data.
        privilegeKey = 7
        personKey = 4
        organizationKey = 9999
        # Get the result of the tested method.
        result = controller_privileges._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 4: Valid execution.
        # Define prerequisite data.
        privilegeKey = 7
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controller_privileges._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 5: Duplicate permission.
        # Define prerequisite data.
        privilegeKey = 7
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controller_privileges._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

        #self.resetDB()
        
        
def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(ControllerPrivilegesTestCase('test__getPrivilegesForPerson'))
    suite.addTest(ControllerPrivilegesTestCase('test__getOrgsWithPrivilegesForPerson'))
    suite.addTest(ControllerPrivilegesTestCase('test__getGlobalPrivilegesForPerson'))
    suite.addTest(ControllerPrivilegesTestCase('test__getOrgsWithPersonPrivilege'))
    suite.addTest(ControllerPrivilegesTestCase('test__grantPrivilegeToPerson_Global'))
    suite.addTest(ControllerPrivilegesTestCase('test__grantPrivilegeToPerson_Person'))
    suite.addTest(ControllerPrivilegesTestCase('test__revokePrivilegeForPerson_Global'))
    suite.addTest(ControllerPrivilegesTestCase('test__revokePrivilegeForPerson_Person'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
