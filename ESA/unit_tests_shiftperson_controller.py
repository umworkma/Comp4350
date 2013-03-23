#!../venv/bin/python
import unittest
import json

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models
import shiftperson_controller


class ShiftControllerTestCase(TestCase):

    database_uri = "sqlite:///test_shifts_controller.db"
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
        
        
    def test_shiftToJSON(self):
        control = models.Shift.query.first()
        controlJSON = shifts_controller.shiftToJSON(control)
        expectedJSON = stringJSON = '{"shift_pk":1,"shift_eventfk":1,"shift_start":"2013-07-12 12:00:00","shift_end":"2013-07-12 13:00:00","shift_location":"Booth A","shift_minworkers":2,"shift_maxworkers":4}'
        self.assertEqual(controlJSON, expectedJSON)
        
    
    def test_extractShiftFromDict(self):
        control = models.Shift.query.first()
        stringJSON = shifts_controller.shiftToJSON(control)
        data = json.loads(stringJSON)
        target = shifts_controller.extractShiftFromDict(data)

        self.assertEqual(control.pk, target.pk)
        self.assertEqual(control.eventFK, target.eventFK)
        self.assertEqual(control.startdatetime, target.startdatetime)
        self.assertEqual(control.enddatetime, target.enddatetime)
        self.assertEqual(control.location, target.location)
        self.assertEqual(control.minWorkers, target.minWorkers)
        self.assertEqual(control.maxWorkers, target.maxWorkers)
        
        
    def test__getShiftByEvent_true(self):
        key = 1
        shiftList = shifts_controller._getShiftsByEvent(key)
        self.assertIsNotNone(shiftList)
        self.assertEqual(shiftList.count(), 4)
        counter = 0
        for shift in shiftList:
            counter += 1
            self.assertTrue(shift.pk > 0 and shift.pk <= 4)
            control = models.Shift.query.filter_by(pk=shift.pk).first()
            self.assertEqual(shift.__repr__(), control.__repr__())
        self.assertEqual(counter, 4)
        
    def test__getShiftByEvent_false(self):
        key = 9999
        shiftList = shifts_controller._getShiftsByEvent(key)
        self.assertEqual(shiftList.count(), 0)
        
        
    def test_getShiftByEventJSON_true(self):
        key = 1
        shiftListJSON = shifts_controller.getShiftsByEventJSON(key)
        shiftListDict = json.loads(shiftListJSON)
        for rootKey, rootVal in shiftListDict.iteritems():
            self.assertEqual(rootKey, 'Shifts')
            counter = 0
            for shiftJSON in rootVal:
                shift = shifts_controller.extractShiftFromDict(shiftJSON)
                self.assertEqual(shift.eventFK, key)
                self.assertEqual(shift.location, 'Booth A')
                if shift.pk == 1:
                    counter += 1
                    self.assertEqual(shift.startdatetime, datetime.datetime(2013, 7, 12, 12, 0))
                    self.assertEqual(shift.enddatetime, datetime.datetime(2013, 7, 12, 13, 0))
                    self.assertEqual(shift.minWorkers, 2)
                    self.assertEqual(shift.maxWorkers, 4)
                elif shift.pk == 2:
                    counter += 1
                    self.assertEqual(shift.startdatetime, datetime.datetime(2013, 7, 12, 13, 0))
                    self.assertEqual(shift.enddatetime, datetime.datetime(2013, 7, 12, 14, 0))
                    self.assertEqual(shift.minWorkers, 2)
                    self.assertEqual(shift.maxWorkers, 4)
                elif shift.pk == 3:
                    counter += 1
                    self.assertEqual(shift.startdatetime, datetime.datetime(2013, 7, 12, 14, 0))
                    self.assertEqual(shift.enddatetime, datetime.datetime(2013, 7, 12, 15, 0))
                    self.assertEqual(shift.minWorkers, 3)
                    self.assertEqual(shift.maxWorkers, 4)
                elif shift.pk == 4:
                    counter += 1
                    self.assertEqual(shift.startdatetime, datetime.datetime(2013, 7, 12, 15, 0))
                    self.assertEqual(shift.enddatetime, datetime.datetime(2013, 7, 12, 16, 0))
                    self.assertEqual(shift.minWorkers, 3)
                    self.assertEqual(shift.maxWorkers, 4)
            self.assertEqual(counter, 4)
            
    def test_getShiftByEventJSON_false(self):
        key = 999
        shiftListJSON = shifts_controller.getShiftsByEventJSON(key)
        shiftListDict = json.loads(shiftListJSON)
        for rootKey, rootVal in shiftListDict.iteritems():
            self.assertEqual(rootKey, 'Shifts')
            self.assertEqual(rootVal, 'None')
        
    
    def test__isDuplicateShift_true(self):
        shift1 = models.Shift.query.first()
        
        shift2 = models.Shift()
        shift2.eventFK = shift1.eventFK
        shift2.startdatetime = shift1.startdatetime
        shift2.enddatetime = shift1.enddatetime
        shift2.location = shift1.location
        
        result = shifts_controller._isDuplicateShift(shift2)
        self.assertTrue(result)
        
    def test__isDuplicateShift_false(self):
        shift1 = models.Shift.query.first()

        shift2 = models.Shift()
        shift2.eventFK = shift1.eventFK
        shift2.startdatetime = shift1.startdatetime
        shift2.enddatetime = shift1.enddatetime
        shift2.location = shift1.location + 'difference'

        result = shifts_controller._isDuplicateShift(shift2)
        self.assertFalse(result)
        
        
    def test__insertShift_true(self):
        shift = models.Shift()
        eventFK = 1
        start = datetime.datetime(2013, 7, 24, 13, 0)
        end = datetime.datetime(2013, 7, 24, 14, 0)
        location = 'Booth B'
        minWorkers = 24
        maxWorkers = 42
        
        shift.eventFK = eventFK
        shift.startdatetime = start
        shift.enddatetime = end
        shift.location = location
        shift.minWorkers = minWorkers
        shift.maxWorkers = maxWorkers
        
        result = shifts_controller._insertShift(shift, self.db)
        self.assertTrue(result > 0)
        
        newShift = models.Shift.query.filter_by(pk=result).first()
        self.assertEqual(newShift.pk, result)
        self.assertEqual(newShift.eventFK, eventFK)
        self.assertEqual(newShift.startdatetime, start)
        self.assertEqual(newShift.enddatetime, end)
        self.assertEqual(newShift.location, location)
        self.assertEqual(newShift.minWorkers, minWorkers)
        self.assertEqual(newShift.maxWorkers, maxWorkers)
        
    def test__insertShift_duplicate(self):
        shift = models.Shift()
        eventFK = 1
        start = datetime.datetime(2013, 7, 12, 15, 0)
        end = datetime.datetime(2013, 7, 12, 16, 0)
        location = 'Booth A'
        minWorkers = 3
        maxWorkers = 4

        shift.eventFK = eventFK
        shift.startdatetime = start
        shift.enddatetime = end
        shift.location = location
        shift.minWorkers = minWorkers
        shift.maxWorkers = maxWorkers

        result = shifts_controller._insertShift(shift, self.db)
        self.assertEqual(result, 'Duplicate')
        
    def test__insertShift_badevent(self):
        shift = models.Shift()
        eventFK = 0
        start = datetime.datetime(2013, 7, 12, 15, 0)
        end = datetime.datetime(2013, 7, 12, 16, 0)
        location = 'Booth A'
        minWorkers = 3
        maxWorkers = 4

        shift.eventFK = eventFK
        shift.startdatetime = start
        shift.enddatetime = end
        shift.location = location
        shift.minWorkers = minWorkers
        shift.maxWorkers = maxWorkers

        result = shifts_controller._insertShift(shift, self.db)
        self.assertEqual(result, 'BadEvent')
        
        
    def test_insertShift_true(self):
        eventFK = 1
        start = datetime.datetime(2013, 7, 24, 13, 0)
        end = datetime.datetime(2013, 7, 24, 14, 0)
        location = 'Booth C'
        minWorkers = 24
        maxWorkers = 42
        
        shiftJSON = '{'
        shiftJSON += '"{key}":"{val}",'.format(key=models.SHIFT_START_KEY, val=start)
        shiftJSON += '"{key}":"{val}",'.format(key=models.SHIFT_END_KEY, val=end)
        shiftJSON += '"{key}":"{val}",'.format(key=models.SHIFT_LOCATION_KEY, val=location)
        shiftJSON += '"{key}":{val},'.format(key=models.SHIFT_MINWORKERS_KEY, val=minWorkers)
        shiftJSON += '"{key}":{val}'.format(key=models.SHIFT_MAXWORKERS_KEY, val=maxWorkers)
        shiftJSON += '}'
        shiftDict = json.loads(shiftJSON)
        
        result = shifts_controller.insertShift(eventFK, shiftDict, self.db)
        self.assertIsNotNone(result)
        newKey = 0
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'true')
            if key == models.SHIFT_PK_KEY:
                self.assertTrue(value > 0)
                newKey = value
        
        newShift = models.Shift.query.filter_by(pk=newKey).first()
        self.assertEqual(newShift.pk, newKey)
        self.assertEqual(newShift.eventFK, eventFK)
        self.assertEqual(newShift.startdatetime, start)
        self.assertEqual(newShift.enddatetime, end)
        self.assertEqual(newShift.location, location)
        self.assertEqual(newShift.minWorkers, minWorkers)
        self.assertEqual(newShift.maxWorkers, maxWorkers)
        
    def test_insertShift_duplicate(self):
        shift1 = models.Shift.query.first()
        
        shift2 = models.Shift()
        shift2.startdatetime = shift1.startdatetime
        shift2.enddatetime = shift1.enddatetime
        shift2.location=shift1.location
        shiftJSON = shifts_controller.shiftToJSON(shift2)
        shiftDict = json.loads(shiftJSON)
        
        result = shifts_controller.insertShift(shift1.eventFK, shiftDict, self.db)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'false')
            if key == 'msg':
                self.assertEqual(value, 'Duplicate')
            elif key == 'shift_pk':
                self.assertEqual(value, 'None')
        
    def test_insertShift_badevent(self):
        eventFK = 99999
        start = datetime.datetime(2013, 7, 24, 13, 0)
        end = datetime.datetime(2013, 7, 24, 14, 0)
        location = 'Booth B'
        minWorkers = 24
        maxWorkers = 42
        
        shiftJSON = '{'
        shiftJSON += '"{key}":"{val}",'.format(key=models.SHIFT_START_KEY, val=start)
        shiftJSON += '"{key}":"{val}",'.format(key=models.SHIFT_END_KEY, val=end)
        shiftJSON += '"{key}":"{val}",'.format(key=models.SHIFT_LOCATION_KEY, val=location)
        shiftJSON += '"{key}":{val},'.format(key=models.SHIFT_MINWORKERS_KEY, val=minWorkers)
        shiftJSON += '"{key}":{val}'.format(key=models.SHIFT_MAXWORKERS_KEY, val=maxWorkers)
        shiftJSON += '}'
        shiftDict = json.loads(shiftJSON)
        
        result = shifts_controller.insertShift(eventFK, shiftDict, self.db)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'false')
            if key == 'msg':
                self.assertEqual(value, 'BadEvent')
            elif key == 'shift_pk':
                self.assertEqual(value, 'None')        

                
    def test__removeShift_true(self):
        # Define the values we're going to have to add for the test.
        newShift = models.Shift()
        newShift.eventFK = 1
        newShift.startdatetime = datetime.datetime(2013,7,28,16,0)
        newShift.enddatetime = datetime.datetime(2013,7,28,17,0)
        newShift.location = 'Booth C.5'
        newShift.minWorkers = 24
        newShift.maxWorkers = 42
        
        # Ensure it's not already in db.
        result = shifts_controller._isDuplicateShift(newShift)
        self.assertFalse(result)
        
        # Add it to db
        newShiftPK = shifts_controller._insertShift(newShift, self.db)
        self.assertTrue(newShiftPK > 0)
        
        # Ensure it's in db.
        result = shifts_controller._isDuplicateShift(newShift)
        self.assertTrue(result)
        
        # Now that we added it, lets delete it.
        result = shifts_controller._removeShift(newShiftPK, self.db)
        self.assertTrue(result)
        
        # Ensure it's not in db.
        result = shifts_controller._isDuplicateShift(newShift)
        self.assertFalse(result)
        
    def test__removeShift_invalid(self):
        # Define the values we're going to have to add for the test.
        newShift = models.Shift()
        newShift.eventFK = 1
        newShift.startdatetime = datetime.datetime(2013,7,28,16,0)
        newShift.enddatetime = datetime.datetime(2013,7,28,17,0)
        newShift.location = 'Booth C.5'
        newShift.minWorkers = 24
        newShift.maxWorkers = 42
        
        # Ensure it's not already in db.
        result = shifts_controller._isDuplicateShift(newShift)
        self.assertFalse(result)
        
        # Try to delete it even though we know it's not there
        result = shifts_controller._removeShift(newShift.pk, self.db)
        self.assertFalse(result)
        
    def test__removeShift_false(self):
        # Try to delete a record that's not there
        result = shifts_controller._removeShift(9999999, self.db)
        self.assertFalse(result)
        
        
    def test_removeShift_true(self):
        # Define the values we're going to have to add for the test.
        newShift = models.Shift()
        newShift.eventFK = 1
        newShift.startdatetime = datetime.datetime(2013,7,28,16,0)
        newShift.enddatetime = datetime.datetime(2013,7,28,17,0)
        newShift.location = 'Booth C.5'
        newShift.minWorkers = 24
        newShift.maxWorkers = 42
        
        # Ensure it's not already in db.
        result = shifts_controller._isDuplicateShift(newShift)
        self.assertFalse(result)
        
        # Add it to db
        newShiftPK = shifts_controller._insertShift(newShift, self.db)
        self.assertTrue(newShiftPK > 0)
        
        # Ensure it's in db.
        result = shifts_controller._isDuplicateShift(newShift)
        self.assertTrue(result)
        
        # Now that we added it, lets delete it.
        result = shifts_controller.removeShift(newShiftPK, self.db)
        self.assertIsNotNone(result)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'true')
            if key == models.SHIFT_PK_KEY:
                self.assertEqual(value, newShiftPK)
        
        # Ensure it's not in db.
        result = shifts_controller._isDuplicateShift(newShift)
        self.assertFalse(result)
        
        
        
        
        



