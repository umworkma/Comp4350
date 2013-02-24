#!../venv/bin/python
import unittest

import unit_tests_privilege


def suite():
    # Define a suite to group other test suites.
    allUnitTests = unittest.TestSuite()

    # Add the test suite to our grouping.
    allUnitTests.addTest(unit_tests_privilege.suite())

    return allUnitTests



if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
