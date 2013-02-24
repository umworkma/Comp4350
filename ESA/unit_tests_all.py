#!../venv/bin/python
import unittest

import unit_tests_privilege
import unit_tests_member
import unit_tests_privilegepersonassignment
import unit_tests_globalprivilegeassignment


def suite():
    # Define a suite to group other test suites.
    allUnitTests = unittest.TestSuite()

    # Add the test suite to our grouping.
    allUnitTests.addTest(unit_tests_privilege.suite())
    allUnitTests.addTest(unit_tests_member.suite())
    allUnitTests.addTest(unit_tests_privilegepersonassignment.suite())
    allUnitTests.addTest(unit_tests_globalprivilegeassignment.suite())

    return allUnitTests



if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
