#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class AddressTestCase(TestCase):
    database_uri = "sqlite:///address_unittest.db"
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri


    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    @classmethod
    def setUpClass(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.address_test_data)
        self.db = models.init_app(self.app)

    @classmethod
    def tearDownClass(self):
        self.db.session.remove()
        self.db.drop_all()

    def resetDB(self):
        self.db.session.remove()
        self.db.drop_all()
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.address_test_data)
        self.db = models.init_app(self.app)


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
    

    """ Test that an entity can be retrieved from an address relationship. """
    def test_address_entity_relationship_1(self):
        # Define prerequisite data.
        entityKey = 1
        addressKey = 1
        address1Value = '123 Vroom Street'
        isprimaryValue = 1
        # Retrieve the target object directly.
        direct = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Address.query.filter_by(pk=addressKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, entityKey)
        self.assertEqual(host.address1, address1Value)
        self.assertEqual(host.isprimary, isprimaryValue)
        # Retrieve the target object through the containing object.
        target = host.entity
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())
    """ Test that an entity can be retrieved from an address relationship. """
    def test_address_entity_relationship_2(self):
        # Define prerequisite data.
        entityKey = 2
        addressKey = 2
        address1Value = '66 Chancellors Circle'
        isprimaryValue = 1
        # Retrieve the target object directly.
        direct = models.Entity.query.filter_by(pk=entityKey).first()
        self.assertIsNotNone(direct)
        # Retrieve the containing object.
        host = models.Address.query.filter_by(pk=addressKey).first()
        self.assertIsNotNone(host)
        self.assertEqual(host.pk, entityKey)
        self.assertEqual(host.address1, address1Value)
        self.assertEqual(host.isprimary, isprimaryValue)
        # Retrieve the target object through the containing object.
        target = host.entity
        self.assertIsNotNone(target)
        self.assertEqual(direct.__repr__(), target.__repr__())


    """ Test adding an Address. """
    def test_address_add(self):
        # Verify state of related tables before operation.
        addressesCount = models.Address.query.count()
        entityCount = models.Entity.query.count()
        
        # Define prerequisite data.
        entityKey = 1
        address1Value = 'New Adddress 1'
        address2Value = 'New Adddress 2'
        address3Value = 'New Adddress 3'
        cityValue = 'Sydney'
        provValue = 'NSW'
        countryValue = 'Australia'
        postalcodeValue = 'B2B 2B2'
        isprimaryValue = False
        target = models.Address(address1Value, address2Value, address3Value, cityValue, provValue, countryValue, postalcodeValue, entityKey, isprimaryValue)

        # Verify that the data does not already exist.
        fetched = models.Address.query.filter_by(entityFK=entityKey, address1=address1Value, address2=address2Value, address3=address3Value, city=cityValue).first()
        self.assertIsNone(fetched)
        
        # Perform the operation.
        self.db.session.add(target)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        fetchedList = models.Address.query.filter_by(entityFK=entityKey, address1=address1Value, address2=address2Value, address3=address3Value, city=cityValue)
        self.assertIsNotNone(fetchedList)
        count = 0
        for item in fetchedList:
            self.assertEqual(item.entityFK, target.entityFK)
            self.assertEqual(item.address1, target.address1)
            self.assertEqual(item.address2, target.address2)
            self.assertEqual(item.address3, target.address3)
            self.assertEqual(item.city, target.city)
            self.assertEqual(item.province, target.province)
            self.assertEqual(item.country, target.country)
            self.assertEqual(item.postalcode, target.postalcode)
            self.assertEqual(item.isprimary, target.isprimary)
            count += 1
        self.assertEqual(count, 1)

        # Verify state of related tables after the operation.
        addressesCountAfter = models.Address.query.count()
        entityCountAfter = models.Entity.query.count()
        self.assertEqual(entityCount, entityCountAfter)
        self.assertTrue(addressesCountAfter == addressesCount + 1)


    """ Test adding an Address. """
    def test_address_update(self):
        # Verify state of related tables before operation.
        addressesCount = models.Address.query.count()
        entityCount = models.Entity.query.count()
        
        # Define prerequisite data.
        addressKey = 1
        address1Value = 'New Adddress 1'
        address2Value = 'New Adddress 2'
        address3Value = 'New Adddress 3'
        cityValue = 'Sydney'
        provinceValue = 'NSW'
        countryValue = 'Australia'
        postalcodeValue = 'B2B 2B2'

        # Verify that the data exists.
        count = models.Address.query.filter_by(pk=addressKey).count()
        self.assertEqual(count, 1)
        target = models.Address.query.filter_by(pk=addressKey).first()
        self.assertIsNotNone(target)
        
        # Perform the operation.
        target.address1 = address1Value
        target.address2 = address2Value
        target.address3 = address3Value
        target.city = cityValue
        target.province = provinceValue
        target.country = countryValue
        target.postalcode = postalcodeValue
        merged = self.db.session.merge(target)
        self.db.session.commit()

        # Verify that the data was updated.
        self.assertTrue(merged.__repr__() == target.__repr__())
        count = models.Address.query.filter_by(pk=addressKey).count()
        self.assertEqual(count, 1)
        fetched = models.Address.query.filter_by(pk=addressKey).first()
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.entityFK, target.entityFK)
        self.assertEqual(fetched.address1, target.address1)
        self.assertEqual(fetched.address2, target.address2)
        self.assertEqual(fetched.address3, target.address3)
        self.assertEqual(fetched.city, target.city)
        self.assertEqual(fetched.province, target.province)
        self.assertEqual(fetched.country, target.country)
        self.assertEqual(fetched.postalcode, target.postalcode)
        self.assertEqual(fetched.isprimary, target.isprimary)

        # Verify state of related tables after the operation.
        addressesCountAfter = models.Address.query.count()
        entityCountAfter = models.Entity.query.count()
        self.assertEqual(entityCount, entityCountAfter)
        self.assertTrue(addressesCountAfter == addressesCount)

        #self.resetDB()


    """ Test deleting an address. """
    def test_address_delete(self):
        # Verify state of related tables before operation.
        addressesCount = models.Address.query.count()
        entityCount = models.Entity.query.count()
        
        # Define prerequisite data.
        addressKey = 1

        # Verify that the data exists.
        fetched = models.Address.query.filter_by(pk=addressKey).first()
        self.assertIsNotNone(fetched)
        
        # Perform the operation.
        self.db.session.delete(fetched)
        self.db.session.commit()

        # Verify that the data was added, and only added once.
        count = models.Address.query.filter_by(pk=addressKey).count()
        self.assertEqual(count, 0)

        # Verify state of related tables after the operation.
        addressesCountAfter = models.Address.query.count()
        entityCountAfter = models.Entity.query.count()
        self.assertEqual(entityCount, entityCountAfter)
        self.assertTrue(addressesCountAfter == addressesCount - 1)

        #self.resetDB()


def suite():
    # Define the container for this module's tests.
    suite = unittest.TestSuite()

    # Add tests to suite.
    suite.addTest(AddressTestCase('test_address_model'))
    suite.addTest(AddressTestCase('test_address_entity_relationship_1'))
    suite.addTest(AddressTestCase('test_address_entity_relationship_2'))
    suite.addTest(AddressTestCase('test_address_add'))
    suite.addTest(AddressTestCase('test_address_update'))
    suite.addTest(AddressTestCase('test_address_delete'))
    
    return suite
    

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

