from flask import *
import models


# Organizations
def getAllOrganizations(db):
    results = models.Organization.query.all()
    return results

def getAllOrganizationsJSON(db):
    allOrgs = getAllOrganizations(db)
    isFirst = True
    jsonString = '{"Organizations":['
    for org in allOrgs:
        if(isFirst == False):
            jsonString += ','
        else:
            isFirst = False
        jsonString += organizationToJSON(org)
    jsonString += ']}'
    return jsonString


def registerOrganization(jsonString, db):
    result = False
    failCause = 'Unknown'

    # Added this check here to just by pass if the input is a dict object
    # else turn josn into dict. Dan has email Mr. Zapp regrading to clarify
    # should all controller code accept json string or dict object. At incoming 
    # request, Flask will parse JSON string into dict object.
    # if isinstance(request.form, dict): 
    #     org = extractOrganizationFromJSON(jsonString)
    # else:
    ''' Parse the given JSON data and create our basic organization. '''
    data = json.loads(jsonString)
    org = extractOrganizationFromJSON(data)


    ''' Check for duplicate organization. '''
    #existing = models.Organization.query.filter_by(name = org.name).first()
    isDuplicate = _checkForDuplicateOrganization(org)
    if(isDuplicate is True):
        failCause = 'duplicate'
    else:
        db.session.add(org)
        db.session.commit()
        result = True

    
    if(result is True):
        resultJson = '{"result": "True"}'
    else:
        resultJson = '{' + '"result": "{val}"'.format(val=failCause) + '}'
    return resultJson


""" Internal method for checking for djuplicates. Currently only checks
    the organization.name property. Since it doesn't use JSON, this is not
    meant for the view code to use. """
def _checkForDuplicateOrganization(org):
    result = False
    if(org is not None and org.name is not None):
        existing = models.Organization.query.filter_by(name = org.name).first()
        if(existing is not None):
            result = True
    return result


""" Allows the view to check whether a given organization name already exists
    in the application. Returns True if duplicated. """
def checkForDuplicateOrganizationNameJSON(orgNameJSON):
    result = False
    orgNameDict = json.loads(orgNameJSON)
    if(orgNameDict is not None and orgNameDict[models.ORGANIZATION_NAME_KEY] is not None):
        orgName = orgNameDict[models.ORGANIZATION_NAME_KEY]
        org = models.Organization()
        org.name = orgName
        result = _checkForDuplicateOrganization(org)

    resultJSON = '{'
    resultJSON += '"result":"{val}"'.format(val=result)
    resultJSON += '}'
    return resultJSON


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


""" Converts an Organization (including the entity object) into JSON format. """
def organizationToJSON(org):
    jsonString = '{' + '"{key}":{val},'.format(key=models.ORGANIZATION_ENTITYFK_KEY,val=org.entityFK if (org.entityFK is not None) else '"None"')
    jsonString += '"{key}":"{val}",'.format(key=models.ORGANIZATION_NAME_KEY,val=org.name)
    jsonString += '"{key}":"{val}",'.format(key=models.ORGANIZATION_DESCRIPTION_KEY,val=org.description)
    jsonString += '"Entity":{val}'.format(val=entityToJSON(org.entity))
    jsonString += '}'
    return jsonString

""" Converts an Entity (including related objects) into JSON format. """
def entityToJSON(entity):
    jsonString = '{' + '"{key}":{val},'.format(key=models.ENTITY_PK_KEY,val=entity.pk if (entity.pk is not None) else '"None"')
    jsonString += '"{key}":"{val}",'.format(key=models.ENTITY_TYPE_KEY,val=entity.type if (entity.type is not None) else '"None"')
    jsonString += '"addresses":['

    isFirst = True
    for addr in entity.addresses:
        if(isFirst == False):
            jsonString += ','
        else:
            isFirst = False
        jsonString += addressToJSON(addr)
    jsonString += ']'
    
    isFirst = True
    jsonString += ', "contacts":['
    for contact in entity.contacts:
        if(isFirst == False):
            jsonString += ','
        else:
            isFirst = False
        jsonString += contactToJSON(contact)
    jsonString += ']}'
    return jsonString

