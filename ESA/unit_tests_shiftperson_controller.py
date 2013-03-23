#!../venv/bin/python
import unittest
import json

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models
import controllers
import shiftperson_controller
import shifts_controller
import datetime


class ShiftPersonControllerTestCase(TestCase):

    database_uri = "sqlite:///test_shiftperson_controller.db"
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
        
        
    def test_shiftPersonToJSON(self):
        control = models.ShiftPerson.query.first()
        controlJSON = shiftperson_controller.shiftPersonToJSON(control)
        expectedJSON = stringJSON = '{"shiftperson_pk":1,"shiftperson_shiftfk":1,"shiftperson_personfk":3}'
        self.assertEqual(controlJSON, expectedJSON)
        
    
    def test_extractShiftPersonFromDict(self):
        control = models.ShiftPerson.query.first()
        stringJSON = shiftperson_controller.shiftPersonToJSON(control)
        data = json.loads(stringJSON)
        target = shiftperson_controller.extractShiftPersonFromDict(data)

        self.assertEqual(control.pk, target.pk)
        self.assertEqual(control.shiftFK, target.shiftFK)
        self.assertEqual(control.personFK, target.personFK)
        
        
    def test__getPeopleByShift_true(self):
        key = 1
        shiftPersonList = shiftperson_controller._getPeopleByShift(key)
        self.assertIsNotNone(shiftPersonList)
        self.assertEqual(shiftPersonList.count(), 2)
        counter = 0
        for shiftPerson in shiftPersonList:
            counter += 1
            self.assertTrue(shiftPerson.pk > 0 and shiftPerson.pk <= 2)
            control = models.ShiftPerson.query.filter_by(pk=shiftPerson.pk).first()
            self.assertEqual(shiftPerson.__repr__(), control.__repr__())
        self.assertEqual(counter, 2)
        
    def test__getPeopleByShift_false(self):
        key = 9999
        shiftPersonList = shiftperson_controller._getPeopleByShift(key)
        self.assertEqual(shiftPersonList.count(), 0)
        
        
    def test_getPeopleByShiftJSON_true(self):
        key = 1
        shiftPersonListJSON = shiftperson_controller.getPeopleByShiftJSON(key)
        shiftPersonListDict = json.loads(shiftPersonListJSON)
        for rootKey, rootVal in shiftPersonListDict.iteritems():
            self.assertEqual(rootKey, 'Workers')
            counter = 0
            for personJSON in rootVal:
                person = controllers.extractEmployeeFromDict(personJSON)
                if person.entityFK == 3:
                    counter += 1
                    self.assertEqual(person.firstname, 'Chris')
                    self.assertEqual(person.lastname, 'Workman')
                elif person.entityFK == 4:
                    counter += 1
                    self.assertEqual(person.firstname, 'Ryoji')
                    self.assertEqual(person.lastname, 'Betchaku')
            self.assertEqual(counter, 2)
            
    def test_getPeopleByShiftJSON_false(self):
        key = 999
        shiftPersonListJSON = shiftperson_controller.getPeopleByShiftJSON(key)
        shiftPersonListDict = json.loads(shiftPersonListJSON)
        for rootKey, rootVal in shiftPersonListDict.iteritems():
            self.assertEqual(rootKey, 'Workers')
            self.assertEqual(rootVal, 'None')
            
            
    def test__getShiftsByPerson_true(self):
        key = 3
        shiftPersonList = shiftperson_controller._getShiftsByPerson(key)
        self.assertIsNotNone(shiftPersonList)
        self.assertEqual(shiftPersonList.count(), 3)
        counter = 0
        for shiftPerson in shiftPersonList:
            counter += 1
            self.assertTrue(shiftPerson.pk == 1 or shiftPerson.pk == 5 or shiftPerson.pk == 7)
            control = models.ShiftPerson.query.filter_by(pk=shiftPerson.pk).first()
            self.assertEqual(shiftPerson.__repr__(), control.__repr__())
        self.assertEqual(counter, 3)
        
    def test__getShiftsByPerson_false(self):
        key = 9999
        shiftPersonList = shiftperson_controller._getShiftsByPerson(key)
        self.assertEqual(shiftPersonList.count(), 0)
            
            
    def test_getShiftsByPersonJSON_true(self):
        key = 3
        shiftPersonListJSON = shiftperson_controller.getShiftsByPersonJSON(key)
        shiftPersonListDict = json.loads(shiftPersonListJSON)
        for rootKey, rootVal in shiftPersonListDict.iteritems():
            self.assertEqual(rootKey, 'Shifts')
            counter = 0
            for shiftJSON in rootVal:
                shift = shifts_controller.extractShiftFromDict(shiftJSON)
                if shift.pk == 1:
                    counter += 1
                    self.assertEqual(shift.startdatetime, datetime.datetime(2013, 7, 12, 12, 0))
                    self.assertEqual(shift.enddatetime, datetime.datetime(2013, 7, 12, 13, 0))
                    self.assertEqual(shift.location, 'Booth A')
                    self.assertEqual(shift.minWorkers, 2)
                    self.assertEqual(shift.maxWorkers, 4)
                elif shift.pk == 3:
                    counter += 1
                    self.assertEqual(shift.startdatetime, datetime.datetime(2013, 7, 12, 14, 0))
                    self.assertEqual(shift.enddatetime, datetime.datetime(2013, 7, 12, 15, 0))
                    self.assertEqual(shift.location, 'Booth A')
                    self.assertEqual(shift.minWorkers, 3)
                    self.assertEqual(shift.maxWorkers, 4)
                elif shift.pk == 4:
                    counter += 1
                    self.assertEqual(shift.startdatetime, datetime.datetime(2013, 7, 12, 15, 0))
                    self.assertEqual(shift.enddatetime, datetime.datetime(2013, 7, 12, 16, 0))
                    self.assertEqual(shift.location, 'Booth A')
                    self.assertEqual(shift.minWorkers, 3)
                    self.assertEqual(shift.maxWorkers, 4)
            self.assertEqual(counter, 3)
            
    def test_getShiftsByPersonJSON_false(self):
        key = 999
        shiftPersonListJSON = shiftperson_controller.getShiftsByPersonJSON(key)
        shiftPersonListDict = json.loads(shiftPersonListJSON)
        for rootKey, rootVal in shiftPersonListDict.iteritems():
            self.assertEqual(rootKey, 'Shifts')
            self.assertEqual(rootVal, 'None')
        
    
    def test__isDuplicateAssignment_true(self):
        shiftPerson1 = models.ShiftPerson.query.first()
        shiftPerson2 = models.ShiftPerson(shiftPerson1.shiftFK, shiftPerson1.personFK)
        shiftPerson2.pk = shiftPerson1.pk
        result = shiftperson_controller._isDuplicateAssignment(shiftPerson2)
        self.assertTrue(result)
        
    def test__isDuplicateAssignment_false(self):
        shiftPerson1 = models.ShiftPerson.query.first()
        shiftPerson2 = models.ShiftPerson(shiftPerson1.shiftFK, shiftPerson1.personFK)
        shiftPerson2.pk = shiftPerson1.pk
        shiftPerson2.shiftFK = 2
        result = shiftperson_controller._isDuplicateAssignment(shiftPerson2)
        self.assertFalse(result)
        
        
    def test__insertShiftPerson_true(self):
        shiftFK = 1
        personFK = 5
        shiftPerson = models.ShiftPerson(shiftFK, personFK)
        result = shiftperson_controller._insertShiftPerson(shiftPerson, self.db)
        self.assertTrue(result > 0)
        
        newShiftPerson = models.ShiftPerson.query.filter_by(pk=result).first()
        self.assertEqual(newShiftPerson.pk, result)
        self.assertEqual(newShiftPerson.shiftFK, shiftFK)
        self.assertEqual(newShiftPerson.personFK, personFK)
        
    def test__insertShiftPerson_duplicate(self):
        shiftFK = 1
        personFK = 4
        shiftPerson = models.ShiftPerson(shiftFK, personFK)
        result = shiftperson_controller._insertShiftPerson(shiftPerson, self.db)
        self.assertEqual(result, 'Duplicate')
        
    def test__insertShiftPerson_badshift(self):
        shiftFK = 999
        personFK = 4
        shiftPerson = models.ShiftPerson(shiftFK, personFK)
        result = shiftperson_controller._insertShiftPerson(shiftPerson, self.db)
        self.assertEqual(result, 'BadShift')
        
    def test__insertShiftPerson_badperson(self):
        shiftFK = 1
        personFK = 999
        shiftPerson = models.ShiftPerson(shiftFK, personFK)
        result = shiftperson_controller._insertShiftPerson(shiftPerson, self.db)
        self.assertEqual(result, 'BadPerson')
        
        
    def test_insertShiftPerson_true(self):
        shiftFK = 2
        personFK = 3
        
        shiftPersonJSON = '{'
        shiftPersonJSON += '"{key}":"{val}"'.format(key=models.SHIFTPERSON_PERSON_KEY, val=personFK)
        shiftPersonJSON += '}'
        shiftPersonDict = json.loads(shiftPersonJSON)
        
        result = shiftperson_controller.insertShiftPerson(shiftFK, personFK, self.db)
        self.assertIsNotNone(result)
        newKey = 0
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'true')
            if key == models.SHIFTPERSON_PK_KEY:
                self.assertTrue(value > 0)
                newKey = value
        
        newShiftPerson = models.ShiftPerson.query.filter_by(pk=newKey).first()
        self.assertEqual(newShiftPerson.pk, newKey)
        self.assertEqual(newShiftPerson.shiftFK, shiftFK)
        self.assertEqual(newShiftPerson.personFK, personFK)
        
    def test_insertShiftPerson_duplicate(self):
        shiftPerson1 = models.ShiftPerson.query.first()
        shiftPerson2 = models.ShiftPerson(shiftPerson1.personFK)
        shiftPersonJSON = shiftperson_controller.shiftPersonToJSON(shiftPerson2)
        shiftPersonDict = json.loads(shiftPersonJSON)
        
        result = shiftperson_controller.insertShiftPerson(shiftPerson1.shiftFK, shiftPerson1.personFK, self.db)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'false')
            if key == 'msg':
                self.assertEqual(value, 'Duplicate')
            elif key == models.SHIFTPERSON_PK_KEY:
                self.assertEqual(value, 'None')
        
    def test_insertShiftPerson_badshift(self):
        shiftFK = 999
        personFK = 5
        shiftPerson1 = models.ShiftPerson()
        shiftPerson1.personFK = 5
        shiftPersonJSON = shiftperson_controller.shiftPersonToJSON(shiftPerson1)
        shiftPersonDict = json.loads(shiftPersonJSON)

        result = shiftperson_controller.insertShiftPerson(shiftFK, personFK, self.db)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'false')
            if key == 'msg':
                self.assertEqual(value, 'BadShift')
            elif key == models.SHIFTPERSON_PK_KEY:
                self.assertEqual(value, 'None')    
        
    def test_insertShiftPerson_badperson(self):
        shiftFK = 1
        personFK = 999
        shiftPerson1 = models.ShiftPerson()
        shiftPerson1.personFK = 999
        shiftPersonJSON = shiftperson_controller.shiftPersonToJSON(shiftPerson1)
        shiftPersonDict = json.loads(shiftPersonJSON)

        result = shiftperson_controller.insertShiftPerson(shiftFK, personFK, self.db)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'false')
            if key == 'msg':
                self.assertEqual(value, 'BadPerson')
            elif key == models.SHIFTPERSON_PK_KEY:
                self.assertEqual(value, 'None')

                
    def test__removeShiftPerson_true(self):
        # Define the values we're going to have to add for the test.
        shiftFK = 3
        personFK = 4
        newShiftPerson = models.ShiftPerson(shiftFK, personFK)
        
        # Ensure it's not already in db.
        result = shiftperson_controller._isDuplicateAssignment(newShiftPerson)
        self.assertFalse(result)
        
        # Add it to db
        newShiftPersonPK = shiftperson_controller._insertShiftPerson(newShiftPerson, self.db)
        self.assertTrue(newShiftPersonPK > 0)
        
        # Ensure it's in db.
        result = shiftperson_controller._isDuplicateAssignment(newShiftPerson)
        self.assertTrue(result)
        
        # Now that we added it, lets delete it.
        result = shiftperson_controller._removeShiftPerson(newShiftPersonPK, self.db)
        self.assertTrue(result)
        
        # Ensure it's not in db.
        result = shiftperson_controller._isDuplicateAssignment(newShiftPerson)
        self.assertFalse(result)
        
    def test__removeShiftPerson_invalid(self):
        # Define the values we're going to have to add for the test.
        shiftFK = 3
        personFK = 4
        newShiftPerson = models.ShiftPerson(shiftFK, personFK)
        
        # Ensure it's not already in db.
        result = shiftperson_controller._isDuplicateAssignment(newShiftPerson)
        self.assertFalse(result)
        
        # Try to delete it even though we know it's not there
        result = shiftperson_controller._removeShiftPerson(newShiftPerson.pk, self.db)
        self.assertFalse(result)
        
    def test__removeShiftPerson_false(self):
        # Try to delete a record that's not there
        result = shiftperson_controller._removeShiftPerson(9999999, self.db)
        self.assertFalse(result)
        
        
    def test_removeShiftPerson_true(self):
        # Define the values we're going to have to add for the test.
        shiftFK = 3
        personFK = 4
        newShiftPerson = models.ShiftPerson(shiftFK, personFK)
        
        # Ensure it's not already in db.
        result = shiftperson_controller._isDuplicateAssignment(newShiftPerson)
        self.assertFalse(result)
        
        # Add it to db
        newShiftPersonPK = shiftperson_controller._insertShiftPerson(newShiftPerson, self.db)
        self.assertTrue(newShiftPersonPK > 0)
        
        # Ensure it's in db.
        result = shiftperson_controller._isDuplicateAssignment(newShiftPerson)
        self.assertTrue(result)
        
        # Now that we added it, lets delete it.
        result = shiftperson_controller.removeShiftPerson(newShiftPersonPK, self.db)
        self.assertIsNotNone(result)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'success':
                self.assertEqual(value, 'true')
            if key == models.SHIFTPERSON_PK_KEY:
                self.assertEqual(value, newShiftPersonPK)
        
        # Ensure it's not in db.
        result = shiftperson_controller._isDuplicateAssignment(newShiftPerson)
        self.assertFalse(result)
        
        
        
        
        



