#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class PersonTestCase(TestCase):
    database_uri = "sqlite:///person_unittest.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.person_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.person_test_data)
        self.db = models.init_app(self.app)


    """ Test that person objects are defined and the model represents them correctly. """
    def test_person_model(self):
        chris = models.Person.query.filter_by(entityFK=3).first()
        self.assertEqual(chris.entityFK, 3)
        self.assertEqual(chris.firstname, 'Chris')
        self.assertEqual(chris.lastname, 'Workman')
        self.assertEqual(chris.username, 'user0')
        self.assertEqual(chris.password, 'password0')

        ryoji = models.Person.query.filter_by(entityFK=4).first()
        self.assertEqual(ryoji.entityFK, 4)
        self.assertEqual(ryoji.firstname, 'Ryoji')
        self.assertEqual(ryoji.lastname, 'Betchaku')
        self.assertEqual(ryoji.username, 'user1')
        self.assertEqual(ryoji.password, 'password1')

        dan = models.Person.query.filter_by(entityFK=5).first()
        self.assertEqual(dan.entityFK, 5)
        self.assertEqual(dan.firstname, 'Dan')
        self.assertEqual(dan.lastname, 'Nelson')
        self.assertEqual(dan.username, 'meat_lol')
        self.assertEqual(dan.password, 'password2')
        
    
    """ Test that we can retrieve an entity from the person relationship. """
    def test_person_entity_relationship_1(self):
        # Define prerequisite data.
        entityKey = 3
        fname = 'Chris'
        lname = 'Workman'
        username = 'user0'
        password = 'password0'
        # Retrieve the target object directly.
        direct = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Person.query.filter_by(entityFK=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, entityKey)
        self.assertEqual(host.firstname, fname)
        self.assertEqual(host.lastname, lname)
        self.assertEqual(host.username, username)
        self.assertEqual(host.password, password)
        # Retrieve the target object through the containing object.
        target = host.entity
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())
    def test_person_entity_relationship_2(self):
        # Define prerequisite data.
        entityKey = 4
        fname = 'Ryoji'
        lname = 'Betchaku'
        username = 'user1'
        password = 'password1'
        # Retrieve the target object directly.
        direct = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Person.query.filter_by(entityFK=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, entityKey)
        self.assertEqual(host.firstname, fname)
        self.assertEqual(host.lastname, lname)
        self.assertEqual(host.username, username)
        self.assertEqual(host.password, password)
        # Retrieve the target object through the containing object.
        target = host.entity
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())
    def test_person_entity_relationship_3(self):
        # Define prerequisite data.
        entityKey = 5
        fname = 'Dan'
        lname = 'Nelson'
        username = 'meat_lol'
        password = 'password2'
        # Retrieve the target object directly.
        direct = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Person.query.filter_by(entityFK=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, entityKey)
        self.assertEqual(host.firstname, fname)
        self.assertEqual(host.lastname, lname)
        self.assertEqual(host.username, username)
        self.assertEqual(host.password, password)
        # Retrieve the target object through the containing object.
        target = host.entity
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())
        
    
    """ Test that we can retrieve members from the person relationship. """
    def test_person_members_relationship_1(self):
        # Define prerequisite data.
        entityKey = 4
        # Retrieve the target object directly.
        directList = models.Member.query.filter_by(personentityFK=entityKey)
        self.assertIsNotNone(directList)
        # Retrieve the containing object.
        host = models.Person.query.filter_by(entityFK=entityKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, entityKey)
        # Retrieve the target object through the containing object.
        targetList = host.memberships
        self.assertIsNotNone(targetList)
        count = 0
        for di,ti in zip(directList,targetList):
            count += 1
            self.assertEqual(di.__repr__(), ti.__repr__())
        self.assertEqual(count, 2)
        
        
    """ Test that we can retieve global privilege assignments from a person. """
    def test_person_gpa_relationship(self):
        # Define prerequisite data.
        key = 5
        # Retrieve the target object directly.
        directList = models.GlobalPrivilegeAssignment.query.filter_by(personentityFK=key)
        self.assertIsNotNone(directList)
        # Retrieve the containing object.
        host = models.Person.query.filter_by(entityFK=key).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.entityFK, key)
        # Retrieve the target object through the containing object.
        targetList = host.gpaList
        self.assertIsNotNone(targetList)
        count = 0
        for di,ti in zip(directList,targetList):
            count += 1
            self.assertEqual(di.__repr__(), ti.__repr__())
        self.assertEqual(count, 2)
    

    """ Test adding a Person. """
    def test_person_add(self):
        # Verify state of related tables before operation.
        personCount = models.Person.query.count()
        entityCount = models.Entity.query.count()
        memberCount = models.Member.query.count()
        
        # Define prerequisite data.
        fname = 'new fname'
        lname = 'new lname'
        username = 'new_user'
        password = 'new_password'
        target = models.Person(fname, lname, username, password)
        target.entity = models.Entity(models.TYPE_EMPLOYEE)

        # Verify that the data does not already exist.
        fetched = models.Person.query.filter_by(firstname=fname, lastname=lname).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.Person.query.filter_by(firstname=fname, lastname=lname)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.firstname, target.firstname)
            self.assertEqual(item.lastname, target.lastname)
            self.assertEqual(item.username, target.username)
            self.assertEqual(item.password, target.password)
            count += 1
        self.assertEqual(count, 1)

        # Verify state of related tables after the operation.
        personCountAfter = models.Person.query.count()
        entityCountAfter = models.Entity.query.count()
        memberCountAfter = models.Member.query.count()
        self.assertTrue(personCountAfter == personCount + 1)
        self.assertTrue(entityCountAfter == entityCount + 1)
        self.assertEqual(memberCountAfter, memberCount)


    """ Test updating a Person. """
    def test_person_update(self):
        # Verify state of related tables before operation.
        personCount = models.Person.query.count()
        entityCount = models.Entity.query.count()
        memberCount = models.Member.query.count()
        
        # Define prerequisite data.
        key = 3
        name = 'new fname'

        # Verify that the data exists.
        count = models.Person.query.filter_by(entityFK=key).count()
        self.assertEqual(count, 1)
        target = models.Person.query.filter_by(entityFK=key).first()
        self.assertIsNotNone(target)
        
        # Perform the operation.
        target.firstname = name
        merged = self.db.session.merge(target)
        self.db.session.commit()

        # Verify that the data was updated.
        self.assertTrue(merged.__repr__() == target.__repr__())
        count = models.Person.query.filter_by(entityFK=key).count()
        self.assertEqual(count, 1)
        fetched = models.Person.query.filter_by(entityFK=key).first()
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.entityFK, target.entityFK)
        self.assertEqual(fetched.firstname, target.firstname)
        self.assertEqual(fetched.lastname, target.lastname)
        self.assertEqual(fetched.username, target.username)
        self.assertEqual(fetched.password, target.password)



        # Verify state of related tables after the operation.
        personCountAfter = models.Person.query.count()
        entityCountAfter = models.Entity.query.count()
        memberCountAfter = models.Member.query.count()
        self.assertEqual(entityCount, entityCountAfter)
        self.assertEqual(personCount, personCountAfter)
        self.assertEqual(memberCount, memberCountAfter)

        #self.resetDB()


    """ Test deleting a person. """
    def test_person_delete(self):
        # Verify state of related tables before operation.
        personCount = models.Person.query.count()
        entityCount = models.Entity.query.count()
        memberCount = models.Member.query.count()
        
        # Define prerequisite data.
        key = 5

        # Verify that the data exists.
        fetched = models.Person.query.filter_by(entityFK=key).first()
        self.assertIsNotNone(fetched)
        
        # Perform the operation.
        self.db.session.delete(fetched)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        count = models.Person.query.filter_by(entityFK=key).count()
        self.assertEqual(count, 0)

        # Verify state of related tables after the operation.
        personCountAfter = models.Person.query.count()
        entityCountAfter = models.Entity.query.count()
        memberCountAfter = models.Member.query.count()
        self.assertTrue(entityCountAfter == entityCount - 1)
        self.assertTrue(personCountAfter == personCount - 1)
        self.assertTrue(memberCountAfter == memberCount - 1)

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(PersonTestCase('test_person_model'))
    suite.addTest(PersonTestCase('test_person_entity_relationship_1'))
    suite.addTest(PersonTestCase('test_person_entity_relationship_2'))
    suite.addTest(PersonTestCase('test_person_entity_relationship_3'))
    
    suite.addTest(PersonTestCase('test_person_members_relationship_1'))
    suite.addTest(PersonTestCase('test_person_gpa_relationship'))
    
    suite.addTest(PersonTestCase('test_person_add'))
    suite.addTest(PersonTestCase('test_person_update'))
    suite.addTest(PersonTestCase('test_person_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

