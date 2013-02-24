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


    """ Test adding a Privilege to the database """
    def test_privilege_add(self):
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


    """ Test updating an existing record. """
    def test_privilege_update(self):
        # Define the required test data.
        keyBefore = 'SOME_OTHER_EMP_PRIVILEGE'
        keyAfter  = 'SOME_OTHER_EMP_PRIVILEGE after'
        target = models.Privilege(privilege=keyBefore)

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


    """ Test deleting a privilege. """
    def test_privilege_delete(self):
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

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(PrivilegeTestCase('test_privilege_model'))
    suite.addTest(PrivilegeTestCase('test_privilege_add'))
    suite.addTest(PrivilegeTestCase('test_privilege_update'))

    # Tests that must be run last b/c they delete from the DB.
    # Since we aren't resetting, they might remove info other tests need.
    # If we chose to call resetDB() after any of these tests, they
    # could be moved up to the previous section, but they would
    # take a little bit longer to run.
    suite.addTest(PrivilegeTestCase('test_privilege_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
