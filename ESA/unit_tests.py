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

    

if __name__ == "__main__":
    unittest.main()
