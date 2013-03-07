from flask import *
import models


""" Retrieve all privileges. """
def _getAllPrivileges():
    return models.Privilege.query.order_by(models.Privilege.privilege).all()

""" Retrieve all privileges and wrap them in JSON. """
# Format: {"Privileges":[<privilege json string>,...]}
def getAllPrivilegesJSON():
    privileges = _getAllPrivileges()
    jsonString = '{"Privileges":'
    if len(privileges) > 0:
        jsonString += '['
        count = 0
        for privilege in privileges:
            if count > 0:
                jsonString += ','
            count += 1
            jsonString += privilegeToJSON(privilege)
        jsonString += ']'
    else:
        jsonString += '"None"'
    jsonString += '}'
    return jsonString
    
    


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
    
""" Retrieve all assigned privileges for a given person in JSON format. """
# Format: {"<person key string>":<person.pk>,"<organization key string>":<org pk>,"PersonPrivileges":[{privilege json format}, ...]}
def getPrivilegesForPersonJSON(personKey, organizationKey):
    privileges = _getPrivilegesForPerson(personKey, organizationKey)
    jsonString = '{'
    jsonString += '"{key}":{value}'.format(key=models.EMPLOYEE_ENTITYFK_KEY, value=personKey)
    jsonString += ',"{key}":{value}'.format(key=models.ORGANIZATION_ENTITYFK_KEY, value=organizationKey)
    jsonString += ',"PersonPrivileges":'
    if len(privileges) > 0:
        jsonString += '['
        count = 0
        for privilege in privileges:
            if count > 0:
                jsonString += ','
            jsonString += privilegeToJSON(privilege)
            count += 1;
        jsonString += ']'
    else:
        jsonString += '"None"'
    jsonString += '}'
    return jsonString



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
    
    
""" Retrieve all organizations that the given person has privileges for in JSON format. """
# Format: {"OrganizationKeys":[#,#,#,#,...]}
def getOrgsWithPrivilegesForPersonJSON(personKey):
    orgKeys = _getOrgsWithPrivilegesForPerson(personKey)
    jsonString = '{"OrganizationKeys":'
    if len(orgKeys) > 0:
        jsonString += '['
        count = 0
        for key in orgKeys:
            if count > 0:
                jsonString += ','
            count += 1
            jsonString += str(key)  # convert key to string for concatenation, python restriction
        jsonString += ']'
    else:
        jsonString += '"None"'
    jsonString += '}'
    return jsonString



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
    

""" Retrieve all global privileges for a given person in JSON format. """
# Format: {"<person key string>":<person.pk>, "GlobalPrivileges":[{privilege json format}, ...]}
def getGlobalPrivilegesForPersonJSON(personKey):
    privileges = _getGlobalPrivilegesForPerson(personKey)
    jsonString = '{'
    jsonString += '"{key}":{value}'.format(key=models.EMPLOYEE_ENTITYFK_KEY, value=personKey)
    jsonString += ',"GlobalPrivileges":'
    if len(privileges) > 0:
        jsonString += '['
        count = 0
        for privilege in privileges:
            if count > 0:
                jsonString += ','
            jsonString += privilegeToJSON(privilege)
            count += 1;
        jsonString += ']'
    else:
        jsonString += '"None"'
    jsonString += '}'
    return jsonString
    


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

""" Retrieves all organization keys where the given person has the given privilege, in JSON format. """
# Format: {"OrganizationKeys":[#,#,#,#,...]}    
def getOrgsWithPersonPrivilegeJSON(personKey, privilegeKey):
    orgKeys = _getOrgsWithPersonPrivilege(personKey, privilegeKey)
    jsonString = '{"OrganizationKeys":'
    if orgKeys is not None and len(orgKeys) > 0:
        jsonString += '['
        count = 0
        for key in orgKeys:
            if count > 0:
                jsonString += ','
            count += 1
            jsonString += str(key)  # convert key to string for concatenation, python restriction
        jsonString += ']'
    else:
        jsonString += '"None"'
    jsonString += '}'
    return jsonString



""" Grant a privilege to a person. """
# Returns True if the privilege was added or already existed.
# Returns False if one of the given keys did not correlate to a necessary
#   database object.
# If OrganizationKey is not included, then it is assumed this refers to a global privilege.
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

""" Grant a privilege to a person, result returned in JSON format. """
# Format: {"Result":"True"} or {"Result":"False"}
def grantPrivilegeToPersonJSON(db, privilegeKey, personKey, organizationKey=None):
    result = _grantPrivilegeToPerson(db, privilegeKey,personKey,organizationKey)
    resultString = "True"
    if result is False:
        resultString = "False"
    jsonString = '{"Result":' + '"{val}"'.format(val=resultString) + '}'
    return jsonString


""" Revoke a privilege from a person. """
# Returns True if the privilege was revoked or was not owned by the person.
# Returns False if one of the given keys did not correlate to a necessary
#   database object.
# If OrganizationKey is not included, then it is assumed this refers to a global privilege.
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
    
    
    
""" Converts a Privilege into JSON format. """
def privilegeToJSON(privilege):
    jsonString = '{' + '"{key}":{val},'.format(key=models.PRIVILEGE_PK_KEY,val=privilege.pk if privilege.pk != None else '"None"')
    jsonString += '"{key}":"{val}"'.format(key=models.PRIVILEGE_VALUE,val=privilege.privilege if privilege.privilege != None else '"None"')
    jsonString += '}'
    return jsonString
    
    

""" Extracts a Privilege in Dict format to a Privilege object. """
def extractPrivilegeFromDict(privilege):
    newPrivilege = models.Privilege()
    for key,value in privilege.iteritems():
        if(key == models.PRIVILEGE_PK_KEY and value != 'None'):
            newPrivilege.pk = int(value)
        if(key == models.PRIVILEGE_VALUE):
            newPrivilege.privilege = value
    return newPrivilege
    
    
    
""" Public method to retrieve privileges for a person. """
# Can optionally include an organization key to get privileges specific
# to that organization.
# JSON format: {"emp_entityfk":<number>[, "org_entityfk":<organizationKey>]}
#def getPrivilegesForPerson(jsonString):
    

# validate a person has a required member privilege for an organiation
# validate a person has a required global privilege
