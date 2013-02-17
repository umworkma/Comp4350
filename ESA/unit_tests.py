#!../venv/bin/python
import unittest

from flask import Flask
from flask.ext.testing import TestCase

import fixtures
import models

class ESATestCase(TestCase):

    database_uri = "sqlite:///test.db"

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri
        return app

    def setUp(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.all_data)
        self.db = models.init_app(self.app)
        
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_entity(self):
        entity1 = models.Entity.query.first()
        self.assertEquals(entity1.type, models.TYPE_ORGANIZATION)

        entity2 = models.Entity.query.filter_by(pk=3).first()
        self.assertEquals(entity2.type, models.TYPE_EMPLOYEE)

        address1 = models.Address.query.first()
        self.assertEquals(address1.address1, '123 Vroom Street')

        address2 = entity1.addresses[0]
        self.assertEquals(address1, address2)
        
if __name__ == "__main__":
    unittest.main()
