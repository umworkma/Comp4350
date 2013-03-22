#####################################
# events.py
# Controller code relating to events
#####################################

from flask import *
import models
import controllers
from datetime import datetime

#####################################
# extractEventFromDict
# Takes a dict of event data and parses
# it into a new event object then
# returns the event object
#####################################
def extractEventFromDict(eventDict):
    newEvent = models.Event()

    for eventKey, eventValue in eventDict.iteritems():
        if(eventKey == models.EVENT_PK_KEY and eventValue != 'None'):
            newEvent.pk = int(eventValue)
        if(eventKey == models.EVENT_NAME_KEY):
            newEvent.name = eventValue
        if(eventKey == models.EVENT_DESC_KEY):
            newEvent.description = eventValue
        if(eventKey == models.EVENT_START_KEY):
            newEvent.startdate = datetime.strptime(eventValue, '%Y-%m-%d %H:%M:%S')
        if(eventKey == models.EVENT_END_KEY):
            newEvent.enddate = datetime.strptime(eventValue, '%Y-%m-%d %H:%M:%S')
        if(eventKey == models.EVENT_ORGFK_KEY):
            newEvent.organizationFK = eventValue

    return newEvent

def eventToJSON(event):
    jsonString = '{' + '"{key}":{val},'.format(key=models.EVENT_PK_KEY, val=event.pk if event.pk != None else '"None"')
    jsonString += '"{key}":"{val}",'.format(key=models.EVENT_NAME_KEY, val=event.name)
    jsonString += '"{key}":"{val}",'.format(key=models.EVENT_DESC_KEY, val=event.description)
    jsonString += '"{key}":"{val}",'.format(key=models.EVENT_START_KEY, val=event.startdate)
    jsonString += '"{key}":"{val}",'.format(key=models.EVENT_END_KEY, val=event.enddate)
    jsonString += '"{key}":"{val}"'.format(key=models.EVENT_ORGFK_KEY, val=event.organizationFK)
    jsonString += '}'
    return jsonString

def _getEventByID(pk, db):
    return models.Event.query.get(pk)

def getAllOrgsEvents(orgId, db):
    results = models.Event.query.filter_by(organizationFK=orgId)

# Returns True or False
def _isDuplicateEvent(event, db):
    result = True
    target = models.Event.query.filter_by(name=event.name, startdate=event.startdate, enddate=event.enddate, organizationFK=event.organizationFK).first()
    if(target == None):
        result = False
    return result

# Return values: BadOrg = couldn't find org matching event.organizationFK
#                Duplicate = found an existing event with same name/start/end/org
#                event.pk = new pk of event successfully added
def _insertEvent(event, db):
    result = 'Unknown'
    isDup = _isDuplicateEvent(event, db)
    org = controllers._getOrganizationByID(event.organizationFK)
    if org is None:
        result = 'BadOrg'
    if(isDup == False and result == 'Unknown'):
        db.session.add(event)
        db.session.commit()
        if(event.pk > 0):
            result = event.pk
    if(result == 'Unknown'):
        result = 'Duplicate'
    return result


# returns: {"result":"True", "event_pk":<pk>}
#      or: {"result":["BadOrg" | "Duplicate"], "event_pk":"None"}
def insertEvent(orgFK, eventDict, db):
    event = extractEventFromDict(eventDict)
    event.organizationFK = orgFK
    result = _insertEvent(event, db)
    if result != 'BadOrg' and result != 'Duplicate':
        resultJSON = '{"result":"True",'
    else:
        resultJSON = '{' + '"result":"{val}",'.format(val=result)
    
    if event.pk is not None:
        resultJSON += '"{key}":{val}'.format(key=models.EVENT_PK_KEY, val=event.pk)
    else:
        resultJSON += '"{key}":"None"'.format(key=models.EVENT_PK_KEY)
    resultJSON += '}'
    return resultJSON


def updateEvent(pk, name, description, startdate, enddate, organizationFK):
    controller = models.Event()
    result = controller.update(pk, name, description, startdate, enddate, organizationFK);
    print result


# Returns True on success or False on failure (couldn't find the event).
def _removeEvent(pk, db):
    event = models.Event.query.filter_by(pk=pk).first()
    result = False
    if event is not None:
        db.session.delete(event)
        db.session.commit()
        result = True
    return result
    

# Returns JSON: {"result":["True" | "False"],"event_pk":<pk>}
def removeEvent(pk, db):
    result = _removeEvent(pk, db)
    resultJSON = '{'+ '"result":"{result}",'
    resultJSON += '"{key}":{val}'.format(result=result, key=models.EVENT_PK_KEY, val=pk)
    resultJSON += '}'
    return resultJSON

