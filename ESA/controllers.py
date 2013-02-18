from flask import *
import models

# Organizations
def getAllOrganizations():
    controller = models.Organization()
    results = controller.getAll()
    print results
    jsonified = [org.serialize for org in results]
    return jsonified

def insertOrganization(name, description):
    controller = models.Organization()
    result = controller.insert(name, description);
    print result

def updateOrganization(entityid, name, description):
    controller = models.Organization()
    result = controller.update(entityid, name, description);
    print result

def getOrganizationByID(entityid):
    controller = models.Organization()
    results = controller.getByID(entityid)
    jsonified = [org.serialize for org in results]
    return jsonified

def removeOrganization():
    return
