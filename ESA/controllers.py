from flask import *
import models

# Organizations
def getAllOrganizations():
    org = models.Organization()
    results = org.getAll()
    return results

def insertOrganization(jsonParams):
    data = json.loads(jsonParams)
    print data

def getOrganization():
    return

def removeOrganization():
    return
