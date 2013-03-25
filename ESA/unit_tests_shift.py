#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models
import datetime

class ShiftTestCase(TestCase):
    database_uri = "sqlite:///shift_unittest.db"
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


    """ Test that shifts are defined and the model represents them correctly. """
    def test_shift_model(self):
        current = models.Shift.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.eventFK, 1)
        self.assertEqual(current.startdatetime, datetime.datetime(2013, 7, 12, 12, 0))
        self.assertEqual(current.enddatetime, datetime.datetime(2013, 7, 12, 13, 0))
        self.assertEqual(current.location, 'Booth A')
        self.assertEqual(current.minWorkers, 2)
        self.assertEqual(current.maxWorkers, 4)

        current = models.Shift.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.eventFK, 1)
        self.assertEqual(current.startdatetime, datetime.datetime(2013, 7, 12, 13, 0))
        self.assertEqual(current.enddatetime, datetime.datetime(2013, 7, 12, 14, 0))
        self.assertEqual(current.location, 'Booth A')
        self.assertEqual(current.minWorkers, 2)
        self.assertEqual(current.maxWorkers, 4)

        current = models.Shift.query.filter_by(pk=3).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.eventFK, 1)
        self.assertEqual(current.startdatetime, datetime.datetime(2013, 7, 12, 14, 0))
        self.assertEqual(current.enddatetime, datetime.datetime(2013, 7, 12, 15, 0))
        self.assertEqual(current.location, 'Booth A')
        self.assertEqual(current.minWorkers, 3)
        self.assertEqual(current.maxWorkers, 4)

        current = models.Shift.query.filter_by(pk=4).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.eventFK, 1)
        self.assertEqual(current.startdatetime, datetime.datetime(2013, 7, 12, 15, 0))
        self.assertEqual(current.enddatetime, datetime.datetime(2013, 7, 12, 16, 0))
        self.assertEqual(current.location, 'Booth A')
        self.assertEqual(current.minWorkers, 3)
        self.assertEqual(current.maxWorkers, 4)


    """ Test that we can retieve an event from the shift. """
    def test_shift_event_relationship(self):
        # Define prerequisite data.
        eventKey = 1
        shiftKey = 2
        # Retrieve the target object directly.
        direct = models.Event.query.filter_by(pk=eventKey).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, eventKey)
        # Retrieve the containing object.
        host = models.Shift.query.filter_by(pk=shiftKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.eventFK, direct.pk)
        # Retrieve the target object through the containing object.
        target = host.event
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())
    


    """ Test that we can retieve shift assignments (to a person) from the shift. """
    """def test_shift_personbridge_relationship(self):
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
        self.assertEqual(direct.__repr__(), target.__repr__())"""


    """ Test adding a Shift to the database """
    def test_shift_add(self):
        # Verify state of related tables before operation.
        eventCount = models.Event.query.count()
        shiftCount = models.Shift.query.count()
        
        # Define prerequisite data.
        eventKey=1
        start=datetime.datetime(2013, 7, 13, 12, 0)
        end=datetime.datetime(2013, 7, 13, 13, 0)
        location='Booth A'
        minWorkers=2
        maxWorkers=4
        target = models.Shift(eventFK=eventKey, startdatetime=start, enddatetime=end, location=location, minWorkers=minWorkers, maxWorkers=maxWorkers)

        # Verify that the data does not already exist.
        fetched = models.Shift.query.filter_by(eventFK=eventKey, startdatetime=start, enddatetime=end, location=location).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.Shift.query.filter_by(eventFK=eventKey, startdatetime=start, enddatetime=end, location=location)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.eventFK, eventKey)
            self.assertEqual(item.startdatetime, start)
            self.assertEqual(item.enddatetime, end)
            self.assertEqual(item.location, location)
            self.assertEqual(item.minWorkers, minWorkers)
            self.assertEqual(item.maxWorkers, maxWorkers)
            count += 1
        self.assertEqual(count, 1)
        
        # Verify state of related tables before operation.
        eventCountAfter = models.Event.query.count()
        shiftCountAfter = models.Shift.query.count()
        self.assertTrue(eventCountAfter == eventCount)        
        self.assertTrue(shiftCountAfter == shiftCount + 1)


    """ Test deleting a shift. """
    def test_shift_delete(self):
        # Verify state of related tables before operation.
        eventCount = models.Event.query.count()
        shiftCount = models.Shift.query.count()
        
        # Define required test data.
        key = 4

        # Verify that prerequisite data exists.
        target = models.Shift.query.filter_by(pk=key).first()
        self.assertIsNotNone(target)

        # Perform the operation.
        self.db.session.delete(target)
        self.db.session.commit()

        # Verify that the record has been removed.
        target = models.Shift.query.filter_by(pk=key).first()
        self.assertIsNone(target)
        
        # Verify state of related tables before operation.
        eventCountAfter = models.Event.query.count()
        shiftCountAfter = models.Shift.query.count()
        self.assertTrue(eventCountAfter == eventCount)
        self.assertTrue(shiftCountAfter == shiftCount - 1)


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(ShiftTestCase('test_shift_model'))
    suite.addTest(ShiftTestCase('test_shift_event_relationship'))
    #suite.addTest(ShiftTestCase('test_shift_personbridge_relationship'))
    suite.addTest(ShiftTestCase('test_shift_add'))
    suite.addTest(ShiftTestCase('test_shift_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