""" Converts an Address into JSON format. """
def addressToJSON(address):
    jsonString = '{' + '"{key}":{val},'.format(key=models.ADDRESS_ENTITYFK_KEY,val=address.entityFK if address.entityFK != None else '"None"')
    jsonString += '"{key}":"{val}",'.format(key=models.ADDRESS_ADDRESS1_KEY,val=address.address1)
    jsonString += '"{key}":"{val}",'.format(key=models.ADDRESS_ADDRESS2_KEY,val=address.address2)
    jsonString += '"{key}":"{val}",'.format(key=models.ADDRESS_ADDRESS3_KEY,val=address.address3)
    jsonString += '"{key}":"{val}",'.format(key=models.ADDRESS_CITY_KEY,val=address.city)
    jsonString += '"{key}":"{val}",'.format(key=models.ADDRESS_PROVINCE_KEY,val=address.province)
    jsonString += '"{key}":"{val}",'.format(key=models.ADDRESS_COUNTRY_KEY,val=address.country)
    jsonString += '"{key}":"{val}",'.format(key=models.ADDRESS_POSTALCODE_KEY,val=address.postalcode)
    jsonString += '"{key}":"{val}"'.format(key=models.ADDRESS_ISPRIMARY_KEY,val=address.isprimary if address.isprimary != None else 'False')
    jsonString += '}'
    return jsonString

""" Converts a Contact into JSON format. """
def contactToJSON(contact):
    jsonString = '{' + '"{key}":{val},'.format(key=models.CONTACT_ENTITYFK_KEY,val=contact.entityFK if contact.entityFK != None else '"None"')
    jsonString += '"{key}":"{val}",'.format(key=models.CONTACT_TYPE_KEY,val=contact.type)
    jsonString += '"{key}":"{val}",'.format(key=models.CONTACT_VALUE_KEY,val=contact.value)
    jsonString += '"{key}":"{val}"'.format(key=models.CONTACT_ISPRIMARY_KEY,val=contact.isprimary if contact.isprimary != None else 'False')
    jsonString += '}'
    return jsonString


""" Converts an Organization in JSON format to an Organization object. """
def extractOrganizationFromJSON(organization):
    newOrg = models.Organization()
    for orgKey,orgValue in organization.iteritems():
        if(orgKey == models.ORGANIZATION_ENTITYFK_KEY and orgValue != 'None'):
            newOrg.entityFK = int(orgValue)
        if(orgKey == models.ORGANIZATION_NAME_KEY):
            newOrg.name = orgValue
        if(orgKey == models.ORGANIZATION_DESCRIPTION_KEY):
            newOrg.description = orgValue
        if(orgKey == 'Entity'):
            newOrg.entity = extractEntityFromJSON(orgValue)
    return newOrg


""" Converts an Entity in JSON format to an Entity object. """
def extractEntityFromJSON(entity):
    newEntity = models.Entity()
    for entityKey,entityValue in entity.iteritems():
        if(entityKey == models.ENTITY_PK_KEY and entityValue != 'None'):
            newEntity.pk = int(entityValue)
        if(entityKey == models.ENTITY_TYPE_KEY):
            newEntity.type = int(entityValue)
        if(entityKey == 'addresses'):
            for address in entityValue:
                newAddress = extractAddressFromJSON(address)
                newEntity.addresses.append(newAddress)
        
        if(entityKey == 'contacts'):
            for contact in entityValue:
                newContact = extractContactFromJSON(contact)
                newEntity.contacts.append(newContact)
    return newEntity
    

