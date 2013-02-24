#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class ESATestCase(TestCase):

    database_uri = "sqlite:///test.db"
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
    
    
    def test_member_model(self):
        current = models.Member.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.personentityFK, 3)
        self.assertEqual(current.organizationentityFK, 1)

        current = models.Member.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.personentityFK, 4)
        self.assertEqual(current.organizationentityFK, 1)

        current = models.Member.query.filter_by(pk=3).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.personentityFK, 4)
        self.assertEqual(current.organizationentityFK, 2)

        current = models.Member.query.filter_by(pk=4).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.personentityFK, 5)
        self.assertEqual(current.organizationentityFK, 2)
    
    
    def test_privilegePersonAssignment_model(self):
        current = models.PrivilegePersonAssignment.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 5)
        self.assertEqual(current.memberFK, 1)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 6)
        self.assertEqual(current.memberFK, 1)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=3).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 7)
        self.assertEqual(current.memberFK, 2)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=4).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 8)
        self.assertEqual(current.memberFK, 3)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=5).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 5)
        self.assertEqual(current.memberFK, 4)

        current = models.PrivilegePersonAssignment.query.filter_by(pk=6).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 6)
        self.assertEqual(current.memberFK, 4)
    
    
    def test_globalPrivilegeAssignment_model(self):
        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=1).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 1)
        self.assertEqual(current.personentityFK, 3)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=2).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 4)
        self.assertEqual(current.personentityFK, 3)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=3).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 3)
        self.assertEqual(current.personentityFK, 4)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=4).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 4)
        self.assertEqual(current.personentityFK, 4)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=5).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 2)
        self.assertEqual(current.personentityFK, 5)

        current = models.GlobalPrivilegeAssignment.query.filter_by(pk=6).first()
        self.assertIsNotNone(current)
        self.assertEqual(current.privilegeFK, 4)
        self.assertEqual(current.personentityFK, 5)
    
            
    """ Test that entites are defined and the model represents them correctly. """
    def test_entity_model(self):
        for idx in range(1,3):
            org = models.Entity.query.filter_by(pk=idx).first()
            self.assertEqual(org.type, models.TYPE_ORGANIZATION)

        for idx in range(3,6):
            emp = models.Entity.query.filter_by(pk=idx).first()
            self.assertEqual(emp.type, models.TYPE_EMPLOYEE)


    """ Test that organizations are defined and the model represents them correctly. """
    def test_organization_model(self):
        aikon = models.Organization.query.filter_by(entityFK=1).first()
        self.assertEqual(aikon.entityFK, 1)
        self.assertEqual(aikon.name, 'Ai-Kon')
        self.assertEqual(aikon.description, 'Ai-Kon Anime Convention')

        uOfM = models.Organization.query.filter_by(entityFK=2).first()
        self.assertEqual(uOfM.entityFK, 2)
        self.assertEqual(uOfM.name, 'University of Manitoba')
        self.assertEqual(uOfM.description, 'The University of Manitoba, is a public university in the province of Manitoba, Canada. Located in Winnipeg, it is Manitoba\'s largest, most comprehensive, and only research-intensive post-secondary educational institution.')


    """ Test that person objects are defined and the model represents them correctly. """
    def test_person_model(self):
        chris = models.Person.query.filter_by(entityFK=3).first()
        self.assertEqual(chris.entityFK, 3)
        self.assertEqual(chris.firstname, 'Chris')
        self.assertEqual(chris.lastname, 'Workman')

        ryoji = models.Person.query.filter_by(entityFK=4).first()
        self.assertEqual(ryoji.entityFK, 4)
        self.assertEqual(ryoji.firstname, 'Ryoji')
        self.assertEqual(ryoji.lastname, 'Betchaku')

        dan = models.Person.query.filter_by(entityFK=5).first()
        self.assertEqual(dan.entityFK, 5)
        self.assertEqual(dan.firstname, 'Dan')
        self.assertEqual(dan.lastname, 'Nelson')

    
    """ Test that addresses are defined and the model represents them correctly. """
    def test_address_model(self):
        aikonPrimaryAddress = models.Address.query.filter_by(entityFK=1, isprimary=1).first()
        self.assertEqual(aikonPrimaryAddress.entityFK, 1)
        self.assertEqual(aikonPrimaryAddress.isprimary, 1)
        self.assertEqual(aikonPrimaryAddress.address1, '123 Vroom Street')
        self.assertEqual(aikonPrimaryAddress.city, 'Winnipeg')
        self.assertEqual(aikonPrimaryAddress.province, 'Manitoba')
        self.assertEqual(aikonPrimaryAddress.country, 'Canada')
        self.assertEqual(aikonPrimaryAddress.postalcode, 'A1A1A1')

        uOfMPrimaryAddress = models.Address.query.filter_by(entityFK=2, isprimary=1).first()
        self.assertEqual(uOfMPrimaryAddress.entityFK, 2)
        self.assertEqual(uOfMPrimaryAddress.isprimary, 1)
        self.assertEqual(uOfMPrimaryAddress.address1, '66 Chancellors Circle')
        self.assertEqual(uOfMPrimaryAddress.city, 'Winnipeg')
        self.assertEqual(uOfMPrimaryAddress.province, 'Manitoba')
        self.assertEqual(uOfMPrimaryAddress.country, 'Canada')
        self.assertEqual(uOfMPrimaryAddress.postalcode, 'R3T2N2')

        chrisPrimaryAddress = models.Address.query.filter_by(entityFK=3, isprimary=1).first()
        self.assertEqual(chrisPrimaryAddress.entityFK, 3)
        self.assertEqual(chrisPrimaryAddress.isprimary, 1)
        self.assertEqual(chrisPrimaryAddress.address1, '2116 - 991D Markham Rd')
        self.assertEqual(chrisPrimaryAddress.city, 'Winnipeg')
        self.assertEqual(chrisPrimaryAddress.province, 'Manitoba')
        self.assertEqual(chrisPrimaryAddress.country, 'Canada')
        self.assertEqual(chrisPrimaryAddress.postalcode, 'R3K 5J1')

        chrisNotPrimaryAddress = models.Address.query.filter_by(entityFK=3, isprimary=0).first()
        self.assertEqual(chrisNotPrimaryAddress.entityFK, 3)
        self.assertEqual(chrisNotPrimaryAddress.isprimary, 0)
        self.assertEqual(chrisNotPrimaryAddress.address1, '16 Premier Place')
        self.assertEqual(chrisNotPrimaryAddress.city, 'Winnipeg')
        self.assertEqual(chrisNotPrimaryAddress.province, 'Manitoba')
        self.assertEqual(chrisNotPrimaryAddress.country, 'Canada')
        self.assertEqual(chrisNotPrimaryAddress.postalcode, 'R2C 0S9')

        ryojiPrimaryAddress = models.Address.query.filter_by(entityFK=4, isprimary=1).first()
        self.assertEqual(ryojiPrimaryAddress.entityFK, 4)
        self.assertEqual(ryojiPrimaryAddress.isprimary, 1)
        self.assertEqual(ryojiPrimaryAddress.address1, '2194 Pembina Hwy')
        self.assertEqual(ryojiPrimaryAddress.city, 'Winnipeg')
        self.assertEqual(ryojiPrimaryAddress.province, 'Manitoba')
        self.assertEqual(ryojiPrimaryAddress.country, 'Canada')
        self.assertEqual(ryojiPrimaryAddress.postalcode, 'R1G 5V4')

        danPrimaryAddress = models.Address.query.filter_by(entityFK=5, isprimary=1).first()
        self.assertEqual(danPrimaryAddress.entityFK, 5)
        self.assertEqual(danPrimaryAddress.isprimary, 1)
        self.assertEqual(danPrimaryAddress.address1, '123 Main St')
        self.assertEqual(danPrimaryAddress.city, 'Selkirk')
        self.assertEqual(danPrimaryAddress.province, 'Manitoba')
        self.assertEqual(danPrimaryAddress.country, 'Canada')
        self.assertEqual(danPrimaryAddress.postalcode, '1V1 F2F')


    """ Test that contacts are defined and the model represents them properly. """
    def test_contact_model(self):
        aikonContactEmail1 = models.Contact.query.filter_by(entityFK = 1, type = 2, isprimary = 1).first()
        self.assertEqual(aikonContactEmail1.entityFK, 1)
        self.assertEqual(aikonContactEmail1.type, 2)
        self.assertEqual(aikonContactEmail1.value, 'info@ai-kon.org')
        self.assertEqual(aikonContactEmail1.isprimary, 1)

        uOfMContactPhone1 = models.Contact.query.filter_by(entityFK = 2, type = 1, isprimary = 1).first()
        self.assertEqual(uOfMContactPhone1.entityFK, 2)
        self.assertEqual(uOfMContactPhone1.type, 1)
        self.assertEqual(uOfMContactPhone1.value, '18004321960')
        self.assertEqual(uOfMContactPhone1.isprimary, 1)


    """ Test that an address can be retrieved from the entity relationship. """
    def test_entity_address_relationship(self):
        aikonAddressDirect = models.Address.query.filter_by(entityFK=1).first()
        self.assertEqual(aikonAddressDirect.address1, '123 Vroom Street')
        aikonEntity = models.Entity.query.filter_by(pk = 1).first()
        self.assertEqual(aikonEntity.type, models.TYPE_ORGANIZATION)
        aikonAddressByEntity = aikonEntity.addresses[0]
        self.assertEqual(aikonAddressByEntity.address1, '123 Vroom Street')
        self.assertEqual(aikonAddressByEntity, aikonAddressDirect)

        uOfMAddressDirect = models.Address.query.filter_by(entityFK=2).first()
        self.assertEqual(uOfMAddressDirect.address1, '66 Chancellors Circle')
        uOfMEntity = models.Entity.query.filter_by(pk = 2).first()
        self.assertEqual(uOfMEntity.type, models.TYPE_ORGANIZATION)
        uOfMAddressByEntity = uOfMEntity.addresses[0]
        self.assertEqual(uOfMAddressByEntity.address1, '66 Chancellors Circle')
        self.assertEqual(uOfMAddressByEntity, uOfMAddressDirect)

    
    """ Test that we can retrieve an entity from the organization relationship. """
    def test_organization_entity_relationship(self):
        aikonEntityDirect = models.Entity.query.filter_by(pk = 1).first()
        self.assertEqual(aikonEntityDirect.type, models.TYPE_ORGANIZATION)
        aikonOrg = models.Organization.query.filter_by(entityFK = 1).first()
        self.assertEqual(aikonOrg.name, 'Ai-Kon')
        aikonEntityByOrg = aikonOrg.entity
        self.assertEqual(aikonEntityByOrg.type, models.TYPE_ORGANIZATION)
        self.assertEqual(aikonEntityDirect, aikonEntityByOrg)

        uOfMEntityDirect = models.Entity.query.filter_by(pk = 2).first()
        self.assertEqual(uOfMEntityDirect.type, models.TYPE_ORGANIZATION)
        uOfMOrg = models.Organization.query.filter_by(entityFK = 2).first()
        self.assertEqual(uOfMOrg.name, 'University of Manitoba')
        uOfMEntityByOrg = uOfMOrg.entity
        self.assertEqual(uOfMEntityByOrg.type, models.TYPE_ORGANIZATION)
        self.assertEqual(uOfMEntityDirect, uOfMEntityByOrg)


    """ Test that we can retrieve an organzation from a member. """
    def test_member_organization_relationship(self):
        direct = models.Organization.query.filter_by(entityFK=1).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.name, 'Ai-Kon')
        host = models.Member.query.filter_by(pk=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.organizationentityFK, 1)
        target = host.organization
        self.assertIsNotNone(target)
        self.assertEqual(target.entityFK, direct.entityFK)
        self.assertEqual(target.name, direct.name)
    """ Test that we can retrieve members from an organization. """
    def test_organization_member_relationship(self):
        directList = models.Member.query.filter_by(organizationentityFK=1)
        self.assertIsNotNone(directList)

        host = models.Organization.query.filter_by(entityFK=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, 1)

        targetList = host.employees
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.personentityFK, ti.personentityFK)
            self.assertEqual(di.organizationentityFK, ti.organizationentityFK)
        self.assertGreater(resultCount, 0)


    """ Test that we can retrieve a person from a member. """
    def test_member_person_relationship(self):
        direct = models.Person.query.filter_by(entityFK=4).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.firstname, 'Ryoji')
        host = models.Member.query.filter_by(pk=3).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.personentityFK, 4)
        target = host.person
        self.assertIsNotNone(target)
        self.assertEqual(target.entityFK, direct.entityFK)
        self.assertEqual(target.firstname, direct.firstname)
        self.assertEqual(target.lastname, direct.lastname)
    """ Test that we can retrieve members from a person. """
    def test_person_member_relationship(self):
        directList = models.Member.query.filter_by(personentityFK=4)
        self.assertIsNotNone(directList)

        host = models.Person.query.filter_by(entityFK=4).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, 4)

        targetList = host.memberships
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.personentityFK, ti.personentityFK)
            self.assertEqual(di.organizationentityFK, ti.organizationentityFK)
        self.assertGreater(resultCount, 0)


    """ Test that we can retieve a permission from the person-assignment. """
    def test_privilegepersonassignment_privilege_relationship(self):
        direct = models.Privilege.query.filter_by(pk=5).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, 5)

        host = models.PrivilegePersonAssignment.query.filter_by(pk=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.privilegeFK, direct.pk)

        target = host.privilege
        self.assertIsNotNone(target)
        self.assertEqual(target.pk, direct.pk)
        self.assertEqual(target.privilege, direct.privilege)
    """ Test that we can retieve a person-assignments from a privilege. """
    def test_privilege_privilegepersonassignment_relationship(self):
        directList = models.PrivilegePersonAssignment.query.filter_by(privilegeFK=5)
        self.assertIsNotNone(directList)

        host = models.Privilege.query.filter_by(pk=5).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, 5)

        targetList = host.privilegedPeople
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.memberFK, ti.memberFK)
            self.assertEqual(di.privilegeFK, ti.privilegeFK)
        self.assertGreater(resultCount, 0)


    """ Test that we can retieve a permission from the global privilege assignment. """
    def test_privilegepersonassignment_privilege_relationship(self):
        direct = models.Privilege.query.filter_by(pk=4).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, 4)

        host = models.GlobalPrivilegeAssignment.query.filter_by(pk=2).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.privilegeFK, direct.pk)

        target = host.privilege
        self.assertIsNotNone(target)
        self.assertEqual(target.pk, direct.pk)
        self.assertEqual(target.privilege, direct.privilege)
    """ Test that we can retieve global privilege assignments from a privilege. """
    def test_privilege_privilegepersonassignment_relationship(self):
        directList = models.GlobalPrivilegeAssignment.query.filter_by(privilegeFK=4)
        self.assertIsNotNone(directList)

        host = models.Privilege.query.filter_by(pk=4).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, 4)

        targetList = host.privilegedGlobalPeople
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.personentityFK, ti.personentityFK)
            self.assertEqual(di.privilegeFK, ti.privilegeFK)
        self.assertGreater(resultCount, 0)


    """ Test that we can retieve a member from the person-assignment. """
    def test_privilegepersonassignment_member_relationship(self):
        direct = models.Member.query.filter_by(pk=1).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.pk, 1)

        host = models.PrivilegePersonAssignment.query.filter_by(pk=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.memberFK, direct.pk)

        target = host.member
        self.assertIsNotNone(target)
        self.assertEqual(target.pk, direct.pk)
        self.assertEqual(target.personentityFK, direct.personentityFK)
        self.assertEqual(target.organizationentityFK, direct.organizationentityFK)
    """ Test that we can retieve a person-assignments from a member. """
    def test_member_privilegepersonassignment_relationship(self):
        directList = models.PrivilegePersonAssignment.query.filter_by(memberFK=1)
        self.assertIsNotNone(directList)

        host = models.Member.query.filter_by(pk=1).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, 1)

        targetList = host.memberPrivileges
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.memberFK, ti.memberFK)
            self.assertEqual(di.privilegeFK, ti.privilegeFK)
        self.assertGreater(resultCount, 0)


    """ Test that we can retieve a person from the global privilege assignment. """
    def test_globalpersonassignment_person_relationship(self):
        direct = models.Person.query.filter_by(entityFK=5).first()
        self.assertIsNotNone(direct)
        self.assertEqual(direct.entityFK, 5)

        host = models.GlobalPrivilegeAssignment.query.filter_by(pk=5).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.personentityFK, direct.entityFK)

        target = host.person
        self.assertIsNotNone(target)
        self.assertEqual(target.entityFK, direct.entityFK)
        self.assertEqual(target.firstname, direct.firstname)
        self.assertEqual(target.lastname, direct.lastname)
    """ Test that we can retieve global privilege assignments from a person. """
    def test_person_globalpersonassignment_relationship(self):
        directList = models.GlobalPrivilegeAssignment.query.filter_by(personentityFK=5)
        self.assertIsNotNone(directList)

        host = models.Person.query.filter_by(entityFK=5).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, 5)

        targetList = host.personGlobalPrivileges
        self.assertIsNotNone(targetList)
        resultCount = 0
        for di,ti in zip(directList, targetList):
            resultCount += 1
            self.assertEqual(di.pk, ti.pk)
            self.assertEqual(di.personentityFK, ti.personentityFK)
            self.assertEqual(di.privilegeFK, ti.privilegeFK)
        self.assertGreater(resultCount, 0)


    """ Test that we can retrieve an entity from the person relationship. """
    def test_person_entity_relationship(self):
        currEntityDirect = models.Entity.query.filter_by(pk = 3).first()
        self.assertEqual(currEntityDirect.type, models.TYPE_EMPLOYEE)
        currentObject = models.Person.query.filter_by(entityFK = 3).first()
        self.assertEqual(currentObject.firstname, 'Chris')
        currEntityByPerson = currentObject.entity
        self.assertEqual(currEntityByPerson.type, models.TYPE_EMPLOYEE)
        self.assertEqual(currEntityDirect, currEntityByPerson)

        currEntityDirect = models.Entity.query.filter_by(pk = 4).first()
        self.assertEqual(currEntityDirect.type, models.TYPE_EMPLOYEE)
        currentObject = models.Person.query.filter_by(entityFK = 4).first()
        self.assertEqual(currentObject.firstname, 'Ryoji')
        currEntityByPerson = currentObject.entity
        self.assertEqual(currEntityByPerson.type, models.TYPE_EMPLOYEE)
        self.assertEqual(currEntityDirect, currEntityByPerson)

        currEntityDirect = models.Entity.query.filter_by(pk = 5).first()
        self.assertEqual(currEntityDirect.type, models.TYPE_EMPLOYEE)
        currentObject = models.Person.query.filter_by(entityFK = 5).first()
        self.assertEqual(currentObject.firstname, 'Dan')
        currEntityByPerson = currentObject.entity
        self.assertEqual(currEntityByPerson.type, models.TYPE_EMPLOYEE)
        self.assertEqual(currEntityDirect, currEntityByPerson)
        
    
    """ Test that we can retrieve an address from the organization relationship """
    def test_organization_address_relationship(self):
        aikonOrg = models.Organization.query.filter_by(entityFK = 1).first()
        self.assertEqual(aikonOrg.entity.addresses[0].address1, '123 Vroom Street')

        uOfMOrg = models.Organization.query.filter_by(entityFK = 2).first()
        self.assertEqual(uOfMOrg.entity.addresses[0].address1, '66 Chancellors Circle')

    
    """ Test that we can retrieve an address from the person relationship """
    def test_person_address_relationship(self):
        currTarget = models.Person.query.filter_by(entityFK = 3).first()
        self.assertEqual(currTarget.entity.addresses[0].address1, '2116 - 991D Markham Rd')
        self.assertEqual(currTarget.entity.addresses[1].address1, '16 Premier Place')

        currTarget = models.Person.query.filter_by(entityFK = 4).first()
        self.assertEqual(currTarget.entity.addresses[0].address1, '2194 Pembina Hwy')

        currTarget = models.Person.query.filter_by(entityFK = 5).first()
        self.assertEqual(currTarget.entity.addresses[0].address1, '123 Main St')
        

    """ Test that we can get contacts from an entity """
    def test_entity_contact_relationship(self):
        entity = models.Entity.query.filter_by(pk = 1).first()
        self.assertEqual(entity.contacts[0].value, 'info@ai-kon.org')

        entity = models.Entity.query.filter_by(pk = 2).first()
        self.assertEqual(entity.contacts[0].value, '18004321960')

    
    """ Test adding a complete organization to the database """
    def test_add_organization(self):
        """ Define the data objects to be added """
        org1 = models.Organization(name='Test Org',
                            description='This is a test organization')
        org1.entity = models.Entity(type=models.TYPE_ORGANIZATION)
        org1.entity.addresses.append(models.Address(address1='4350 University Drive', address2='Suite 350',
                           city='Winnipeg', province='Manitoba',
                           isprimary=True))
        org1.entity.contacts.append(models.Contact(type=models.TYPE_PHONE,
                                  value='(204) 555-1234', isprimary=True))
        
        """ Add the data objects """       
        self.db.session.add(org1)
        self.db.session.commit()

        """ Retrieve the organization and test that data matches """
        org2 = models.Organization.query.filter_by(name='Test Org').first()
        self.assertEqual(org2, org1)
        self.assertIsNotNone(org2.entity)
        self.assertEqual(org2.entity.addresses[0].address1, '4350 University Drive')
        self.assertEqual(org2.entity.contacts[0].value, '(204) 555-1234')

        """ Try grabbing some of the sub-objects from the database """
        entity2 = models.Entity.query.filter_by(pk=org2.entity.pk).first()
        self.assertIsNotNone(entity2)

        address2 = models.Address.query.filter_by(pk=org2.entity.addresses[0].pk).first()
        self.assertEqual(address2.address1, '4350 University Drive')

        contact2 = models.Contact.query.filter_by(pk=org2.entity.contacts[0].pk).first()
        self.assertEqual(contact2.value, '(204) 555-1234')
    

    """ Test adding a complete person to the database """
    def test_add_person(self):
        """ Define the data objects to be added """
        target = models.Person(firstname='Test',
                            lastname='Person')
        target.entity = models.Entity(type=models.TYPE_EMPLOYEE)
        target.entity.addresses.append(models.Address(address1='4350 University Drive', address2='Suite 350', address3='C/O The cat down the hall',
                           city='Winnipeg', province='Manitoba',country='Canada',
                           postalcode='A1A 1A1', isprimary=True))
        target.entity.contacts.append(models.Contact(type=models.TYPE_PHONE,
                                  value='(204) 555-1234', isprimary=True))
        
        """ Add the data objects """       
        self.db.session.add(target)
        self.db.session.commit()

        """ Retrieve the organization and test that data matches """
        fetched = models.Person.query.filter_by(firstname='Test', lastname='Person').first()
        self.assertEqual(fetched, target)
        self.assertIsNotNone(fetched.entity)
        self.assertEqual(fetched.entity.addresses[0].address1, '4350 University Drive')
        self.assertEqual(fetched.entity.contacts[0].value, '(204) 555-1234')

        """ Try grabbing some of the sub-objects from the database """
        entity2 = models.Entity.query.filter_by(pk=fetched.entity.pk).first()
        self.assertIsNotNone(entity2)

        address2 = models.Address.query.filter_by(pk=fetched.entity.addresses[0].pk).first()
        self.assertEqual(address2.address1, '4350 University Drive')

        contact2 = models.Contact.query.filter_by(pk=fetched.entity.contacts[0].pk).first()
        self.assertEqual(contact2.value, '(204) 555-1234')

        
    def test_organization_delete(self):
        """ Test that our organization exists prior to deleting. """
        org2 = models.Organization.query.filter_by(entityFK=1).first()
        self.assertIsNotNone(org2)

        """ Delete Organization 1 """
        org1 = models.Organization.query.filter_by(entityFK=1).first()
        self.db.session.delete(org1)
        self.db.session.commit()

        """ Test that it has been deleted """
        org2 = models.Organization.query.filter_by(entityFK=1).first()
        self.assertIsNone(org2)

        """ Check if the first entity is no longer entity.pk==1
            This will determine if entity was auto-deleted and that
            other entities still exist """
        entity1 = models.Entity.query.first()
        self.assertIsNotNone(entity1)
        self.assertNotEqual(entity1.pk, 1)

        """ Test that the addresses and contacts have been deleted """
        address1 = models.Address.query.filter_by(entityFK=1).first()
        contact1 = models.Contact.query.filter_by(entityFK=1).first()
        self.assertIsNone(address1)
        self.assertIsNone(contact1)

        """ Reset the DB for other tests, since we removed data other tests may depend on. """
        self.resetDB()


    def test_person_delete(self):
        """ Add our privilege prior to deleting. """
        target = models.Person.query.filter_by(entityFK=3).first()
        self.assertIsNotNone(target)

        """ Delete target """
        self.db.session.delete(target)
        self.db.session.commit()

        """ Test that it has been deleted """
        target = models.Organization.query.filter_by(entityFK=3).first()
        self.assertIsNone(target)

        """ Verify entity record deleted. """
        entity1 = models.Entity.query.filter_by(pk=3).first()
        self.assertIsNone(entity1)

        """ Test that the addresses and contacts have been deleted """
        address1 = models.Address.query.filter_by(entityFK=3).first()
        contact1 = models.Contact.query.filter_by(entityFK=3).first()
        self.assertIsNone(address1)
        self.assertIsNone(contact1)

        """ Reset the DB for other tests, since we removed data other tests may depend on. """
        self.resetDB()
    

if __name__ == "__main__":
    unittest.main()
