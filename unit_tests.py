#!./venv/bin/python
import os
import unittest
import ESA
from ESA import config_test
from ESA import models

class ESATestCase(unittest.TestCase):

    def setUp(self):
        ESA.app.config['TESTING'] = True
        self.app = ESA.app.test_client()
        
    def tearDown(self):
        pass

    def test_main_page(self):
        rv = self.app.get('/')
        assert 'ESA Service' in rv.data
        
if __name__ == "__main__":
    unittest.main()
