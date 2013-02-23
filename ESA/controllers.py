from flask import *
import models

# Employees
def registerEmployee(jsonString, db):
    result = False
    failCause = 'Unknown'
    data = json.loads(jsonString)
    employee = extractEmployeeFromJSON(data)
	
	isDuplicate = _checkForDuplicateEmployee(employee)
	# if(isduplicate is true):
		# failcause = 'duplicate'
	# else:
		# db.session.add(employee)
        # db.session.commit()
		# result = true
	
		# if(result is true):
			# resultjson = '{"result": "true"}'
		# else:
			# resultjson = '{' + '"result": "{val}"'.format(val=failcause) + '}'
		# return resultjson




""" Allows the view to check whether a given  username already exists
    in the application. Returns True if duplicated. """
def checkForDuplicateEmployeeUserNameJSON(employeeUserNameJSON):
    result = False
    employeeUserNameDict = json.loads(employeeUserNameJSON)
    if(employeeUserNameDict is not None and employeeUserNameDict[models.EMPLOYEE_USER_NAME_KEY] is not None):
        employeeUserName = employeeUserNameDict[models.EMPLOYEE_USER_NAME_KEY]
        employee = models.Employee()
        employee.username = employeeUserName
        result = _checkForDuplicateEmployee(employee)

    resultJSON = '{'
    resultJSON += '"result":"{val}"'.format(val=result)
    resultJSON += '}'
    return resultJSON



""" Internal method for checking for duplicate employee. Currently only checks
    the employee.username property. """

def _checkForDuplicateEmployee(employee):
    result = False
    if(employee is not None and employee.username is not None):
        existing = models.Employee.query.filter_by(username = employee.username).first()
        if(existing is not None):
            result = True
    return result
 

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


""" Converts an employee in JSON format to an employee object. """
def extractEmployeeFromJSON(employee):
    employee = models.Person()
    for employeeKey,employeeValue in employee.iteritems():
        if(employeeKey == models.EMPLOYEE_ENTITYFK_KEY and employeeValue != 'None'):
            employee.entityFK = int(employeeValue)
        # if(employeeKey == models.EMPLOYEE_USER_NAME_KEY):
            # employee.username = employeeValue
        if(employeeKey == models.EMPLOYEE_FIRST_NAME_KEY):
            employee.firstname = employeeValue
        if(employeeKey == models.EMPLOYEE_LAST_NAME_KEY):
            employee.lastname = employeeValue
        # if(employeeKey == models.EMPLOYEE_PASSWORD_KEY):
            # employee.password = employeeValue
        if(employeeKey == 'Entity'):
            employee.entity = extractEntityFromJSON(employeeValue)
    return employee


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
