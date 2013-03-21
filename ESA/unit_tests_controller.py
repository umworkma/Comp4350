#!../venv/bin/python
import unittest
import json

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models
import controllers
import events
import datetime


class ControllerTestCase(TestCase):

    database_uri = "sqlite:///test_controller.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    
    
    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.all_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

     
    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.all_data)
        self.db = models.init_app(self.app)


    def test_getAllOrganizations(self):
        allOrgs = controllers.getAllOrganizations(self.db)
        aikonIsValid = False
        uOfMIsValid = False
        
        for org in allOrgs:
            if(org.entityFK == 1):
                self.assertEquals(org.name, 'Ai-Kon')
                self.assertEquals(org.description, 'Ai-Kon Anime Convention')
                self.assertEquals(org.entity.type, models.TYPE_ORGANIZATION)
                self.assertEquals(org.entity.addresses[0].address1, '123 Vroom Street')
                self.assertEquals(org.entity.addresses[0].address2, None)
                self.assertEquals(org.entity.addresses[0].address3, None)
                self.assertEquals(org.entity.addresses[0].city, 'Winnipeg')
                self.assertEquals(org.entity.addresses[0].province, 'Manitoba')
                self.assertEquals(org.entity.addresses[0].country, 'Canada')
                self.assertEquals(org.entity.addresses[0].postalcode, 'A1A1A1')
                self.assertEquals(org.entity.addresses[0].isprimary, True)
                self.assertEquals(org.entity.contacts[0].type, models.TYPE_EMAIL)
                self.assertEquals(org.entity.contacts[0].value, 'info@ai-kon.org')
                self.assertEquals(org.entity.contacts[0].isprimary, True)
                aikonIsValid = True
            elif(org.entityFK == 2):
                self.assertEquals(org.name, 'University of Manitoba')
                self.assertEquals(org.description, 'The University of Manitoba, is a public university in the province of Manitoba, Canada. Located in Winnipeg, it is Manitoba\'s largest, most comprehensive, and only research-intensive post-secondary educational institution.')
                self.assertEquals(org.entity.type, models.TYPE_ORGANIZATION)
                self.assertEquals(org.entity.addresses[0].address1, '66 Chancellors Circle')
                self.assertEquals(org.entity.addresses[0].address2, None)
                self.assertEquals(org.entity.addresses[0].address3, None)
                self.assertEquals(org.entity.addresses[0].city, 'Winnipeg')
                self.assertEquals(org.entity.addresses[0].province, 'Manitoba')
                self.assertEquals(org.entity.addresses[0].country, 'Canada')
                self.assertEquals(org.entity.addresses[0].postalcode, 'R3T2N2')
                self.assertEquals(org.entity.addresses[0].isprimary, True)
                self.assertEquals(org.entity.contacts[0].type, models.TYPE_PHONE)
                self.assertEquals(org.entity.contacts[0].value, '18004321960')
                self.assertEquals(org.entity.contacts[0].isprimary, True)
                uOfMIsValid = True

        self.assertEquals(aikonIsValid, True)
        self.assertEquals(uOfMIsValid, True)


    def test_getAllOrganizationsJSON(self):
        ''' Get the JSON version of all organizations. '''
        jsonified = controllers.getAllOrganizationsJSON(self.db)

        data = json.loads(jsonified)
        for root,orgs in data.iteritems():
            self.assertEquals(root, 'Organizations')

            orgList = list()
            for org in orgs:
                newOrg = controllers.extractOrganizationFromDict(org)
                orgList.append(newOrg)

            allOrgs = controllers.getAllOrganizations(self.db)
            for first,second in zip(allOrgs,orgList):
                self.assertEqual(first.entityFK, second.entityFK);
                self.assertEqual(first.name, second.name)
                self.assertEqual(first.description, second.description)
                self.assertEqual(first.entity.pk, second.entity.pk)
                self.assertEqual(first.entity.type, second.entity.type)
                for a1,a2 in zip(first.entity.addresses, second.entity.addresses):
                    self.assertEqual(a1.entityFK, a2.entityFK)
                    self.assertEqual(a1.address1, a2.address1)
                    self.assertEqual(a1.address2, a2.address2)
                    self.assertEqual(a1.address3, a2.address3)
                    self.assertEqual(a1.city, a2.city)
                    self.assertEqual(a1.province, a2.province)
                    self.assertEqual(a1.country, a2.country)
                    self.assertEqual(a1.postalcode, a2.postalcode)
                    self.assertEqual(a1.isprimary, a2.isprimary)
                for c1,c2 in zip(first.entity.contacts, second.entity.contacts):
                    self.assertEqual(c1.entityFK, c2.entityFK)
                    self.assertEqual(c1.type, c2.type)
                    self.assertEqual(c1.value, c2.value)
                    self.assertEqual(c1.isprimary, c2.isprimary)

    def test_getAllOrgNamesJSON(self):
        ''' Test that we are getting JSON object containing org names and IDs '''
        allOrgs = json.loads(controllers.getAllOrgNamesJSON(self.db))

        ''' First Org should be Ai-Kon with ID 1 '''
        self.assertEqual(allOrgs['OrgNames'][0]['org_name'], 'Ai-Kon')
        self.assertEqual(allOrgs['OrgNames'][0]['org_entityfk'], 1)

        ''' Second Org should be University of Manitoba with ID 2 '''
        self.assertEqual(allOrgs['OrgNames'][1]['org_name'], 'University of Manitoba')
        self.assertEqual(allOrgs['OrgNames'][1]['org_entityfk'], 2)

    def test_registerDuplicateOrganization(self):
        ''' Construct our new organization. '''
        testOrg = models.Organization()
        testOrg.name = 'Test Org'
        testOrg.description = 'A test organization'
        testOrg.entity = models.Entity()
        testOrg.entity.type = models.TYPE_ORGANIZATION

        corpAddr = models.Address()
        corpAddr.address1 = '123 Corporate Way'
        corpAddr.address2 = 'C/O Event Planning'
        corpAddr.address3 = 'PO Box 123'
        corpAddr.city = 'Vancouver'
        corpAddr.province = 'British Columbia'
        corpAddr.country = 'Canada'
        corpAddr.postalcode = '2C2C2C'
        corpAddr.isprimary = True
        testOrg.entity.addresses.append(corpAddr)

        subAddr = models.Address()
        subAddr.address1 = '15 Field Office blvd'
        subAddr.address2 = 'PO Box 15'
        subAddr.address3 = 'C/O People That Work'
        subAddr.city = 'Regina'
        subAddr.province = 'Saskatchewan'
        subAddr.country = 'Canada'
        subAddr.postalcode = '3S3S3S'
        subAddr.isprimary = False
        testOrg.entity.addresses.append(subAddr)

        corpContact = models.Contact()
        corpContact.type = models.TYPE_PHONE
        corpContact.value = '18001234567'
        corpContact.isprimary = True
        testOrg.entity.contacts.append(corpContact)

        corpContact2 = models.Contact()
        corpContact2.type = models.TYPE_EMAIL
        corpContact2.value = 'corpcomm@mycorp.bc.ca'
        corpContact2.isprimary = False
        testOrg.entity.contacts.append(corpContact2)

        subContact = models.Contact()
        subContact.type = models.TYPE_EMAIL
        subContact.value = 'regional@mycorp.bc.ca'
        subContact.isprimary = False
        testOrg.entity.contacts.append(subContact)


        ''' Register the organization. '''
        corpJSON = controllers.organizationToJSON(testOrg)
        resultDict = json.loads(corpJSON)
        result = controllers.registerOrganization(resultDict,self.db)

        ''' Validate the result response. '''
        resultDict = json.loads(result)
        foundResult = False
        for key,value in resultDict.iteritems():
            if(key == 'result'):
                foundResult = True
                self.assertEqual('True', value)
        self.assertEqual(foundResult, True)

        ''' Register the organization a second time. '''
        resultDict = json.loads(corpJSON)
        result = controllers.registerOrganization(resultDict,self.db)

        ''' Validate the result response. '''
        resultDict = json.loads(result)
        foundResult = False
        for key,value in resultDict.iteritems():
            if(key == 'result'):
                foundResult = True
                self.assertEqual('duplicate', value)
        self.assertEqual(foundResult, True)
        self.resetDB()

    
    def test_registerOrganization(self):
        ''' Construct our new organization. '''
        testOrg = models.Organization()
        testOrg.name = 'Test Org'
        testOrg.description = 'A test organization'
        testOrg.entity = models.Entity()
        testOrg.entity.type = models.TYPE_ORGANIZATION

        corpAddr = models.Address()
        corpAddr.address1 = '123 Corporate Way'
        corpAddr.address2 = 'C/O Event Planning'
        corpAddr.address3 = 'PO Box 123'
        corpAddr.city = 'Vancouver'
        corpAddr.province = 'British Columbia'
        corpAddr.country = 'Canada'
        corpAddr.postalcode = '2C2C2C'
        corpAddr.isprimary = True
        testOrg.entity.addresses.append(corpAddr)

        subAddr = models.Address()
        subAddr.address1 = '15 Field Office blvd'
        subAddr.address2 = 'PO Box 15'
        subAddr.address3 = 'C/O People That Work'
        subAddr.city = 'Regina'
        subAddr.province = 'Saskatchewan'
        subAddr.country = 'Canada'
        subAddr.postalcode = '3S3S3S'
        subAddr.isprimary = False
        testOrg.entity.addresses.append(subAddr)

        corpContact = models.Contact()
        corpContact.type = models.TYPE_PHONE
        corpContact.value = '18001234567'
        corpContact.isprimary = True
        testOrg.entity.contacts.append(corpContact)

        corpContact2 = models.Contact()
        corpContact2.type = models.TYPE_EMAIL
        corpContact2.value = 'corpcomm@mycorp.bc.ca'
        corpContact2.isprimary = False
        testOrg.entity.contacts.append(corpContact2)

        subContact = models.Contact()
        subContact.type = models.TYPE_EMAIL
        subContact.value = 'regional@mycorp.bc.ca'
        subContact.isprimary = False
        testOrg.entity.contacts.append(subContact)


        ''' Register the organization. '''
        corpJSON = controllers.organizationToJSON(testOrg)
        resultDict = json.loads(corpJSON)
        result = controllers.registerOrganization(resultDict,self.db)

        ''' Validate the result response. '''
        resultDict = json.loads(result)
        foundResult = False
        for key,value in resultDict.iteritems():
            if(key == 'result'):
                foundResult = True
                self.assertEqual('True', value)
        self.assertEqual(foundResult, True)

        ''' Find the organization and compare to our structure. '''
        savedOrg = models.Organization.query.filter_by(name = testOrg.name).first()
        self.assertNotEqual(savedOrg,None)
        self.assertEqual(savedOrg.name, testOrg.name)
        self.assertEqual(savedOrg.description, testOrg.description)
        self.assertEqual(savedOrg.entity.type, testOrg.entity.type)

        for a1,a2 in zip(savedOrg.entity.addresses, testOrg.entity.addresses):
            self.assertEqual(a1.address1, a2.address1)
            self.assertEqual(a1.address2, a2.address2)
            self.assertEqual(a1.address3, a2.address3)
            self.assertEqual(a1.city, a2.city)
            self.assertEqual(a1.province, a2.province)
            self.assertEqual(a1.country, a2.country)
            self.assertEqual(a1.postalcode, a2.postalcode)
            self.assertEqual(a1.isprimary, a2.isprimary)

        for c1,c2 in zip(savedOrg.entity.contacts, testOrg.entity.contacts):
            self.assertEqual(c1.type, c2.type)
            self.assertEqual(c1.value, c2.value)
            self.assertEqual(c1.isprimary, c2.isprimary)
        self.resetDB()
        

    def test_organizationToJSON(self):
        target = models.Organization.query.first()
        targetJSON = controllers.organizationToJSON(target)
        stringJSON = '{"org_entityfk":1,"org_name":"Ai-Kon","org_desc":"Ai-Kon Anime Convention","Entity":{"entity_pk":1,"entity_type":"1","addresses":[{"addr_entityfk":1,"address1":"123 Vroom Street","address2":"None","address3":"None","city":"Winnipeg","province":"Manitoba","country":"Canada","postalcode":"A1A1A1","isprimary":"True"}], "contacts":[{"contact_entityfk":1,"type":"2","value":"info@ai-kon.org","isprimary":"True"}]}}'
        self.assertEqual(targetJSON, stringJSON)

    def test_entityToJSON(self):
        target = models.Entity.query.first()
        targetJSON = controllers.entityToJSON(target)
        stringJSON = '{"entity_pk":1,"entity_type":"1","addresses":[{"addr_entityfk":1,"address1":"123 Vroom Street","address2":"None","address3":"None","city":"Winnipeg","province":"Manitoba","country":"Canada","postalcode":"A1A1A1","isprimary":"True"}], "contacts":[{"contact_entityfk":1,"type":"2","value":"info@ai-kon.org","isprimary":"True"}]}'
        self.assertEqual(targetJSON, stringJSON)

    def test_addressToJSON(self):
        target = models.Address.query.first()
        targetJSON = controllers.addressToJSON(target)
        stringJSON = '{"addr_entityfk":1,"address1":"123 Vroom Street","address2":"None","address3":"None","city":"Winnipeg","province":"Manitoba","country":"Canada","postalcode":"A1A1A1","isprimary":"True"}'
        self.assertEqual(targetJSON, stringJSON)

    def test_contactToJSON(self):
        target = models.Contact.query.first()
        targetJSON = controllers.contactToJSON(target)
        stringJSON = '{"contact_entityfk":1,"type":"2","value":"info@ai-kon.org","isprimary":"True"}'
        self.assertEqual(targetJSON, stringJSON)

    def test_extractOrganizationFromDict(self):
        control = models.Organization.query.first()
        stringJSON = '{"org_entityfk":1,"org_name":"Ai-Kon","org_desc":"Ai-Kon Anime Convention","Entity":{"entity_pk":1,"entity_type":"1","addresses":[{"addr_entityfk":1,"address1":"123 Vroom Street","address2":"None","address3":"None","city":"Winnipeg","province":"Manitoba","country":"Canada","postalcode":"A1A1A1","isprimary":"True"}], "contacts":[{"contact_entityfk":1,"type":"2","value":"info@ai-kon.org","isprimary":"True"}]}}'
        data = json.loads(stringJSON)
        target = controllers.extractOrganizationFromDict(data)

        self.assertEqual(control.entityFK, target.entityFK);
        self.assertEqual(control.name, target.name)
        self.assertEqual(control.description, target.description)
        self.assertEqual(control.entity.pk, target.entity.pk)
        self.assertEqual(control.entity.type, target.entity.type)
        for a1,a2 in zip(control.entity.addresses, target.entity.addresses):
            self.assertEqual(a1.entityFK, a2.entityFK)
            self.assertEqual(a1.address1, a2.address1)
            self.assertEqual(a1.address2, a2.address2)
            self.assertEqual(a1.address3, a2.address3)
            self.assertEqual(a1.city, a2.city)
            self.assertEqual(a1.province, a2.province)
            self.assertEqual(a1.country, a2.country)
            self.assertEqual(a1.postalcode, a2.postalcode)
            self.assertEqual(a1.isprimary, a2.isprimary)
        for c1,c2 in zip(control.entity.contacts, target.entity.contacts):
            self.assertEqual(c1.entityFK, c2.entityFK)
            self.assertEqual(c1.type, c2.type)
            self.assertEqual(c1.value, c2.value)
            self.assertEqual(c1.isprimary, c2.isprimary)

    def test_extractEntityFromDict(self):
        control = models.Entity.query.first()
        stringJSON = '{"entity_pk":1,"entity_type":"1","addresses":[{"addr_entityfk":1,"address1":"123 Vroom Street","address2":"None","address3":"None","city":"Winnipeg","province":"Manitoba","country":"Canada","postalcode":"A1A1A1","isprimary":"True"}], "contacts":[{"contact_entityfk":1,"type":"2","value":"info@ai-kon.org","isprimary":"True"}]}'
        data = json.loads(stringJSON)
        target = controllers.extractEntityFromDict(data)

        self.assertEqual(control.pk, target.pk)
        self.assertEqual(control.type, target.type)
        for a1,a2 in zip(control.addresses, target.addresses):
            self.assertEqual(a1.entityFK, a2.entityFK)
            self.assertEqual(a1.address1, a2.address1)
            self.assertEqual(a1.address2, a2.address2)
            self.assertEqual(a1.address3, a2.address3)
            self.assertEqual(a1.city, a2.city)
            self.assertEqual(a1.province, a2.province)
            self.assertEqual(a1.country, a2.country)
            self.assertEqual(a1.postalcode, a2.postalcode)
            self.assertEqual(a1.isprimary, a2.isprimary)
        for c1,c2 in zip(control.contacts, target.contacts):
            self.assertEqual(c1.entityFK, c2.entityFK)
            self.assertEqual(c1.type, c2.type)
            self.assertEqual(c1.value, c2.value)
            self.assertEqual(c1.isprimary, c2.isprimary)

    def test_extractAddressFromDict(self):
        control = models.Address.query.first()
        stringJSON = '{"addr_entityfk":1,"address1":"123 Vroom Street","address2":"None","address3":"None","city":"Winnipeg","province":"Manitoba","country":"Canada","postalcode":"A1A1A1","isprimary":"True"}'
        data = json.loads(stringJSON)
        target = controllers.extractAddressFromDict(data)

        self.assertEqual(control.entityFK, target.entityFK)
        self.assertEqual(control.address1, target.address1)
        self.assertEqual(control.address2, target.address2)
        self.assertEqual(control.address3, target.address3)
        self.assertEqual(control.city, target.city)
        self.assertEqual(control.province, target.province)
        self.assertEqual(control.country, target.country)
        self.assertEqual(control.postalcode, target.postalcode)
        self.assertEqual(control.isprimary, target.isprimary)

    def test_extractContactFromDict(self):
        control = models.Contact.query.first()
        stringJSON = '{"contact_entityfk":1,"type":"2","value":"info@ai-kon.org","isprimary":"True"}'
        data = json.loads(stringJSON)
        target = controllers.extractContactFromDict(data)
        
        self.assertEqual(control.entityFK, target.entityFK)
        self.assertEqual(control.type, target.type)
        self.assertEqual(control.value, target.value)
        self.assertEqual(control.isprimary, target.isprimary)

    def test__checkForDuplicateOrganization(self):
        # Define an organization.
        testOrg = models.Organization()
        testOrg.name = 'test__checkForDuplicateOrganization'
        testOrg.description = 'test org description'
        testOrg.entity = models.Entity()
        testOrg.entity.type = models.TYPE_ORGANIZATION

        # Check for duplicates (should be no duplicates).
        isDuplicate = controllers._checkForDuplicateOrganization(testOrg)
        self.assertFalse(isDuplicate)

        # Insert the organization (should succeed).
        testOrgJSON = controllers.organizationToJSON(testOrg)
        resultDict = json.loads(testOrgJSON)
        result1 = controllers.registerOrganization(resultDict, self.db)
        resultDict = json.loads(result1)
        self.assertEqual(resultDict['result'], 'True')

        # Check for duplicates (should be duplicate).
        isDuplicate = controllers._checkForDuplicateOrganization(testOrg)
        self.assertTrue(isDuplicate)

    def test_checkForDuplicateOrganizationName(self):
        orgName = 'test_checkForDuplicateOrganization'
        orgDesc = 'test org description'
        
        # Define our input JSON string.
        orgNameJSON = '{';
        orgNameJSON += '"{key}":"{val}"'.format(key='org_name', val=orgName)
        orgNameJSON += '}'

        # Define an organization.
        testOrg = models.Organization()
        testOrg.name = orgName
        testOrg.description = orgDesc
        testOrg.entity = models.Entity()
        testOrg.entity.type = models.TYPE_ORGANIZATION
        testOrgJSON = controllers.organizationToJSON(testOrg)

        # Check for duplicates (should be no duplicates).
        resultDict = json.loads(orgNameJSON)
        result1 = controllers.checkForDuplicateOrganizationName(resultDict)
        resultDict = json.loads(result1)
        self.assertEqual(resultDict['result'], 'False')

        # Insert the organization (should succeed).
        resultDict = json.loads(testOrgJSON)
        result1 = controllers.registerOrganization(resultDict, self.db)
        resultDict = json.loads(result1)
        self.assertEqual(resultDict['result'], 'True')

        # Check for duplicates (should be duplicate).
        resultDict = json.loads(orgNameJSON)
        result1 = controllers.checkForDuplicateOrganizationName(resultDict)
        resultDict = json.loads(result1)
        self.assertEqual(resultDict['result'], 'True')


    """ Tests for Permissions feature """
    
    def test__getPrivilegesForPerson(self):
        # Define prerequisite data.
        personKey = 3
        organizationKey = 1
        # Get the result of the tested method.
        privileges = controllers._getPrivilegesForPerson(personKey, organizationKey)
        # Validate the result.
        self.assertIsNotNone(privileges)
        count = 0
        for priv in privileges:
            count += 1
            self.assertTrue(priv.pk is 5 or priv.pk is 6)
            self.assertTrue(priv.privilege == 'VIEW_ALL_EMPLOYEES_IN_ORG' or
                            priv.privilege == 'ASSIGN_EMPS_TO_SHIFTS')
        self.assertEqual(count, 2)

    def test__getOrgsWithPrivilegesForPerson(self):
        # Define prerequisite data.
        personKey = 4
        # Get the result of the tested method.
        orgKeys = controllers._getOrgsWithPrivilegesForPerson(personKey=personKey)
        # Validate the result.
        self.assertIsNotNone(orgKeys)
        count = 0
        for value in orgKeys:
            count += 1
            self.assertTrue(value == 1 or value == 2)
        self.assertEqual(count, 2)

    def test__getGlobalPrivilegesForPerson(self):
        # Define prerequisite data.
        personKey = 3
        # Get the result of the tested method.
        privileges = controllers._getGlobalPrivilegesForPerson(personKey)
        # Validate the result.
        self.assertIsNotNone(privileges)
        count = 0
        for priv in privileges:
            count += 1
            self.assertTrue(priv.pk is 1 or priv.pk is 4)
            self.assertTrue(priv.privilege == 'REGISTER_NEW_ORGANIZATION' or
                            priv.privilege == 'VIEW_ALL_ORGANIZATIONS')
        self.assertEqual(count, 2)

    def test__getOrgsWithPersonPrivilege(self):
        # Define prerequisite data.
        personKey = 4
        privilegeKey = 7
        # Get the restult of the tested method.
        orgKeys = controllers._getOrgsWithPersonPrivilege(personKey=personKey,privilegeKey=privilegeKey)
        # Validate the result.
        self.assertIsNotNone(orgKeys)
        count = 0
        for value in orgKeys:
            count += 1
            self.assertTrue(value == 1 or value == 2)
        self.assertEqual(count, 2)

    def test__getPeopleInOrganization(self):
        # Define prerequisite data.
        organizationKey = 1
        # Get the restult of the tested method.
        personKeys = controllers._getPeopleInOrganization(organizationKey=organizationKey)
        # Validate the result.
        self.assertIsNotNone(personKeys)
        count = 0
        for value in personKeys:
            count += 1
            self.assertTrue(value == 3 or value == 4)
        self.assertEqual(count, 2)

    def test__grantPrivilegeToPerson_Global(self):
        self.resetDB()

        # Sub-Test 1: Invalid person key.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 9999
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 2: Invalid privilege key.
        # Define prerequisite data.
        privilegeKey = 9999
        personKey = 5
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 3: Valid execution.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 5
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 4: Duplicate permission.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 5
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertTrue(result)

    def test__grantPrivilegeToPerson_Person(self):
        self.resetDB()

        # Sub-Test 1: Invalid person key.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 9999
        organizationKey = 1
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 2: Invalid privilege key.
        # Define prerequisite data.
        privilegeKey = 9999
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 3: Invalid organization key.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 4
        organizationKey = 9999
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 4: Valid execution.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 5: Duplicate permission.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 6: Duplicate permission, but different organization.
        # Define prerequisite data.
        privilegeKey = 1
        personKey = 4
        organizationKey = 2
        # Get the result of the tested method.
        result = controllers._grantPrivilegeToPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

    def test__revokePrivilegeForPerson_Global(self):
        # Sub-Test 1: Invalid person key.
        # Define prerequisite data.
        privilegeKey = 4
        personKey = 9999
        # Get the result of the tested method.
        result = controllers._revokePrivilegeForPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 2: Invalid privilege key.
        # Define prerequisite data.
        privilegeKey = 9999
        personKey = 4
        # Get the result of the tested method.
        result = controllers._revokePrivilegeForPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 3: Valid execution.
        # Define prerequisite data.
        privilegeKey = 4
        personKey = 4
        # Get the result of the tested method.
        result = controllers._revokePrivilegeForPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 4: Duplicate permission.
        # Define prerequisite data.
        privilegeKey = 4
        personKey = 4
        # Get the result of the tested method.
        result = controllers._revokePrivilegeForPerson(self.db, privilegeKey, personKey, None)
        # Validate the result.
        self.assertTrue(result)

        self.resetDB()

    def test__revokePrivilegeForPerson_Person(self):
        # Sub-Test 1: Invalid person key.
        # Define prerequisite data.
        privilegeKey = 7
        personKey = 9999
        organizationKey = 1
        # Get the result of the tested method.
        result = controllers._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 2: Invalid privilege key.
        # Define prerequisite data.
        privilegeKey = 9999
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controllers._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 3: Invalid organization key.
        # Define prerequisite data.
        privilegeKey = 7
        personKey = 4
        organizationKey = 9999
        # Get the result of the tested method.
        result = controllers._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 4: Valid execution.
        # Define prerequisite data.
        privilegeKey = 7
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controllers._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 5: Duplicate permission.
        # Define prerequisite data.
        privilegeKey = 7
        personKey = 4
        organizationKey = 1
        # Get the result of the tested method.
        result = controllers._revokePrivilegeForPerson(self.db, privilegeKey, personKey, organizationKey)
        # Validate the result.
        self.assertTrue(result)

        self.resetDB()
        
    ########################################        
    # Tests For Employee_Registration_Form #
    ########################################

    # Test functionality of the check for duplicate employee function 
    def test__checkForDuplicateEmployee(self):
        # Define an Person Class
        testEmp = models.Person()
        testEmp.username = 'betcha'
        testEmp.password = '2345'
        testEmp.firstname = 'VedryPrivate'
        testEmp.lastname = 'BetchdakuKun'
        testEmp.entity = models.Entity()
        testEmp.entity.type = models.TYPE_EMPLOYEE
        # Check if there is a duplicate and it should return with false
        isDuplicate = controllers._checkForDuplicateEmployee(testEmp)
        self.assertFalse(isDuplicate)

        #Test employeeToJSON
        testEmpJSON = controllers.employeeToJSON(testEmp)
        resultDict = json.loads(testEmpJSON)
        result = controllers.registerEmployee(resultDict, self.db)
        resultDict = json.loads(result)
        self.assertEqual(resultDict['username'], testEmp.username)

        # Check if there is a duplicate username and should be there.
        isDuplicate = controllers._checkForDuplicateEmployee(testEmp)
        self.assertTrue(isDuplicate)
        
    # Test functionality of the regiser employee function 
    def test_registerEmployee(self):
        # Make emp empty to test if it gets successfully assiged as Person object
        emp = None
        # emp should be empty 
        self.assertIsNone(emp);
        emp = models.Person()
        # Check if emp is not empty
        self.assertIsNotNone(emp)
        # Assign values to this person object
        emp.username = 'umbet'
        emp.password = '123456'
        emp.firstname = 'Elyse'
        emp.lastname = 'Goodall'
        emp.entity = models.Entity()
        emp.entity.type = models.TYPE_EMPLOYEE
        # addr should be empty to begin with
        addr = None
        self.assertIsNone(addr);
        #Create address instance
        addr = models.Address()
        # Check if addr is not empty
        self.assertIsNotNone(addr)
        # Assign values to addr object
        addr.address1 = '242 Lipton'
        addr.address2 = ''
        addr.address3 = ''
        addr.city = 'WPG'
        addr.province = 'MB'
        addr.country = 'Canada'
        addr.postalcode = 'R3M2X6'
        addr.isprimary = True
        # Attach the address instance to the employee
        emp.entity.addresses.append(addr)
        # Create a contact instance for phone
        contactP = None
        self.assertIsNone(contactP)
        contactP = models.Contact()
        self.assertIsNotNone(contactP)
        contactP.type = models.TYPE_PHONE
        contactP.value = '18001234567'
        contactP.isprimary = False
        emp.entity.contacts.append(contactP)
        # Create a contact instanace for Email
        contactE = None
        self.assertIsNone(contactE)
        contactE = models.Contact()
        self.assertIsNotNone(contactE)
        contactE.type = models.TYPE_EMAIL
        contactE.value = 'elyse@dmt.ca'
        contactE.isprimary = False
        emp.entity.contacts.append(contactE)

        # emp should not be None
        self.assertIsNotNone(emp)
        
        # Register the employee
        empJSON = controllers.employeeToJSON(emp)
        self.assertIsNotNone(empJSON)
        resultDict = json.loads(empJSON)
        result = controllers.registerEmployee(resultDict, self.db)
        # Check if everything successfully gets registered
        check = json.loads(result)
        found = False
        for key,value in check.iteritems():
            if(key == 'result'):
                found = True
                self.assertEqual('True', value)
        
        emp2 = models.Person.query.filter_by(username = emp.username).first()
        # Get the FK
        emp.entityFK = emp2.entityFK
        # Make sure that emp2 should not be null
        self.assertNotEqual(emp2, None)
        # emp and emp2 SHOULD NOT BE THE SAME OBJECT
        self.assertIsNot(emp, emp2)
        
        # emp2 should be Person class since we created from emp
        self.assertIsInstance(emp, type(emp2), msg="emp and emp2 are not the same Person class")
        self.assertNotIsInstance(emp2, type('Person'), msg="emp2 is not Person class")
        
        # These values should be equal if everything correctly saved
        self.assertEqual(emp2.firstname, 'Elyse')
        self.assertEqual(emp2.lastname, 'Goodall')
        self.assertEqual(emp2.password, '123456')
        # Check the address (emp and emp2 addresses should be equal)
        for a1,a2 in zip(emp2.entity.addresses, emp.entity.addresses):
            self.assertEqual(a1.address1, a2.address1)
            self.assertEqual(a1.address2, a2.address2)
            self.assertEqual(a1.address3, a2.address3)
            self.assertEqual(a1.city, a2.city)
            self.assertEqual(a1.province, a2.province)
            self.assertEqual(a1.country, a2.country)
            self.assertEqual(a1.postalcode, a2.postalcode)
            self.assertEqual(a1.isprimary, a2.isprimary)
        # Check the contacts (emp2 and emp contacts should be equal)
        for c1,c2 in zip(emp2.entity.contacts, emp.entity.contacts):
            self.assertEqual(c1.type, c2.type)
            self.assertEqual(c1.value, c2.value)
            self.assertEqual(c1.isprimary, c2.isprimary)
        self.resetDB()

    # Test functionality of the get person by id 
    def test_getPersonById(self):
        person = controllers.getPersonById(0, self.db)
        self.assertIsNone(person)

        person = controllers.getPersonById(1, self.db)
        self.assertIsNone(person)

        person = controllers.getPersonById(2, self.db)
        self.assertIsNone(person)

        person = controllers.getPersonById(3, self.db)
        self.assertIsNotNone(person)
        self.assertEqual(person.firstname, 'Chris')
        self.assertEqual(person.lastname, 'Workman')
        self.assertEqual(person.username, 'user0')
        self.assertEqual(person.password, 'password0')

        person = controllers.getPersonById(4, self.db)
        self.assertIsNotNone(person)
        self.assertEqual(person.firstname, 'Ryoji')
        self.assertEqual(person.lastname, 'Betchaku')
        self.assertEqual(person.username, 'user1')
        self.assertEqual(person.password, 'password1')

        person = controllers.getPersonById(5, self.db)
        self.assertIsNotNone(person)
        self.assertEqual(person.firstname, 'Dan')
        self.assertEqual(person.lastname, 'Nelson')
        self.assertEqual(person.username, 'meat_lol')
        self.assertEqual(person.password, 'password2')

        person = controllers.getPersonById(6, self.db)
        self.assertIsNone(person)

        self.resetDB

    # Test functionality of the get person by username
    def test_getPersonByUsername(self):
        person = controllers.getPersonByUsername('', self.db)
        self.assertIsNone(person)

        person = controllers.getPersonById(0, self.db)
        self.assertIsNone(person)

        person = controllers.getPersonById(3, self.db)
        self.assertIsNotNone(person)

        result = controllers.getPersonByUsername(person.username, self.db)
        self.assertIsNotNone(result)
        self.assertEqual(result.firstname, person.firstname)
        self.assertEqual(result.lastname, person.lastname)
        self.assertEqual(result.username, person.username)
        self.assertEqual(result.password, person.password)

        person = controllers.getPersonById(4, self.db)
        self.assertIsNotNone(person)

        result = controllers.getPersonByUsername(person.username, self.db)
        self.assertIsNotNone(result)
        self.assertEqual(result.firstname, person.firstname)
        self.assertEqual(result.lastname, person.lastname)
        self.assertEqual(result.username, person.username)
        self.assertEqual(result.password, person.password)

        person = controllers.getPersonById(5, self.db)
        self.assertIsNotNone(person)

        result = controllers.getPersonByUsername(person.username, self.db)
        self.assertIsNotNone(result)
        self.assertEqual(result.firstname, person.firstname)
        self.assertEqual(result.lastname, person.lastname)
        self.assertEqual(result.username, person.username)
        self.assertEqual(result.password, person.password)

        self.resetDB
        
    def test__getOrganizationByID(self):
        org = controllers._getOrganizationByID(1)
        self.assertIsNotNone(org)
        self.assertEqual(org.entityFK, 1)
        self.assertEquals(org.name, 'Ai-Kon')
        self.assertEquals(org.description, 'Ai-Kon Anime Convention')
        self.assertEquals(org.entity.type, models.TYPE_ORGANIZATION)
        self.assertEquals(org.entity.addresses[0].address1, '123 Vroom Street')
        self.assertEquals(org.entity.addresses[0].address2, None)
        self.assertEquals(org.entity.addresses[0].address3, None)
        self.assertEquals(org.entity.addresses[0].city, 'Winnipeg')
        self.assertEquals(org.entity.addresses[0].province, 'Manitoba')
        self.assertEquals(org.entity.addresses[0].country, 'Canada')
        self.assertEquals(org.entity.addresses[0].postalcode, 'A1A1A1')
        self.assertEquals(org.entity.addresses[0].isprimary, True)
        self.assertEquals(org.entity.contacts[0].type, models.TYPE_EMAIL)
        self.assertEquals(org.entity.contacts[0].value, 'info@ai-kon.org')
        self.assertEquals(org.entity.contacts[0].isprimary, True)

    def test_getOrganizationByIDJSON(self):
        ''' Test getOrganizationByID method '''
        ''' Validate first organization entries '''
        jsonify = json.loads(controllers.getOrganizationByIDJSON(1))
        org = controllers.extractOrganizationFromDict(jsonify)
        self.assertIsNotNone(org)
        self.assertEqual(org.entityFK, 1)
        self.assertEquals(org.name, 'Ai-Kon')
        self.assertEquals(org.description, 'Ai-Kon Anime Convention')
        self.assertEquals(org.entity.type, models.TYPE_ORGANIZATION)
        self.assertEquals(org.entity.addresses[0].address1, '123 Vroom Street')
        self.assertEquals(org.entity.addresses[0].address2, None)
        self.assertEquals(org.entity.addresses[0].address3, None)
        self.assertEquals(org.entity.addresses[0].city, 'Winnipeg')
        self.assertEquals(org.entity.addresses[0].province, 'Manitoba')
        self.assertEquals(org.entity.addresses[0].country, 'Canada')
        self.assertEquals(org.entity.addresses[0].postalcode, 'A1A1A1')
        self.assertEquals(org.entity.addresses[0].isprimary, True)
        self.assertEquals(org.entity.contacts[0].type, models.TYPE_EMAIL)
        self.assertEquals(org.entity.contacts[0].value, 'info@ai-kon.org')
        self.assertEquals(org.entity.contacts[0].isprimary, True)

        ''' Validate second organization entries '''
        jsonify = json.loads(controllers.getOrganizationByIDJSON(2))
        org = controllers.extractOrganizationFromDict(jsonify)
        self.assertIsNotNone(org)
        self.assertEquals(org.entityFK, 2) 
        self.assertEquals(org.name, 'University of Manitoba')
        self.assertEquals(org.description, 'The University of Manitoba, is a public university in the province of Manitoba, Canada. Located in Winnipeg, it is Manitoba\'s largest, most comprehensive, and only research-intensive post-secondary educational institution.')
        self.assertEquals(org.entity.type, models.TYPE_ORGANIZATION)
        self.assertEquals(org.entity.addresses[0].address1, '66 Chancellors Circle')
        self.assertEquals(org.entity.addresses[0].address2, None)
        self.assertEquals(org.entity.addresses[0].address3, None)
        self.assertEquals(org.entity.addresses[0].city, 'Winnipeg')
        self.assertEquals(org.entity.addresses[0].province, 'Manitoba')
        self.assertEquals(org.entity.addresses[0].country, 'Canada')
        self.assertEquals(org.entity.addresses[0].postalcode, 'R3T2N2')
        self.assertEquals(org.entity.addresses[0].isprimary, True)
        self.assertEquals(org.entity.contacts[0].type, models.TYPE_PHONE)
        self.assertEquals(org.entity.contacts[0].value, '18004321960')
        self.assertEquals(org.entity.contacts[0].isprimary, True)

        ''' Attempt an invalid organization '''
        org = controllers.getOrganizationByIDJSON(3)
        self.assertIsNone(org)
        
        
    ##Joining a person to an organization##
    def test_putPersonInOrganization(self):
        self.resetDB()

        # Sub-Test 1: Invalid person key.
        # Define prerequisite data.
        personKey = 9999
        request = '{"org_id": 1}'
        # Get the result of the tested method.
        result = controllers.putPersonInOrganization(request, self.db, personKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 2: Invalid json.
        # Define prerequisite data.
        request = 'xxx'
        personKey = 4
        # Get the result of the tested method.
        result = controllers.putPersonInOrganization(request, self.db, personKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 3: Invalid organization key.
        # Define prerequisite data.
        personKey = 4
        request = {org_id: 9999}
        # Get the result of the tested method.
        result = controllers.putPersonInOrganization(request, self.db, personKey)
        # Validate the result.
        self.assertFalse(result)

        # Sub-Test 4: Valid execution.
        # Define prerequisite data.
        personKey = 4
        request = {org_id: 1}
        # Get the result of the tested method.
        result = controllers.putPersonInOrganization(request, self.db, personKey)
        # Validate the result.
        self.assertTrue(result)

        # Sub-Test 5: Duplicate member.
        # Define prerequisite data.
        # use same data as before
        # Get the result of the tested method.
        result = controllers.putPersonInOrganization(request, self.db, personKey)
        # Validate the result.
        self.assertTrue(result)

        self.resetDB()
        

    ''' Test functionality to get Event by ID in events.py '''
    def test_getEventById(self):
        event = events.getEventById(1, self.db)
        self.assertIsNotNone(event)
        self.assertEqual(event.name, 'My Event')
        self.assertEqual(event.description, 'This is my event')
        self.assertEqual(event.organizationFK, 1)

        event = events.getEventById(2, self.db)
        self.assertIsNotNone(event)
        self.assertEqual(event.name, 'Your Event')
        self.assertEqual(event.description, 'This is your event')
        self.assertEqual(event.organizationFK, 2)

        event = events.getEventById(3, self.db)
        self.assertIsNone(event)
        
    
    ''' Test method in events.py '''
    def test_extractEventFromDict(self):
        control = models.Event.query.first()
        stringJSON = '{"event_pk":1, "event_name":"My Event", "event_desc":"This is my event", "event_start":"2013-07-12 12:00:00", "event_end":"2013-07-14 16:00:00", "event_orgfk":1}'
        data = json.loads(stringJSON)
        target = events.extractEventFromDict(data)

        self.assertEqual(control.pk, target.pk)
        self.assertEqual(control.name, target.name)
        self.assertEqual(control.description, target.description)
        self.assertEqual(control.startdate, target.startdate)
        self.assertEqual(control.enddate, target.enddate)
        self.assertEqual(control.organizationFK, target.organizationFK)
    
    ''' Test method from events.py '''
    def test__isDuplicateEvent_true(self):
        event1 = models.Event.query.first()
        
        event2 = models.Event()
        event2.name = event1.name
        event2.startdate = event1.startdate
        event2.enddate = event1.enddate
        event2.organizationFK = event1.organizationFK
        
        result = events._isDuplicateEvent(event2, self.db)
        self.assertTrue(result)
        
        
    ''' Test method from events.py '''
    def test__isDuplicateEvent_false(self):
        event1 = models.Event.query.first()

        event2 = models.Event()
        event2.name = event1.name + 'differenttext'
        event2.startdate = event1.startdate
        event2.enddate = event1.enddate
        event2.organizationFK = event1.organizationFK

        result = events._isDuplicateEvent(event2, self.db)
        self.assertFalse(result)
        
    ''' Test method from events.py '''
    def test__insertEvent_true(self):
        event = models.Event()
        name = 'test__insertEvent_true event'
        desc = 'description of test__insertEvent_true event is indescribable'
        start = datetime.datetime(2013, 3, 20, 1, 0)
        end = datetime.datetime(2013, 3, 20, 2, 0)
        orgFK = 1
        
        event.name = name
        event.description = desc
        event.startdate = start
        event.enddate = end
        event.organizationFK = orgFK
        
        result = events._insertEvent(event, self.db)
        self.assertTrue(result > 0)
        
        newEvent = models.Event.query.filter_by(pk=result).first()
        self.assertEqual(newEvent.pk, result)
        self.assertEqual(newEvent.name, name)
        self.assertEqual(newEvent.description, desc)
        self.assertEqual(newEvent.startdate, start)
        self.assertEqual(newEvent.enddate, end)
        self.assertEqual(newEvent.organizationFK, orgFK)
        
        
    ''' Test method from events.py '''
    def test__insertEvent_duplicate(self):
        event = models.Event()
        name='My Event'
        desc='This is my event'
        start=datetime.datetime(2013, 7, 12, 12, 0)
        end=datetime.datetime(2013, 7, 14, 16, 0)
        orgFK=1

        event.name = name
        event.description = desc
        event.startdate = start
        event.enddate = end
        event.organizationFK = orgFK

        result = events._insertEvent(event, self.db)
        self.assertEqual(result, 'Duplicate')
        
    ''' Test method from events.py '''
    def test__insertEvent_badorg(self):
        event = models.Event()
        name='My Event'
        desc='This is my event'
        start=datetime.datetime(2013, 7, 12, 12, 0)
        end=datetime.datetime(2013, 7, 14, 16, 0)
        orgFK=0

        event.name = name
        event.description = desc
        event.startdate = start
        event.enddate = end
        event.organizationFK = orgFK

        result = events._insertEvent(event, self.db)
        self.assertEqual(result, 'BadOrg')
        
    ''' Test method from events.py '''    
    def test_insertEvent_true(self):
        name='test_insertEvent_true event'
        desc='description of test_insertEvent_true event is indescribable'
        start=datetime.datetime(2013, 7, 12, 12, 0)
        end=datetime.datetime(2013, 7, 14, 16, 0)
        orgFK=1
        
        eventJSON = '{' + '"{key}":"{val}",'.format(key=models.EVENT_NAME_KEY, val=name)
        eventJSON += '"{key}":"{val}",'.format(key=models.EVENT_DESC_KEY, val=desc)
        eventJSON += '"{key}":"{val}",'.format(key=models.EVENT_START_KEY, val=start)
        eventJSON += '"{key}":"{val}"'.format(key=models.EVENT_END_KEY, val=end)
        eventJSON += '}'
        eventDict = json.loads(eventJSON)
        
        result = events.insertEvent(orgFK, eventDict, self.db)
        self.assertIsNotNone(result)
        newKey = 0
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'result':
                self.assertEqual(value, 'True')
            if key == models.EVENT_PK_KEY:
                self.assertTrue(value > 0)
                newKey = value
        
        newEvent = models.Event.query.filter_by(pk=newKey).first()
        self.assertEqual(newEvent.pk, newKey)
        self.assertEqual(newEvent.name, name)
        self.assertEqual(newEvent.description, desc)
        self.assertEqual(newEvent.startdate, start)
        self.assertEqual(newEvent.enddate, end)
        self.assertEqual(newEvent.organizationFK, orgFK)
        
        
    ''' Test method from events.py '''    
    def test_insertEvent_duplicate(self):
        event1 = models.Event.query.first()
        name=event1.name
        desc=event1.description
        start=event1.startdate
        end=event1.enddate
        orgFK=event1.organizationFK
        
        event2 = models.Event()
        event2.name = name
        event2.description = desc
        event2.startdate = start
        event2.enddate = end
        eventJSON = events.eventToJSON(event2)
        eventDict = json.loads(eventJSON)
        
        result = events.insertEvent(orgFK, eventDict, self.db)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'result':
                self.assertEqual(value, 'Duplicate')
            elif key == 'event_pk':
                self.assertEqual(value, 'None')
        
    ''' Test method from events.py '''    
    def test_insertEvent_badorg(self):
        name='test_insertEvent_badorg event'
        desc='description of test_insertEvent_badorg event is indescribable'
        start=datetime.datetime(2013, 7, 12, 12, 0)
        end=datetime.datetime(2013, 7, 14, 16, 0)
        orgFK=99999
        
        eventJSON = '{' + '"{key}":"{val}",'.format(key=models.EVENT_NAME_KEY, val=name)
        eventJSON += '"{key}":"{val}",'.format(key=models.EVENT_DESC_KEY, val=desc)
        eventJSON += '"{key}":"{val}",'.format(key=models.EVENT_START_KEY, val=start)
        eventJSON += '"{key}":"{val}"'.format(key=models.EVENT_END_KEY, val=end)
        eventJSON += '}'
        eventDict = json.loads(eventJSON)
        
        result = events.insertEvent(orgFK, eventDict, self.db)
        resultDict = json.loads(result)
        for key,value in resultDict.iteritems():
            if key == 'result':
                self.assertEqual(value, 'BadOrg')
            elif key == 'event_pk':
                self.assertEqual(value, 'None')        
        



def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(ControllerTestCase('test_getAllOrganizations'))
    suite.addTest(ControllerTestCase('test_getAllOrganizationsJSON'))
    suite.addTest(ControllerTestCase('test_getAllOrgNamesJSON'))
    suite.addTest(ControllerTestCase('test_registerDuplicateOrganization'))
    suite.addTest(ControllerTestCase('test_registerOrganization'))
    suite.addTest(ControllerTestCase('test_organizationToJSON'))
    suite.addTest(ControllerTestCase('test_entityToJSON'))
    suite.addTest(ControllerTestCase('test_addressToJSON'))
    suite.addTest(ControllerTestCase('test_contactToJSON'))
    suite.addTest(ControllerTestCase('test_extractOrganizationFromDict'))
    suite.addTest(ControllerTestCase('test_extractEntityFromDict'))
    suite.addTest(ControllerTestCase('test_extractAddressFromDict'))
    suite.addTest(ControllerTestCase('test_extractContactFromDict'))
    suite.addTest(ControllerTestCase('test__checkForDuplicateOrganization'))
    suite.addTest(ControllerTestCase('test_checkForDuplicateOrganizationName'))
    suite.addTest(ControllerTestCase('test__getPrivilegesForPerson'))
    suite.addTest(ControllerTestCase('test__getOrgsWithPrivilegesForPerson'))
    suite.addTest(ControllerTestCase('test__getGlobalPrivilegesForPerson'))
    suite.addTest(ControllerTestCase('test__getOrgsWithPersonPrivilege'))
    suite.addTest(ControllerTestCase('test__getPeopleInOrganization'))
    suite.addTest(ControllerTestCase('test__grantPrivilegeToPerson_Global'))
    suite.addTest(ControllerTestCase('test__grantPrivilegeToPerson_Person'))
    suite.addTest(ControllerTestCase('test__revokePrivilegeForPerson_Global'))
    suite.addTest(ControllerTestCase('test__revokePrivilegeForPerson_Person'))
    suite.addTest(ControllerTestCase('test__checkForDuplicateEmployee'))
    suite.addTest(ControllerTestCase('test_registerEmployee'))
    suite.addTest(ControllerTestCase('test_getPersonById'))
    suite.addTest(ControllerTestCase('test_getPersonByUsername'))
    suite.addTest(ControllerTestCase('test__getOrganizationByID'))
    suite.addTest(ControllerTestCase('test_getOrganizationByIDJSON'))
    suite.addTest(ControllerTestCase('test_getEventById'))
    suite.addTest(ControllerTestCase('test_extractEventFromDict'))
    suite.addTest(ControllerTestCase('test__isDuplicateEvent_true'))
    suite.addTest(ControllerTestCase('test__isDuplicateEvent_false'))
    suite.addTest(ControllerTestCase('test__insertEvent_true'))
    suite.addTest(ControllerTestCase('test__insertEvent_duplicate'))
    suite.addTest(ControllerTestCase('test__insertEvent_badorg'))
    suite.addTest(ControllerTestCase('test_insertEvent_true'))
    suite.addTest(ControllerTestCase('test_insertEvent_duplicate'))
    suite.addTest(ControllerTestCase('test_insertEvent_badorg'))
    
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
