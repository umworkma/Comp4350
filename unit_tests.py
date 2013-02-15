import os
import unittest
import tempfile
import ESA

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, ESA.app.config['DATABASE'] = tempfile.mkstemp()
        ESA.app.config['TESTING'] = True
        self.app = ESA.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(ESA.app.config['DATABASE'])

    def test_main_page(self):
        rv = self.app.get('/')
        assert 'ESA Service' in rv.data
        
if __name__ == "__main__":
    unittest.main()