def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(ShiftControllerTestCase('test_shiftToJSON'))
    suite.addTest(ShiftControllerTestCase('test_extractShiftFromDict'))
    suite.addTest(ShiftControllerTestCase('test__getShiftByEvent_true'))
    suite.addTest(ShiftControllerTestCase('test__getShiftByEvent_false'))
    suite.addTest(ShiftControllerTestCase('test_getShiftByEventJSON_true'))
    suite.addTest(ShiftControllerTestCase('test_getShiftByEventJSON_false'))
    suite.addTest(ShiftControllerTestCase('test__isDuplicateShift_true'))
    suite.addTest(ShiftControllerTestCase('test__isDuplicateShift_false'))
    suite.addTest(ShiftControllerTestCase('test__insertShift_true'))
    suite.addTest(ShiftControllerTestCase('test__insertShift_duplicate'))
    suite.addTest(ShiftControllerTestCase('test__insertShift_badevent'))
    suite.addTest(ShiftControllerTestCase('test_insertShift_true'))
    suite.addTest(ShiftControllerTestCase('test_insertShift_duplicate'))
    suite.addTest(ShiftControllerTestCase('test_insertShift_badevent'))
    suite.addTest(ShiftControllerTestCase('test__removeShift_true'))
    suite.addTest(ShiftControllerTestCase('test__removeShift_invalid'))
    suite.addTest(ShiftControllerTestCase('test__removeShift_false'))
    suite.addTest(ShiftControllerTestCase('test_removeShift_true'))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
