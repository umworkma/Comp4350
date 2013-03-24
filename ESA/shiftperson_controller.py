#####################################
# shiftperson_controller.py
# Controller code relating to assigning people to shifts
#####################################

from flask import *
import models
import controllers
import events
import shifts_controller
from datetime import datetime

def extractShiftPersonFromDict(shiftPersonDict):
    target = models.Shift()

    for key, value in shiftPersonDict.iteritems():
        if(key == models.SHIFTPERSON_PK_KEY and value != 'None'):
            target.pk = int(value)
        if(key == models.SHIFTPERSON_SHIFT_KEY and value != 'None'):
            target.shiftFK = int(value)
        if(key == models.SHIFTPERSON_PERSON_KEY and value != 'None'):
            target.personFK = int(value)
    return target

def shiftPersonToJSON(shiftPerson):
    jsonString = '{' + '"{key}":{val},'.format(key=models.SHIFTPERSON_PK_KEY, val=shiftPerson.pk if shiftPerson.pk != None else '"None"')
    jsonString += '"{key}":{val},'.format(key=models.SHIFTPERSON_SHIFT_KEY, val=shiftPerson.shiftFK if shiftPerson.shiftFK != None else '"None"')
    jsonString += '"{key}":{val}'.format(key=models.SHIFTPERSON_PERSON_KEY, val=shiftPerson.personFK if shiftPerson.personFK != None else '"None"')
    jsonString += '}'
    return jsonString

def _getPeopleByShift(shiftFK):
    results = models.ShiftPerson.query.filter_by(shiftFK=shiftFK)
    return results
    
def getPeopleByShiftJSON(shiftFK):
    list = _getPeopleByShift(shiftFK)
    resultJSON = '{"Workers":'
    counter = 0
    if list.count() > 0:
        resultJSON += '['
        for shiftPerson in list:
            person = models.Person.query.filter_by(entityFK=shiftPerson.personFK).first()
            personJSON = controllers.employeeToJSON(person)
            if counter > 0:
                resultJSON += ','
            resultJSON += personJSON
            counter += 1
        resultJSON += ']'
    else:
        resultJSON += '"None"'
    resultJSON += '}'
    return resultJSON
    
def _getShiftsByPerson(personFK):
    results = models.ShiftPerson.query.filter_by(personFK=personFK)
    return results
    
def getShiftsByPersonJSON(personFK):
    list = _getShiftsByPerson(personFK)
    resultJSON = '{"Shifts":'
    counter = 0
    if list.count() > 0:
        resultJSON += '['
        for shiftPerson in list:
            shift = shifts_controller._getShiftByID(shiftPerson.shiftFK)
            shiftJSON = shifts_controller.shiftToJSON(shift)
            if counter > 0:
                resultJSON += ','
            resultJSON += shiftJSON
            counter += 1
        resultJSON += ']'
    else:
        resultJSON += '"None"'
    resultJSON += '}'
    return resultJSON
    

# Returns True or False
def _isDuplicateAssignment(shiftPerson):
    result = True
    target = models.ShiftPerson.query.filter_by(shiftFK=shiftPerson.shiftFK, personFK=shiftPerson.personFK).first()
    if(target == None):
        result = False
    return result

# Return values: BadShift = couldn't find shift matching shiftperson.shiftFK
#                BadPerson = couldn't find person matching shiftperson.personFK
#                Duplicate = found an existing shiftperson with same shift/person
#                shift.pk = new pk of shift-person assignment successfully added
def _insertShiftPerson(shiftPerson, db):
    result = 'Unknown'
    isDup = _isDuplicateAssignment(shiftPerson)
    shift = shifts_controller._getShiftByID(shiftPerson.shiftFK)
    if shift is None:
        result = 'BadShift'
    person = models.Person.query.filter_by(entityFK=shiftPerson.personFK).first()
    if person is None:
        result = 'BadPerson'
    if(isDup == False and result == 'Unknown'):
        db.session.add(shiftPerson)
        db.session.commit()
        if(shiftPerson.pk > 0):
            result = shiftPerson.pk
    if(result == 'Unknown'):
        result = 'Duplicate'
    return result


# returns: {"success":"true", "shiftperson_pk":<pk>}
#      or: {"success":"false", "msg":["BadShift" | "BadPerson" | "Duplicate"], "event_pk":"None"}
def insertShiftPerson(shiftFK, personFK, db):
    shiftPerson = models.ShiftPerson(shiftFK, personFK)
    result = _insertShiftPerson(shiftPerson, db)
    if result != 'BadShift' and result != 'BadPerson' and result != 'Duplicate':
        resultJSON = '{"success":"true",'
    else:
        resultJSON = '{' + '"success":"false","msg":"{val}",'.format(val=result)
    
    if shiftPerson.pk is not None:
        resultJSON += '"{key}":{val}'.format(key=models.SHIFTPERSON_PK_KEY, val=shiftPerson.pk)
    else:
        resultJSON += '"{key}":"None"'.format(key=models.SHIFTPERSON_PK_KEY)
    resultJSON += '}'
    return resultJSON


# Returns True on success or False on failure (couldn't find the ShiftPerson).
def _removeShiftPerson(shiftFK, personFK, db):
    shiftPerson = models.ShiftPerson.query.filter_by(shiftFK=shiftFK,personFK=personFK).first()
    result = False
    if shiftPerson is not None:
        db.session.delete(shiftPerson)
        db.session.commit()
        result = True
    return result
    

# Returns JSON: {"success":["true" | "false"],"shiftperson_pk":<pk>}
def removeShiftPerson(shiftFK, personFK, db):
    result = _removeShiftPerson(shiftFK, personFK, db)
    resultJSON = '{'+ '"success":"{val}"'.format(val="true" if result == True else "false")
    # resultJSON += '"{key}":{val}'.format(result=result, key=models.SHIFTPERSON_PK_KEY, val=pk)
    resultJSON += '}'
    return resultJSON

