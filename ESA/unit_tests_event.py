#!../venv/bin/python
import unittest
import json

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models
import events
import datetime

class EventTestCase(TestCase):
    database_uri = "sqlite:///event_unittest.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.event_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.event_test_data)
        self.db = models.init_app(self.app)


    """ Test that members are defined and the model represents them correctly. """
    def test_event_model(self):
        current = models.Event.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.name, 'My Event')
        self.assertEqual(current.description, 'This is my event')
        self.assertEqual(current.organizationFK, 1)

        current = models.Event.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.name, 'Your Event')
        self.assertEqual(current.description, 'This is your event')
        self.assertEqual(current.organizationFK, 2)

    """ Test that an event can be retrieved from an organization relationship """
    def test_event_organization_relationship(self):        
        # Define prerequisite data.
        eventKey = 1
        orgKey = 1
        name = 'My Event'
        # Retrieve the target object directly.
        direct = models.Organization.query.filter_by(entityFK=orgKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Event.query.filter_by(pk=eventKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, eventKey)
        self.assertEqual(host.organizationFK, orgKey)
        # Retrieve the target object through the containing object.
        target = host.organization
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())

    def test_event_add(self):
        # Verify state of related tables before operation.
        eventCount = models.Event.query.count()
        
        # Define prerequisite data.
        name = 'new event'
        desc = 'new description'
        orgFK = 1
        target = models.Event(name, desc, datetime.datetime.now(), datetime.datetime.now(), orgFK)

        # Verify that the data does not already exist.
        fetched = models.Event.query.filter_by(name=name, description=desc).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.Event.query.filter_by(name=name, description=desc)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.name, target.name)
            self.assertEqual(item.description, target.description)
            count += 1
        self.assertEqual(count, 1)

        # Verify state of related tables after the operation.
        eventCountAfter = models.Event.query.count()
        self.assertTrue(eventCountAfter == eventCount + 1)

    def test_extractEventFromDict(self):
        control = models.Event.query.first()
        stringJSON = '{"event_pk":1, "event_name":"My Event", "event_desc":"This is my event", "event_orgfk":1}'
        data = json.loads(stringJSON)
        target = events.extractEventFromDict(data)

        self.assertEqual(control.pk, target.pk)
        self.assertEqual(control.name, target.name)
        self.assertEqual(control.description, target.description)
        self.assertEqual(control.organizationFK, target.organizationFK)

def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(EventTestCase('test_event_model'))
    suite.addTest(EventTestCase('test_event_organization_relationship'))
    suite.addTest(EventTestCase('test_event_add'))
    suite.addTest(EventTestCase('test_extractEventFromDict'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

