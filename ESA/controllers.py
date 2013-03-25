from flask import *
import models

# Login
def getPersonById(empId, db):
    return models.Person.query.get(empId)

def getPersonByUsername(username, db):
    if username:
        person = models.Person.query.filter_by(username=username).first()

        if person is not None:
            return person
    
    return None

# Employees

def registerEmployee(employeeDict, db):
    result = False
    failCause = 'Unknown'
    employee = extractEmployeeFromDict(employeeDict)
    isDuplicate = _checkForDuplicateEmployee(employee)

    if(isDuplicate is True):
        failcause = 'duplicate'
    else:
        db.session.add(employee)
        db.session.commit()
        result = True
    if(result is True):
        resultjson = '{"username":"'+employee.username+'"}'
    else:
        resultjson = '{' + '"result": "{val}"'.format(val=failcause) + '}'
    return resultjson


""" Internal method for checking for duplicate employee. Currently only checks
    the employee.username property. """

def _checkForDuplicateEmployee(employee):
    result = False
    if(employee is not None and employee.username is not None):
        existing = models.Person.query.filter_by(username = employee.username).first()      
        if(existing is not None):
            result = True
    return result

""" Allows the view to check whether a given  username already exists
    in the application. Returns True if duplicated. """
def checkForDuplicateEmployeeUserName(employeeUserNameDict):
    result = False
   
    if(employeeUserNameDict is not None and employeeUserNameDict[models.EMPLOYEE_USER_NAME_KEY] is not None):
        employeeUserName = employeeUserNameDict[models.EMPLOYEE_USER_NAME_KEY]
        employee = models.Person()
        employee.username = employeeUserName
        result = _checkForDuplicateEmployee(employee)

    resultJSON = '{'
    resultJSON += '"result":"{val}"'.format(val=result)
    resultJSON += '}'
    return resultJSON

""" Converts an Employee (including the entity object) into JSON format. """
def employeeToJSON(emp):
    jsonString = '{' + '"{key}":{val},'.format(key=models.EMPLOYEE_ENTITYFK_KEY,val=emp.entityFK if (emp.entityFK is not None) else '"None"')
    jsonString += '"{key}":"{val}",'.format(key=models.EMPLOYEE_USER_NAME_KEY,val=emp.username)
    jsonString += '"{key}":"{val}",'.format(key=models.EMPLOYEE_PASSWORD_KEY,val=emp.password)
    jsonString += '"{key}":"{val}",'.format(key=models.EMPLOYEE_FIRST_NAME_KEY,val=emp.firstname)
    jsonString += '"{key}":"{val}",'.format(key=models.EMPLOYEE_LAST_NAME_KEY,val=emp.lastname)
    jsonString += '"Entity":{val}'.format(val=entityToJSON(emp.entity))
    jsonString += '}'
    return jsonString


# Organizations
def getAllOrganizations(db):
    results = models.Organization.query.order_by(models.Organization.name).all()
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

def getAllOrgNamesJSON(db):
    allOrgs = getAllOrganizations(db)
    isFirst = True
    jsonString = '{"OrgNames":['
    for org in allOrgs:
        if (isFirst == False):
            jsonString += ','
        else:
            isFirst = False
        jsonString += '{' + '"{key}":{val},'.format(key=models.ORGANIZATION_ENTITYFK_KEY,val=org.entityFK if (org.entityFK is not None) else '"None"')
        jsonString += '"{key}":"{val}"'.format(key=models.ORGANIZATION_NAME_KEY,val=org.name)
        jsonString += '}'
    jsonString += ']}'
    return jsonString

def registerOrganization(orgDict, db):
    result = False
    failCause = 'Unknown'

    ''' Parse the given JSON data and create our basic organization. '''
    org = extractOrganizationFromDict(orgDict)


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
def checkForDuplicateOrganizationName(orgNameDict):
    result = False

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

def _getOrganizationByID(entityid):
    controller = models.Organization()
    results = controller.query.filter_by(entityFK=entityid).first()
    return results

def getOrganizationByIDJSON(entityid):
    #controller = models.Organization()
    #results = controller.query.filter_by(entityFK=entityid).first()
    results = _getOrganizationByID(entityid)

    if results == None:
        return None
    
    jsonified = organizationToJSON(results)
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
    
""" Converts a Person into JSON format. """
def personToJSON(person):
    jsonString = '{' + '"{key}":{val},'.format(key=models.EMPLOYEE_ENTITYFK_KEY,val=person.entityFK if person.entityFK != None else '"None"')
    jsonString += '"{key}":"{val}",'.format(key=models.EMPLOYEE_FIRST_NAME_KEY,val=person.firstname)
    jsonString += '"{key}":"{val}",'.format(key=models.EMPLOYEE_LAST_NAME_KEY,val=person.lastname)
    jsonString += '"{key}":"{val}",'.format(key=models.EMPLOYEE_USER_NAME_KEY,val=person.username)
    jsonString += '"{key}":"{val}"'.format(key=models.EMPLOYEE_PASSWORD_KEY,val=person.password)
    jsonString += '}'
    return jsonString


""" Converts an employee in JSON format to an employee object. """
def extractEmployeeFromDict(employee):
    newEmp = models.Person()
    for employeeKey,employeeValue in employee.iteritems():
        if(employeeKey == models.EMPLOYEE_ENTITYFK_KEY and employeeValue != 'None'):
            newEmp.entityFK = int(employeeValue)
        if(employeeKey == models.EMPLOYEE_USER_NAME_KEY):
            newEmp.username = employeeValue
        if(employeeKey == models.EMPLOYEE_PASSWORD_KEY):
            newEmp.password = employeeValue    
        if(employeeKey == models.EMPLOYEE_FIRST_NAME_KEY):
            newEmp.firstname = employeeValue
        if(employeeKey == models.EMPLOYEE_LAST_NAME_KEY):
            newEmp.lastname = employeeValue
        if(employeeKey == 'Entity'):
            newEmp.entity = extractEntityFromDict(employeeValue)
    return newEmp


