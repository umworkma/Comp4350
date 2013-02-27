#!../venv/bin/python
import unittest

from flask import Flask
from flask import *
from flask.ext.testing import TestCase

import fixtures
import models
import controllers


class ESATestCase(TestCase):

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
        result1Dict = json.loads(result1)
        self.assertEqual(result1Dict['result'], 'True')

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
        result1Dict = json.loads(result1)
        self.assertEqual(result1Dict['result'], 'False')

        # Insert the organization (should succeed).
        resultDict = json.loads(testOrgJSON)
        result1 = controllers.registerOrganization(resultDict, self.db)
        result1Dict = json.loads(result1)
        self.assertEqual(result1Dict['result'], 'True')

        # Check for duplicates (should be duplicate).
        resultDict = json.loads(orgNameJSON)
        result1 = controllers.checkForDuplicateOrganizationName(resultDict)
        result1Dict = json.loads(result1)
        self.assertEqual(result1Dict['result'], 'True')



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
        

if __name__ == "__main__":
    unittest.main()
