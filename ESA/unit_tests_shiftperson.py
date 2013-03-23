#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class ShiftPersonTestCase(TestCase):
    database_uri = "sqlite:///shiftperson_unittest.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.shift_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.shift_test_data)
        self.db = models.init_app(self.app)


    """ Test that shift_person relationships are defined and the model represents them correctly. """
    def test_shiftperson_model(self):
        current = models.ShiftPerson.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.shiftFK, 1)
        self.assertEqual(current.shiftFK, 3)
        
        current = models.ShiftPerson.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.shiftFK, 1)
        self.assertEqual(current.shiftFK, 4)
        
        current = models.ShiftPerson.query.filter_by(pk=3).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.shiftFK, 2)
        self.assertEqual(current.shiftFK, 4)
        
        current = models.ShiftPerson.query.filter_by(pk=4).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.shiftFK, 2)
        self.assertEqual(current.shiftFK, 5)
        
        current = models.ShiftPerson.query.filter_by(pk=5).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.shiftFK, 3)
        self.assertEqual(current.shiftFK, 3)
        
        current = models.ShiftPerson.query.filter_by(pk=6).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.shiftFK, 3)
        self.assertEqual(current.shiftFK, 5)
        
        current = models.ShiftPerson.query.filter_by(pk=7).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.shiftFK, 4)
        self.assertEqual(current.shiftFK, 3)
        
        current = models.ShiftPerson.query.filter_by(pk=8).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.shiftFK, 4)
        self.assertEqual(current.shiftFK, 4)
        
        current = models.ShiftPerson.query.filter_by(pk=9).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.shiftFK, 4)
        self.assertEqual(current.shiftFK, 5)


    """ Test that we can retieve the shift from the shift-person assignment. """
    def test_shiftperson_shift_relationship(self):
        # Define prerequisite data.
        key = 7
        personKey = 3
        # Retrieve the target object directly.
        direct = models.Person.query.filter_by(pk=personKey).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, key)
        # Retrieve the containing object.
        host = models.ShiftPerson.query.filter_by(pk=key).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.personFK, direct.entityFK)
        # Retrieve the target object through the containing object.
        target = host.person
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())


    """ Test adding a Shift-Person assignment to the database """
    def test_shiftperson_add(self):
        # Verify state of related tables before operation.
        shiftPersonCount = models.ShiftPerson.query.count()
        shiftCount = models.Shift.query.count()
        personCount = models.Person.query.count()
        
        # Define prerequisite data.
        shiftKey=1
        personKey=5
        target = models.ShiftPerson(shiftKey=shiftKey, personKey=personKey)

        # Verify that the data does not already exist.
        fetched = models.ShiftPerson.query.filter_by(shiftKey=shiftKey, personKey=personKey).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.ShiftPerson.query.filter_by(shiftKey=shiftKey, personKey=personKey)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.shiftKey, shiftKey)
            self.assertEqual(item.personKey, personKey)
            count += 1
        self.assertEqual(count, 1)
        
        # Verify state of related tables before operation.
        shiftPersonCountAfter = models.ShiftPerson.query.count()
        shiftCountAfter = models.Shift.query.count()
        personCountAfter = models.Person.query.count()
        self.assertTrue(shiftPersonCountAfter == shiftPersonCount + 1)        
        self.assertTrue(shiftCountAfter == shiftCount)
        self.assertTrue(personCountAfter == personCount)


    """ Test deleting a shift-person assignment. """
    def test_shiftperson_delete(self):
        # Verify state of related tables before operation.
        shiftPersonCount = models.ShiftPerson.query.count()
        shiftCount = models.Shift.query.count()
        personCount = models.Person.query.count()
        
        # Define required test data.
        key = 9

        # Verify that prerequisite data exists.
        target = models.ShiftPerson.query.filter_by(pk=key).first()
        self.assertIsNotNone(target)

        # Perform the operation.
        self.db.session.delete(target)
        self.db.session.commit()

        # Verify that the record has been removed.
        target = models.ShiftPerson.query.filter_by(pk=key).first()
        self.assertIsNone(target)
        
        # Verify state of related tables before operation.
        shiftPersonCountAfter = models.ShiftPerson.query.count()
        shiftCountAfter = models.Shift.query.count()
        personCountAfter = models.Person.query.count()
        self.assertTrue(shiftPersonCountAfter == shiftPersonCount - 1)        
        self.assertTrue(shiftCountAfter == shiftCount)
        self.assertTrue(personCountAfter == personCount)


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(ShiftPersonTestCase('test_shiftperson_model'))
    suite.addTest(ShiftPersonTestCase('test_shiftperson_shift_relationship'))
    suite.addTest(ShiftPersonTestCase('test_shiftperson_add'))
    suite.addTest(ShiftPersonTestCase('test_shiftperson_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
