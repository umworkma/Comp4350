#####################################
# shifts_controller.py
# Controller code relating to events
#####################################

from flask import *
import models
import controllers
import events
from datetime import datetime

def extractShiftFromDict(shiftDict):
    target = models.Shift()

    for key, value in shiftDict.iteritems():
        if(key == models.SHIFT_PK_KEY and value != 'None'):
            target.pk = int(value)
        if(key == models.SHIFT_EVENTFK_KEY and value != 'None'):
            target.eventFK = int(value)
        if(key == models.SHIFT_START_KEY):
            target.startdatetime = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        if(key == models.SHIFT_END_KEY):
            target.enddatetime = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        if(key == models.SHIFT_LOCATION_KEY):
            target.location = value
        if(key == models.SHIFT_MINWORKERS_KEY):
            target.minWorkers = int(value)
        if(key == models.SHIFT_MAXWORKERS_KEY):
            target.maxWorkers = int(value)
    return target

def shiftToJSON(shift):
    jsonString = '{' + '"{key}":{val},'.format(key=models.SHIFT_PK_KEY, val=shift.pk if shift.pk != None else '"None"')
    jsonString += '"{key}":{val},'.format(key=models.SHIFT_EVENTFK_KEY, val=shift.eventFK if shift.eventFK != None else '"None"')
    jsonString += '"{key}":"{val}",'.format(key=models.SHIFT_START_KEY, val=shift.startdatetime)
    jsonString += '"{key}":"{val}",'.format(key=models.SHIFT_END_KEY, val=shift.enddatetime)
    jsonString += '"{key}":"{val}",'.format(key=models.SHIFT_LOCATION_KEY, val=shift.location)
    jsonString += '"{key}":{val},'.format(key=models.SHIFT_MINWORKERS_KEY, val=shift.minWorkers if shift.minWorkers is not None else 0)
    jsonString += '"{key}":{val}'.format(key=models.SHIFT_MAXWORKERS_KEY, val=shift.maxWorkers if shift.maxWorkers is not None else 0)
    jsonString += '}'
    return jsonString

def _getShiftByID(pk):
    results = models.Shift.query.filter_by(pk=pk).first()
    return results

def _getShiftsByEvent(eventFK):
    results = models.Shift.query.filter_by(eventFK=eventFK)
    return results
    
def getShiftsByEventJSON(eventFK):
    shiftList = _getShiftsByEvent(eventFK)
    resultJSON = '{"Shifts":'
    counter = 0
    if shiftList.count() > 0:
        resultJSON += '['
        for shift in shiftList:
            shiftJSON = shiftToJSON(shift)
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
def _isDuplicateShift(shift):
    result = True
    target = models.Shift.query.filter_by(eventFK=shift.eventFK, startdatetime=shift.startdatetime, enddatetime=shift.enddatetime, location=shift.location).first()
    if(target == None):
        result = False
    return result

# Return values: BadEvent = couldn't find event matching shift.eventFK
#                Duplicate = found an existing shift with same event/start/end/location
#                shift.pk = new pk of shift successfully added
def _insertShift(shift, db):
    result = 'Unknown'
    isDup = _isDuplicateShift(shift)
    event = events._getEventByID(shift.eventFK)
    if event is None:
        result = 'BadEvent'
    if(isDup == False and result == 'Unknown'):
        db.session.add(shift)
        db.session.commit()
        if(shift.pk > 0):
            result = shift.pk
    if(result == 'Unknown'):
        result = 'Duplicate'
    return result


# returns: {"success":"true", "shift_pk":<pk>}
#      or: {"success":"false", "msg":["BadEvent" | "Duplicate"], "event_pk":"None"}
def insertShift(eventFK, shiftDict, db):
    shift = extractShiftFromDict(shiftDict)
    shift.eventFK = eventFK
    result = _insertShift(shift, db)
    if result != 'BadEvent' and result != 'Duplicate':
        resultJSON = '{"success":"true",'
    else:
        resultJSON = '{' + '"success":"false","msg":"{val}",'.format(val=result)
    
    if shift.pk is not None:
        resultJSON += '"{key}":{val}'.format(key=models.SHIFT_PK_KEY, val=shift.pk)
    else:
        resultJSON += '"{key}":"None"'.format(key=models.SHIFT_PK_KEY)
    resultJSON += '}'
    return resultJSON


# Returns True on success or False on failure (couldn't find the shift).
def _removeShift(pk, db):
    shift = models.Shift.query.filter_by(pk=pk).first()
    result = False
    if shift is not None:
        db.session.delete(shift)
        db.session.commit()
        result = True
    return result
    

# Returns JSON: {"success":["true" | "false"],"shift_pk":<pk>}
def removeShift(pk, db):
    result = _removeShift(pk, db)
    resultJSON = '{'+ '"success":"{val}",'.format(val="true" if result == True else "false")
    resultJSON += '"{key}":{val}'.format(result=result, key=models.SHIFT_PK_KEY, val=pk)
    resultJSON += '}'
    return resultJSON