""" Converts an Address in JSON format to an Address object. """
def extractAddressFromJSON(address):
    newAddress = models.Address()
    for addrKey,addrValue in address.iteritems():
        if(addrKey == models.ADDRESS_ENTITYFK_KEY and addrValue != 'None'):
            newAddress.entityFK = int(addrValue)
        if(addrKey == models.ADDRESS_ADDRESS1_KEY and addrValue != 'None'):
            newAddress.address1 = addrValue
        if(addrKey == models.ADDRESS_ADDRESS2_KEY and addrValue != 'None'):
            newAddress.address2 = addrValue
        if(addrKey == models.ADDRESS_ADDRESS3_KEY and addrValue != 'None'):
            newAddress.address3 = addrValue
        if(addrKey == models.ADDRESS_CITY_KEY and addrValue != 'None'):
            newAddress.city = addrValue
        if(addrKey == models.ADDRESS_PROVINCE_KEY and addrValue != 'None'):
            newAddress.province = addrValue
        if(addrKey == models.ADDRESS_COUNTRY_KEY and addrValue != 'None'):
            newAddress.country = addrValue
        if(addrKey == models.ADDRESS_POSTALCODE_KEY and addrValue != 'None'):
            newAddress.postalcode = addrValue
        if(addrKey == models.ADDRESS_ISPRIMARY_KEY):
            newAddress.isprimary = True if (addrValue == 'True') else False
    return newAddress


""" Extracts a Contact in JSON format to a Contact object. """
def extractContactFromJSON(contact):
    newContact = models.Contact()
    for contactKey,contactValue in contact.iteritems():
        if(contactKey == models.CONTACT_ENTITYFK_KEY and contactValue != 'None'):
            newContact.entityFK = int(contactValue)
        if(contactKey == models.CONTACT_TYPE_KEY):
            newContact.type = int(contactValue)
        if(contactKey == models.CONTACT_VALUE_KEY):
            newContact.value = contactValue
        if(contactKey == models.CONTACT_ISPRIMARY_KEY):
            newContact.isprimary = True if (contactValue == 'True') else False
    return newContact



""" Controller code related to Permissions/Privileges """
""" Retrieve all privileges for a person in an organization. """
# Returns a list of Privilege objects on success, or None on failure.
def _getPrivilegesForPerson(personKey, organizationKey):
    privileges = list()
    returnValue = None
    
    member = models.Member.query.filter_by(personentityFK=personKey, organizationentityFK=organizationKey).first()
    if member is not None:
        personPrivs = models.PrivilegePersonAssignment.query.filter_by(memberFK=member.pk)

        count = 0
        for key in personPrivs:
            privilege = models.Privilege.query.filter_by(pk=key.privilegeFK).first()
            privileges.append(privilege)
            count += 1
        if count > 0:
            returnValue = privileges
        else:
            returnValue = None
    else:
        returnValue = None

    return returnValue

""" Retrieve all organizations that the given person has privileges for. """
# Returns a list of organizationentityFK values on success, or None on failure.
def _getOrgsWithPrivilegesForPerson(personKey):
    orgKeys = list()
    returnValue = None
    
    memberList = models.Member.query.filter_by(personentityFK=personKey)
    if memberList is not None:
        count = 0
        for member in memberList:
            hasPrivs = False
            ppaList = models.PrivilegePersonAssignment.query.filter_by(memberFK=member.pk)
            if ppaList is not None and member.organizationentityFK not in orgKeys:
                count += 1
                orgKeys.append(member.organizationentityFK)

        if count > 0:
            returnValue = orgKeys
        else:
            returnValue = None
    else:
        returnValue = None

    return returnValue

""" Retrieve all global privileges for a given person. """
# Returns a list of Privilege objects on success, or None on failure.
def _getGlobalPrivilegesForPerson(personKey):
    privileges = list()
    returnValue = None

    globalPrivs = models.GlobalPrivilegeAssignment.query.filter_by(personentityFK=personKey)
    
    count = 0
    for key in globalPrivs:
        privilege = models.Privilege.query.filter_by(pk=key.privilegeFK).first()
        privileges.append(privilege)
        count += 1
    if count > 0:
        returnValue = privileges
    else:
        returnValue = None

    return returnValue


""" Retrieves all organization keys where the given person has the given privilege. """
# Returns a list of organization entityFK values where the given person has
#   the given privilege, or None if the person does not have that privilege
#   with any organizations, or if the personKey or privilegeKey are invalid.
# NOTE that this will return None if the person has the privilege as a global
#   privilege and not as one related to a specific organization.
def _getOrgsWithPersonPrivilege(personKey, privilegeKey):
    orgKeys = list()
    returnValue = None
    
    memberList = models.Member.query.filter_by(personentityFK=personKey)
    if memberList is not None:
        count = 0
        for member in memberList:
            ppaList = models.PrivilegePersonAssignment.query.filter_by(memberFK=member.pk, privilegeFK=privilegeKey)
            if ppaList is not None and member.organizationentityFK not in orgKeys:
                orgKeys.append(member.organizationentityFK)
                count += 1
        if count > 0:
            returnValue = orgKeys
    else:
        returnValue = None

    return returnValue


