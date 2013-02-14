import os
import unittest
from ESA import app
from ESA.model import database

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ESA.app.test_client()
        
if __name__ == "__main__":
    unittest.main()
