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


    ''' Test functionality to get Event by ID in events.py '''
    def test__getEventByID(self):
        event = events._getEventByID(1)
        self.assertIsNotNone(event)
        self.assertEqual(event.name, 'My Event')
        self.assertEqual(event.description, 'This is my event')
        self.assertEqual(event.organizationFK, 1)

        event = events._getEventByID(2)
        self.assertIsNotNone(event)
        self.assertEqual(event.name, 'Your Event')
        self.assertEqual(event.description, 'This is your event')
        self.assertEqual(event.organizationFK, 2)

        event = events._getEventByID(3)
        self.assertIsNone(event)
        
        
    def test__getEventsByOrg_true(self):
        key = 1
        eventList = events._getEventsByOrg(key)
        self.assertEqual(eventList.count(), 1);
        for event in eventList:
            self.assertEqual(event.pk, 1)
            self.assertEqual(event.name, 'My Event')
            self.assertEqual(event.description, 'This is my event')
            self.assertEqual(event.organizationFK, key)
            
    def test__getEventsByOrg_false(self):
        key = 999
        eventList = events._getEventsByOrg(key)
        self.assertEqual(eventList.count(), 0);
        
        
    def test_getEventsByOrg_true(self):
        key = 1
        eventListJSON = events.getEventsByOrgJSON(key)
        eventListDict = json.loads(eventListJSON)
        for rootKey, rootVal in eventListDict.iteritems():
            self.assertEqual(rootKey, 'Events')
            counter = 0
            for eventJSON in rootVal:
                counter += 1
                event = events.extractEventFromDict(eventJSON)
                self.assertEqual(event.pk, 1)
                self.assertEqual(event.name, 'My Event')
                self.assertEqual(event.description, 'This is my event')
                self.assertEqual(event.organizationFK, key)
            self.assertEqual(counter, 1)
            
    def test_getEventsByOrg_false(self):
        key = 999
        eventListJSON = events.getEventsByOrgJSON(key)
        eventListDict = json.loads(eventListJSON)
        for rootKey, rootVal in eventListDict.iteritems():
            self.assertEqual(rootKey, 'Events')
            self.assertEqual(rootVal, 'None')
        
    
    ''' Test method in events.py '''
    def test_extractEventFromDict(self):
        control = models.Event.query.first()
        stringJSON = '{"event_pk":1, "event_name":"My Event", "event_desc":"This is my event", "event_start":"2013-07-12 12:00:00", "event_end":"2013-07-14 16:00:00", "event_orgfk":1}'
        data = json.loads(stringJSON)
        target = events.extractEventFromDict(data)

        self.assertEqual(control.pk, target.pk)
        self.assertEqual(control.name, target.name)
        self.assertEqual(control.description, target.description)
        self.assertEqual(control.startdate, target.startdate)
        self.assertEqual(control.enddate, target.enddate)
        self.assertEqual(control.organizationFK, target.organizationFK)
        
    ''' Test method in events.py '''
    def test_extractEventFromDict_incomplete(self):
        control = models.Event()
        control.name = "D Event 3"
        control.startdate = datetime.datetime(2013, 3, 22)
        control.enddate = datetime.datetime(2013, 3, 22)
        control.organizationFK = 4
        
        #stringJSON = '{"event_name":"test_extractEventFromDict_incomplete event", "event_desc":"test_extractEventFromDict_incomplete description is indescribable", "event_start":"2013-03-28 17:30:00", "event_end":"2013-03-28 20:00:00"}'
        stringJSON = '{"event_name":"D Event 3","event_start":"03/22/2013","event_end":"03/22/2013","event_orgfk":4}'
        data = json.loads(stringJSON)
        target = events.extractEventFromDict(data)

        self.assertEqual(control.pk, target.pk)
        self.assertEqual(control.name, target.name)
        self.assertEqual(control.description, target.description)
        self.assertEqual(control.startdate, target.startdate)
        self.assertEqual(control.enddate, target.enddate)
        self.assertEqual(control.organizationFK, target.organizationFK)
    
    ''' Test method from events.py '''
    def test__isDuplicateEvent_true(self):
        event1 = models.Event.query.first()
        
        event2 = models.Event()
        event2.name = event1.name
        event2.startdate = event1.startdate
        event2.enddate = event1.enddate
        event2.organizationFK = event1.organizationFK
        
        result = events._isDuplicateEvent(event2)
        self.assertTrue(result)
        
        
    ''' Test method from events.py '''
    def test__isDuplicateEvent_false(self):
        event1 = models.Event.query.first()

        event2 = models.Event()
        event2.name = event1.name + 'differenttext'
        event2.startdate = event1.startdate
        event2.enddate = event1.enddate
        event2.organizationFK = event1.organizationFK

        result = events._isDuplicateEvent(event2)
        self.assertFalse(result)
        
    ''' Test method from events.py '''
    def test__insertEvent_true(self):
        event = models.Event()
        name = 'test__insertEvent_true event'
        desc = 'description of test__insertEvent_true event is indescribable'
        start = datetime.datetime(2013, 3, 20, 1, 0)
        end = datetime.datetime(2013, 3, 20, 2, 0)
        orgFK = 1
        
        event.name = name
        event.description = desc
        event.startdate = start
        event.enddate = end
        event.organizationFK = orgFK
        
        result = events._insertEvent(event, self.db)
        self.assertTrue(result > 0)
        
        newEvent = models.Event.query.filter_by(pk=result).first()
        self.assertEqual(newEvent.pk, result)
        self.assertEqual(newEvent.name, name)
        self.assertEqual(newEvent.description, desc)
        self.assertEqual(newEvent.startdate, start)
        self.assertEqual(newEvent.enddate, end)
        self.assertEqual(newEvent.organizationFK, orgFK)
        
        
    ''' Test method from events.py '''
    def test__insertEvent_duplicate(self):
        event = models.Event()
        name='My Event'
        desc='This is my event'
        start=datetime.datetime(2013, 7, 12, 12, 0)
        end=datetime.datetime(2013, 7, 14, 16, 0)
        orgFK=1

        event.name = name
        event.description = desc
        event.startdate = start
        event.enddate = end
        event.organizationFK = orgFK

        result = events._insertEvent(event, self.db)
        self.assertEqual(result, 'Duplicate')
        
    ''' Test method from events.py '''
    def test__insertEvent_badorg(self):
        event = models.Event()
        name='My Event'
        desc='This is my event'
        start=datetime.datetime(2013, 7, 12, 12, 0)
        end=datetime.datetime(2013, 7, 14, 16, 0)
        orgFK=0

        event.name = name
        event.description = desc
        event.startdate = start
        event.enddate = end
        event.organizationFK = orgFK

        result = events._insertEvent(event, self.db)
        self.assertEqual(result, 'BadOrg')
        
    ''' Test method from events.py '''    
    def test_insertEvent_true(self):
        name='test_insertEvent_true event'
        desc='description of test_insertEvent_true event is indescribable'
        start=datetime.datetime(2013, 7, 12, 12, 0)
        end=datetime.datetime(2013, 7, 14, 16, 0)
        orgFK=1
        
        eventJSON = '{' + '"{key}":"{val}",'.format(key=models.EVENT_NAME_KEY, val=name)
        eventJSON += '"{key}":"{val}",'.format(key=models.EVENT_DESC_KEY, val=desc)
        eventJSON += '"{key}":"{val}",'.format(key=models.EVENT_START_KEY, val=start)
        eventJSON += '"{key}":"{val}"'.format(key=models.EVENT_END_KEY, val=end)
        eventJSON += '}'
        eventDict = json.loads(eventJSON)
        
        result = events.insertEvent(orgFK, eventDict, self.db)
        self.assertIsNotNone(result)
        newKey = 0
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'true')
            if key == models.EVENT_PK_KEY:
                self.assertTrue(value > 0)
                newKey = value
        
        newEvent = models.Event.query.filter_by(pk=newKey).first()
        self.assertEqual(newEvent.pk, newKey)
        self.assertEqual(newEvent.name, name)
        self.assertEqual(newEvent.description, desc)
        self.assertEqual(newEvent.startdate, start)
        self.assertEqual(newEvent.enddate, end)
        self.assertEqual(newEvent.organizationFK, orgFK)
        
        
    ''' Test method from events.py '''    
    def test_insertEvent_duplicate(self):
        event1 = models.Event.query.first()
        name=event1.name
        desc=event1.description
        start=event1.startdate
        end=event1.enddate
        orgFK=event1.organizationFK
        
        event2 = models.Event()
        event2.name = name
        event2.description = desc
        event2.startdate = start
        event2.enddate = end
        eventJSON = events.eventToJSON(event2)
        eventDict = json.loads(eventJSON)
        
        result = events.insertEvent(orgFK, eventDict, self.db)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'false')
            if key == 'msg':
                self.assertEqual(value, 'Duplicate')
            if key == 'event_pk':
                self.assertEqual(value, 'None')
        
    ''' Test method from events.py '''    
    def test_insertEvent_badorg(self):
        name='test_insertEvent_badorg event'
        desc='description of test_insertEvent_badorg event is indescribable'
        start=datetime.datetime(2013, 7, 12, 12, 0)
        end=datetime.datetime(2013, 7, 14, 16, 0)
        orgFK=99999
        
        eventJSON = '{' + '"{key}":"{val}",'.format(key=models.EVENT_NAME_KEY, val=name)
        eventJSON += '"{key}":"{val}",'.format(key=models.EVENT_DESC_KEY, val=desc)
        eventJSON += '"{key}":"{val}",'.format(key=models.EVENT_START_KEY, val=start)
        eventJSON += '"{key}":"{val}"'.format(key=models.EVENT_END_KEY, val=end)
        eventJSON += '}'
        eventDict = json.loads(eventJSON)
        
        result = events.insertEvent(orgFK, eventDict, self.db)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'false')
            if key == 'msg':
                self.assertEqual(value, 'BadOrg')
            elif key == 'event_pk':
                self.assertEqual(value, 'None')        

                
    ''' Test method in events.py '''
    def test__removeEvent_true(self):
        # Define the values we're going to have to add for the test.
        newEvent = models.Event()
        name = 'test__removeEvent_true event'
        desc = 'description of test__removeEvent_true event is indescribable'
        start = datetime.datetime(2013, 3, 20, 1, 0)
        end = datetime.datetime(2013, 3, 20, 2, 0)
        orgFK = 1
        newEvent.name = name
        newEvent.description = desc
        newEvent.startdate = start
        newEvent.enddate = end
        newEvent.organizationFK = orgFK
        
        # Ensure it's not already in db.
        result = events._isDuplicateEvent(newEvent)
        self.assertFalse(result)
        
        # Add it to db
        newEventPK = events._insertEvent(newEvent, self.db)
        self.assertTrue(newEventPK > 0)
        
        # Ensure it's in db.
        result = events._isDuplicateEvent(newEvent)
        self.assertTrue(result)
        
        # Now that we added it, lets delete it.
        result = events._removeEvent(newEventPK, self.db)
        self.assertTrue(result)
        
        # Ensure it's not in db.
        result = events._isDuplicateEvent(newEvent)
        self.assertFalse(result)
        
    ''' Test method in events.py '''
    def test__removeEvent_invalid(self):
        # Define the values we're going to have to add for the test.
        newEvent = models.Event()
        name = 'test__removeEvent_invalid event'
        desc = 'description of test__removeEvent_invalid event is indescribable'
        start = datetime.datetime(2013, 3, 20, 1, 0)
        end = datetime.datetime(2013, 3, 20, 2, 0)
        orgFK = 1
        newEvent.name = name
        newEvent.description = desc
        newEvent.startdate = start
        newEvent.enddate = end
        newEvent.organizationFK = orgFK
        
        # Ensure it's not already in db.
        result = events._isDuplicateEvent(newEvent)
        self.assertFalse(result)
        
        # Try to delete it even though we know it's not there
        result = events._removeEvent(newEvent.pk, self.db)
        self.assertFalse(result)
        
        
    ''' Test method in events.py '''
    def test__removeEvent_false(self):
        # Try to delete a record that's not there
        result = events._removeEvent(9999999, self.db)
        self.assertFalse(result)
        
        
    ''' Test method in events.py '''
    def test_removeEvent_true(self):
        # Define the values we're going to have to add for the test.
        newEvent = models.Event()
        name = 'test_removeEvent_true event'
        desc = 'description of test_removeEvent_true event is indescribable'
        start = datetime.datetime(2013, 3, 20, 1, 0)
        end = datetime.datetime(2013, 3, 20, 2, 0)
        orgFK = 2
        newEvent.name = name
        newEvent.description = desc
        newEvent.startdate = start
        newEvent.enddate = end
        newEvent.organizationFK = orgFK

        # Ensure it's not already in db.
        result = events._isDuplicateEvent(newEvent)
        self.assertFalse(result)

        # Add it to db
        newEventPK = events._insertEvent(newEvent, self.db)
        self.assertTrue(newEventPK > 0)

        # Ensure it's in db.
        result = events._isDuplicateEvent(newEvent)
        self.assertTrue(result)

        # Now that we added it, lets delete it.
        result = events.removeEvent(newEventPK, self.db)
        self.assertIsNotNone(result)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'true')
            if key == models.EVENT_PK_KEY:
                self.assertEqual(value, newEventPK)

        # Ensure it's not in db.
        result = events._isDuplicateEvent(newEvent)
        self.assertFalse(result)


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(EventTestCase('test__getEventByID'))
    suite.addTest(EventTestCase('test__getEventsByOrg_true'))
    suite.addTest(EventTestCase('test__getEventsByOrg_false'))
    suite.addTest(EventTestCase('test_getEventsByOrg_true'))
    suite.addTest(EventTestCase('test_getEventsByOrg_false'))
    suite.addTest(EventTestCase('test_extractEventFromDict'))
    #suite.addTest(EventTestCase('test_extractEventFromDict_incomplete'))
    suite.addTest(EventTestCase('test__isDuplicateEvent_true'))
    suite.addTest(EventTestCase('test__isDuplicateEvent_false'))
    suite.addTest(EventTestCase('test__insertEvent_true'))
    suite.addTest(EventTestCase('test__insertEvent_duplicate'))
    suite.addTest(EventTestCase('test__insertEvent_badorg'))
    suite.addTest(EventTestCase('test_insertEvent_true'))
    suite.addTest(EventTestCase('test_insertEvent_duplicate'))
    suite.addTest(EventTestCase('test_insertEvent_badorg'))
    suite.addTest(EventTestCase('test__removeEvent_true'))
    suite.addTest(EventTestCase('test__removeEvent_invalid'))
    suite.addTest(EventTestCase('test__removeEvent_false'))
    suite.addTest(EventTestCase('test_removeEvent_true'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