def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(ShiftPersonControllerTestCase('test_shiftPersonToJSON'))
    suite.addTest(ShiftPersonControllerTestCase('test_extractShiftPersonFromDict'))
    
    suite.addTest(ShiftPersonControllerTestCase('test__getPeopleByShift_true'))
    suite.addTest(ShiftPersonControllerTestCase('test__getPeopleByShift_false'))
    suite.addTest(ShiftPersonControllerTestCase('test_getPeopleByShiftJSON_true'))
    suite.addTest(ShiftPersonControllerTestCase('test_getPeopleByShiftJSON_false'))
    
    suite.addTest(ShiftPersonControllerTestCase('test__getShiftsByPerson_true'))
    suite.addTest(ShiftPersonControllerTestCase('test__getShiftsByPerson_false'))
    suite.addTest(ShiftPersonControllerTestCase('test_getShiftsByPersonJSON_true'))
    suite.addTest(ShiftPersonControllerTestCase('test_getShiftsByPersonJSON_false'))
    
    suite.addTest(ShiftPersonControllerTestCase('test__isDuplicateAssignment_true'))
    suite.addTest(ShiftPersonControllerTestCase('test__isDuplicateAssignment_false'))
    
    suite.addTest(ShiftPersonControllerTestCase('test__insertShiftPerson_true'))
    suite.addTest(ShiftPersonControllerTestCase('test__insertShiftPerson_duplicate'))
    suite.addTest(ShiftPersonControllerTestCase('test__insertShiftPerson_badshift'))
    suite.addTest(ShiftPersonControllerTestCase('test__insertShiftPerson_badperson'))
    suite.addTest(ShiftPersonControllerTestCase('test_insertShiftPerson_true'))
    suite.addTest(ShiftPersonControllerTestCase('test_insertShiftPerson_duplicate'))
    suite.addTest(ShiftPersonControllerTestCase('test_insertShiftPerson_badshift'))
    suite.addTest(ShiftPersonControllerTestCase('test_insertShiftPerson_badperson'))
    
    suite.addTest(ShiftPersonControllerTestCase('test__removeShiftPerson_true'))
    suite.addTest(ShiftPersonControllerTestCase('test__removeShiftPerson_invalid'))
    suite.addTest(ShiftPersonControllerTestCase('test__removeShiftPerson_false'))
    suite.addTest(ShiftPersonControllerTestCase('test_removeShiftPerson_true'))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