""" Retrieve all person keys associated with the given organization. """
# Returns a list of person entityFK values, or None if the person has no
#   privileges in the given organization, or the organization key is invalid.
def _getPeopleInOrganization(organizationKey):
    personKeys = list()
    returnValue = None

    memberList = models.Member.query.filter_by(organizationentityFK=organizationKey)
    if memberList is not None:
        count = 0
        for member in memberList:
            if member.personentityFK not in personKeys:
                personKeys.append(member.personentityFK)
                count += 1
        if count > 0:
            returnValue = personKeys
    else:
        returnValue = None

    return returnValue

""" Public method to retrieve privileges for a person. """
# Can optionally include an organization key to get privileges specific
# to that organization.
# JSON format: {"emp_entityfk":<number>[, "org_entityfk":<organizationKey>]}
#def getPrivilegesForPerson(jsonString):
    

# validate a person has a required member privilege for an organiation
# validate a person has a required global privilege


""" Grant a privilege to a person. """
# Returns True if the privilege was added or already existed.
# Returns False if one of the given keys did not correlate to a necessary
#   database object.
def _grantPrivilegeToPerson(db, privilegeKey,personKey,organizationKey=None):
    returnValue = False
    privilege = models.Privilege.query.filter_by(pk=privilegeKey).first()
    person = models.Person.query.filter_by(entityFK=personKey).first()
    organization = None
    if organizationKey is not None:
        organization = models.Organization.query.filter_by(entityFK=organizationKey).first()
        if person is not None and organization is not None:
            member = models.Member.query.filter_by(personentityFK=personKey, organizationentityFK=organizationKey).first()
            if member is not None and privilege is not None:
                ppa = models.PrivilegePersonAssignment.query.filter_by(memberFK=member.pk, privilegeFK=privilegeKey).first()
                if ppa is None:
                    ppa = models.PrivilegePersonAssignment(memberFK=member.pk, privilegeFK=privilegeKey)
                    if ppa is not None:
                        db.session.add(ppa)
                        db.session.commit()
                        returnValue = True
                else:
                    returnValue = True
    elif privilege is not None and person is not None:
        gpa = models.GlobalPrivilegeAssignment.query.filter_by(privilegeFK=privilegeKey, personentityFK=personKey).first()
        if gpa is None:
            gpa = models.GlobalPrivilegeAssignment(privilegeFK=privilegeKey, personentityFK=personKey)
            if gpa is not None:
                db.session.add(gpa)
                db.session.commit()
                returnValue = True
        else:
            returnValue = True

    return returnValue

# revoke a privilege from a person
def _revokePrivilegeForPerson(db, privilegeKey,personKey,organizationKey=None):
    returnValue = False
    privilege = models.Privilege.query.filter_by(pk=privilegeKey).first()
    person = models.Person.query.filter_by(entityFK=personKey).first()
    organization = None
    if organizationKey is not None:
        organization = models.Organization.query.filter_by(entityFK=organizationKey).first()
        if person is not None and organization is not None:
            member = models.Member.query.filter_by(personentityFK=personKey, organizationentityFK=organizationKey).first()
            if member is not None and privilege is not None:
                ppa = models.PrivilegePersonAssignment.query.filter_by(memberFK=member.pk, privilegeFK=privilegeKey).first()
                if ppa is not None:
                    db.session.delete(ppa)
                    db.session.commit()
                    returnValue = True
                else:
                    returnValue = True
    elif privilege is not None and person is not None:
        gpa = models.GlobalPrivilegeAssignment.query.filter_by(privilegeFK=privilegeKey, personentityFK=personKey).first()
        if gpa is not None:
            db.session.delete(gpa)
            db.session.commit()
            returnValue = True
        else:
            returnValue = True

    return returnValue
