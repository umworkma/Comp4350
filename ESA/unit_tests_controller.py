#!../venv/bin/python
import unittest

from flask import Flask
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
    

    
    """ Test that we can register an organization. """
    def test1(self):
        """ Construct JSON object. """
        json =  '{'
        json += '"org_name": "Test Org",'
        json += '"org_desc": "Test org description",'
        json += '"phone": "12042345678",'
        json += '"address1": "123 Test Ogrg Way",'
        json += '"address2": "PO Box 111",'
        json += '"address3": "C/O Customer Service",'
        json += '"city": "Winnipeg",'
        json += '"province": "Manitoba",'
        json += '"country": "Canada",'
        json += '"email": "abuse@testorg.ca"'
        json += '}'

        allOrgsBefore = controllers.getAllOrganizations()
        result = controllers.registerOrganization(json)
        allOrgsAfter = controllers.getAllOrganizations()

        salf.assertEquals(result, True)

if __name__ == "__main__":
    unittest.main()
