from flask import *
import models


# Organizations
def getAllOrganizations():
    db = models.init_app(self.app)
    results = db.Organization.query.all()
    print results
    return results
    '''controller = models.Organization()
    results = controller.getAll()
    print results
    jsonified = [org.serialize for org in results]
    return jsonified'''


def registerOrganization(jsonString):
    result = False
    failCause = 'Unknown'

    """ Parse the given JSON data and create our basic organization. """
    data = json.loads(jsonString)
    org = models.Organization()
    org.entity = models.Entity(type=models.TYPE_ORGANIZATION)

    primaryAddress = models.Address()
    primaryAddress.isprimary = True
    
    email = models.Contact()
    email.type = models.TYPE_EMAIL

    primaryPhone = models.Contact()
    primaryPhone.type = models.TYPE_PHONE
    primaryPhone.isprimary = True

    """ Iterate over given key-value pairs and update model fields as needed. """
    for key,value in data.iteritems():
        if(key == models.ORGANIZATION_NAME_KEY):
            org.name = value
        if(key == models.ORGANIZATION_DESCRIPTION_KEY):
            org.description = value

        if(key == models.ADDRESS_ADDRESS1_KEY):
            primaryAddress.address1 = value
            isValidAddress = True
        if(key == models.ADDRESS_ADDRESS2_KEY):
            primaryAddress.address2 = value
            isValidAddress = True
        if(key == models.ADDRESS_ADDRESS3_KEY):
            primaryAddress.address3 = value
            isValidAddress = True
        if(key == models.ADDRESS_CITY_KEY):
            primaryAddress.city = value
            isValidAddress = True
        if(key == models.ADDRESS_PROVINCE_KEY):
            primaryAddress.province = value
            isValidAddress = True
        if(key == models.ADDRESS_COUNTRY_KEY):
            primaryAddress.country = value
            isValidAddress = True
        if(key == models.ADDRESS_POSTALCODE_KEY):
            primaryAddress.postalcode = value
            isValidAddress = True

        if(key == models.CONTACT_EMAIL_KEY):
            email.value = value
            isValidEmail = True

        if(key == models.CONTACT_PHONE_KEY):
            primaryPhone.value = value
            isValidPhone = True

    
    """ If the additional info types were included in the call, append
        them to the organization (entity). """
    if(isValidAddress == True):
        org.entity.addresses.append(primaryAddress)

    if(isValidPhone == True):
        org.entity.contacts.append(primaryPhone)
    else:
        email.isprimary = True

    if(isValidEmail == True):
        org.entity.contacts.append(email)


    """ Check for duplicate organization. """
    existing = models.Organization.query.filter_by(name = org.name).first()
    if(existing != None):
        failCause = 'duplicate'
    else:
        db = models.init_app(self.app)
        db.session.add(org1)
        db.session.commit()
        result = True

    
    if(result == True):
        resultJson = "{'result': 'true'}"
    else:
        resultJson = "{'result': " + failCause + "}"
    return resultJson



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