""" Converts an Organization in Dict format to an Organization object. """
def extractOrganizationFromDict(organization):
    newOrg = models.Organization()
    for orgKey,orgValue in organization.iteritems():
        if(orgKey == models.ORGANIZATION_ENTITYFK_KEY and orgValue != 'None'):
            newOrg.entityFK = int(orgValue)
        if(orgKey == models.ORGANIZATION_NAME_KEY):
            newOrg.name = orgValue
        if(orgKey == models.ORGANIZATION_DESCRIPTION_KEY):
            newOrg.description = orgValue
        if(orgKey == 'Entity'):
            newOrg.entity = extractEntityFromDict(orgValue)
    return newOrg


""" Converts an Entity in Dict format to an Entity object. """
def extractEntityFromDict(entity):
    newEntity = models.Entity()
    for entityKey,entityValue in entity.iteritems():
        if(entityKey == models.ENTITY_PK_KEY and entityValue != 'None'):
            newEntity.pk = int(entityValue)
        if(entityKey == models.ENTITY_TYPE_KEY):
            newEntity.type = int(entityValue)
        if(entityKey == 'addresses'):
            for address in entityValue:
                newAddress = extractAddressFromDict(address)
                newEntity.addresses.append(newAddress)
        
        if(entityKey == 'contacts'):
            for contact in entityValue:
                newContact = extractContactFromDict(contact)
                newEntity.contacts.append(newContact)
    return newEntity
    

""" Converts an Address in Dict format to an Address object. """
def extractAddressFromDict(address):
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


""" Extracts a Contact in Dict format to a Contact object. """
def extractContactFromDict(contact):
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
    
    
""" Extracts a Person in Dict format to a Person object. """
def extractPersonFromDict(person):
    newPerson = models.Person()
    for key,value in person.iteritems():
        if(key == models.EMPLOYEE_ENTITYFK_KEY and value != 'None'):
            newPerson.entityFK = int(value)
        if(key == models.EMPLOYEE_FIRST_NAME_KEY):
            newPerson.firstname = value
        if(key == models.EMPLOYEE_LAST_NAME_KEY):
            newPerson.lastname = value
        if(key == models.EMPLOYEE_USER_NAME_KEY):
            newPerson.username = value
        if(key == models.EMPLOYEE_PASSWORD_KEY):
            newPerson.password = value
    return newPerson
    
    
""" Retrieve all person objects associated with the given organization. """
# Returns a list of person objects associated with the organization, or None if the organization key is invalid or no people are associated.
def _getPeopleInOrganization(organizationKey):
    personList = list()
    personKeys = list()
    returnValue = None

    memberList = models.Member.query.filter_by(organizationentityFK=organizationKey)
    if memberList is not None:
        count = 0
        for member in memberList:
            if member.personentityFK not in personKeys:
                person = models.Person.query.filter_by(entityFK=member.personentityFK).first()
                if person is not None:
                    person.username = ""
                    person.password = ""
                    personList.append(person)
                    personKeys.append(person.entityFK)
                    count += 1
        if count > 0:
            returnValue = personList
    else:
        returnValue = None
    return returnValue
    


""" Retrieve all person objects associated with the given organization, in JSON format. """
# Format: {"People":[<person json string>,...]}
def getPeopleInOrganizationJSON(organizationKey):
    people = _getPeopleInOrganization(organizationKey)
    jsonString = '{"People":'
    if len(people) > 0:
        jsonString += '['
        count = 0
        for person in people:
            if count > 0:
                jsonString += ','
            count += 1
            jsonString += personToJSON(person)
        jsonString += ']'
    else:
        jsonString += '"None"'
    jsonString += '}'
    return jsonString

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

# Members

""" Associate person with organization. """
def putPersonInOrganization(orgid, db, personid):
    result = False
    failCause = 'Unknown'

    ''' Parse the given JSON data and create our basic member. '''
    newMember = models.Member()
    # for key,value in member.iteritems():
    #     if(key == models.ORGANIZATION_ENTITYFK_KEY and value != 'None'):
    #         newMember.organizationentityFK = int(value)

    org = models.Organization.query.filter_by(entityFK=orgid).first()
    person = models.Person.query.filter_by(entityFK=personid).first()
    if org is not None:
        newMember.organizationentityFK = int(orgid)
        if person is not None:
            newMember.personentityFK = int(personid)
            db.session.add(newMember)
            db.session.commit()
            result = True
        else:
            result = False
            failCause = 'person not found'
    else:
        result = False
        failCause = 'organization not found'

    if(result is True):
        resultJson = '{"result": "True"}'
    else:
        resultJson = '{' + '"result": "{val}"'.format(val=failCause) + '}'
    return resultJson

""" Returns json indicating whether the current_user_id belongs to each of the orgs """
def getMemberDataJSON(db, current_user_id):
    joinedOrgs = getJoinedOrgs(db, current_user_id)
    isFirst = True
    jsonString = '{"Orgs_id":['
    for org in joinedOrgs:
        if (isFirst == False):
            jsonString += ','
        else:
            isFirst = False
        if org in joinedOrgs:
            jsonString += '{key}'.format(key=org.organizationentityFK)
        # jsonString += '}'
    jsonString += ']}'
    return jsonString

def getJoinedOrgs(db, current_user_id):
    results = models.Member.query.filter_by(personentityFK = current_user_id)
    return results
