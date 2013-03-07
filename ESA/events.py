#####################################
# events.py
# Controller code relating to events
#####################################

from flask import *
import models

#####################################
# registerEvent
# Handles registration of a new event
# Requires event dict object and database pointer
# Will update the database and notify of success
# of provide cause of failure
#####################################
def registerEvent(eventDict, db):
    result = False
    failCause = 'Unknown'

    ''' Parse the dict data and create a basic event object '''
    event = extractEventFromDict(eventDict)

####################################
# extractEventFromDict
# Takes a dict object of event data and
# returns an Event object
####################################
def extractEventFromDict(eventDict):
    newEvent = models.Event()

    for eventKey, eventValue in eventDict:
        if(eventKey == models.EVENT_PK_KEY and eventValue != 'None'):
            newEvent.pk = int(eventValue)
        if(eventKey == models.EVENT_NAME_KEY):
            newEvent.name = eventValue
        if(eventKey == models.EVENT_DESC_KEY):
            newEvent.description = eventValue
        if(eventKey == models.EVENT_START_KEY):
            newEvent.startdate = datetime.datetime.strptime(eventValue, '%Y-%m-%dT%H:%M:%S.%f')
        if(eventKey == models.EVENT_END_KEY):
            newEvent.enddate = datetime.datetime.strptime(eventValue, '%Y-%m-%dT%H:%M:%S.%f')
        if(eventKey == models.EVENT_ORGFK_KEY):
            newEvent.organizationFK = eventValue

    return newEvent
