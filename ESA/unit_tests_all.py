#!../venv/bin/python
import unittest

import unit_tests_entity
import unit_tests_organization
import unit_tests_person
import unit_tests_address
import unit_tests_contact
import unit_tests_privilege
import unit_tests_member
import unit_tests_privilegepersonassignment
import unit_tests_globalprivilegeassignment
import unit_tests_controller


def suite():
    # Define a suite to group other test suites.
    allUnitTests = unittest.TestSuite()

    # Add the test suite to our grouping.
    allUnitTests.addTest(unit_tests_entity.suite())
    allUnitTests.addTest(unit_tests_address.suite())
    allUnitTests.addTest(unit_tests_contact.suite())
    allUnitTests.addTest(unit_tests_organization.suite())
    allUnitTests.addTest(unit_tests_person.suite())
    allUnitTests.addTest(unit_tests_privilege.suite())
    allUnitTests.addTest(unit_tests_member.suite())
    allUnitTests.addTest(unit_tests_privilegepersonassignment.suite())
    allUnitTests.addTest(unit_tests_globalprivilegeassignment.suite())
    allUnitTests.addTest(unit_tests_controller.suite())

    return allUnitTests



if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
