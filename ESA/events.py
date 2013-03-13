#####################################
# events.py
# Controller code relating to events
#####################################

from flask import *
import models
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
            newEvent.startdate = datetime.strptime(eventValue, '%Y-%m-%dT%H:%M:%S.%f')
        if(eventKey == models.EVENT_END_KEY):
            newEvent.enddate = datetime.strptime(eventValue, '%Y-%m-%dT%H:%M:%S.%f')
        if(eventKey == models.EVENT_ORGFK_KEY):
            newEvent.organizationFK = eventValue

    return newEvent

def eventToJSON(event):
    jsonString = '{' + '"{key}":{val},'.format(key=models.EVENT_PK_KEY, val=event.pk if event.pk != None else '"None"')
    jsonString += '"{key}":"{val}",'.format(key=models.EVENT_NAME_KEY, val=event.name)
    jsonString += '"{key}":"{val}",'.format(key=models.EVENT_DESC_KEY, val=event.description)
    jsonString += '"{key}":"{val}",'.format(key=models.EVENT_START_KEY, val=event.startdate)
    jsonString += '"{key}":"{val}",'.format(key=models.EVENT_END_KEY, val=event.enddate)
    jsonString += '"{key}":"{val}",'.format(key=models.EVENT_ORGFK_KEY, val=event.organizationFK)
    jsonString += '}'
    return jsonString

def getEventById(pk, db):
    return models.Event.query.get(pk)

def getAllOrgsEvents(orgId, db):
    results = models.Event.query.filter_by(organizationFK=orgId)

def insertEvent(name, description, startdate, enddate, organizationFK):
    controller = models.Event()
    result = controller.insert(name, description, startdate, enddate, organizationFK);
    print result

def updateEvent(pk, name, description, startdate, enddate, organizationFK):
    controller = models.Event()
    result = controller.update(pk, name, description, startdate, enddate, organizationFK);
    print result

def removeEvent(pk):
    return


