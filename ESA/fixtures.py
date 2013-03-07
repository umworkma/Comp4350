from fixture import DataSet, SQLAlchemyFixture
from fixture.style import NamedDataStyle

import models

def install(app, *args):
    engine = models.create_tables(app)
    db = SQLAlchemyFixture(env=models, style=NamedDataStyle(), engine=engine)
    data = db.data(*args)
    data.setup()
    db.dispose()

class EntityData(DataSet):
    class entity01:
        type = 1

    class entity02:
        type = 1

    class entity03:
        type = 2

    class entity04:
        type = 2

    class entity05:
        type = 2

class OrganizationData(DataSet):
    class organization01:
        entityFK = 1
        name = 'Ai-Kon'
        description = 'Ai-Kon Anime Convention'

    class organization02:
        entityFK = 2
        name = 'University of Manitoba'
        description = 'The University of Manitoba, is a public university in the province of Manitoba, Canada. Located in Winnipeg, it is Manitoba\'s largest, most comprehensive, and only research-intensive post-secondary educational institution.'

class PersonData(DataSet):
    class person01:
        entityFK = 3
        firstname = 'Chris'
        lastname = 'Workman'
        username = 'user0'
        password = 'password0'

    class person02:
        entityFK = 4
        firstname = 'Ryoji'
        lastname = 'Betchaku'
        username = 'user1'
        password = 'password1'

    class person04:
        entityFK = 5
        firstname = 'Dan'
        lastname = 'Nelson'
        username = 'meat_lol'
        password = 'password2'

class AddressData(DataSet):
    class address01:
        address1 = '123 Vroom Street'
        city = 'Winnipeg'
        province = 'Manitoba'
        country = 'Canada'
        postalcode = 'A1A1A1'
        entityFK = 1
        isprimary = 1

    class address02:
        address1 = '66 Chancellors Circle'
        city = 'Winnipeg'
        province = 'Manitoba'
        country = 'Canada'
        postalcode = 'R3T2N2'
        entityFK = 2
        isprimary = 1

    class address03:
        address1 = '2116 - 991D Markham Rd'
        city = 'Winnipeg'
        province = 'Manitoba'
        country = 'Canada'
        postalcode = 'R3K 5J1'
        entityFK = 3
        isprimary = 1

    class address04:
        address1 = '16 Premier Place'
        city = 'Winnipeg'
        province = 'Manitoba'
        country = 'Canada'
        postalcode = 'R2C 0S9'
        entityFK = 3
        isprimary = 0

    class address05:
        address1 = '2194 Pembina Hwy'
        city = 'Winnipeg'
        province = 'Manitoba'
        country = 'Canada'
        postalcode = 'R1G 5V4'
        entityFK = 4
        isprimary = 1

    class address06:
        address1 = '123 Main St'
        city = 'Selkirk'
        province = 'Manitoba'
        country = 'Canada'
        postalcode = '1V1 F2F'
        entityFK = 5
        isprimary = 1

class ContactData(DataSet):
    class contact01:
        entityFK = 1
        type = 2
        value = 'info@ai-kon.org'
        isprimary = 1

    class contact02:
        entityFK = 2
        type = 1
        value = '18004321960'
        isprimary = 1

    class contact03:
        entityFK = 3
        type = 2
        value = 'umworkma@cc.umanitoba.ca'
        isprimary = 1

    class contact04:
        entityFK = 3
        type = 1
        value = '2042302916'
        isprimary = 0

    class contact05:
        entityFK = 3
        type = 1
        value = '2042247721'
        isparimy = 1

    class contact06:
        entityFK = 4
        type = 1
        value = '2042916589'
        isprimary = 1

    class contact07:
        entityFK = 5
        type = 1
        value = '2046634588'
        isprimary = 1


class PrivilegeData(DataSet):
    class privilege01:
        privilege = 'REGISTER_NEW_ORGANIZATION'

    class privilege02:
        privilege = 'MODIFY_ORGANIZATION'

    class privilege03:
        privilege = 'DELETE_ORGANIZATION'

    class privilege04:
        privilege = 'VIEW_ALL_ORGANIZATIONS'

    class privilege05:
        privilege = 'VIEW_ALL_EMPLOYEES_IN_ORG'

    class privilege06:
        privilege = 'ASSIGN_EMPS_TO_SHIFTS'

    class privilege07:
        privilege = 'SOME_OTHER_EMP_PRIVILEGE'

    class privilege08:
        privilege = 'YET_ANOTHER_EMP_PRIVILEGE'


class MemberData(DataSet):
    class member01:
        personentityFK = 3
        organizationentityFK = 1

    class member02:
        personentityFK = 4
        organizationentityFK = 1

    class member03:
        personentityFK = 4
        organizationentityFK = 2

    class member04:
        personentityFK = 5
        organizationentityFK = 2
        

class PrivilegePersonAssignmentData(DataSet):
    class personPrivilegeAssign01:
        privilegeFK = 5
        memberFK = 1

    class personPrivilegeAssign02:
        privilegeFK = 6
        memberFK = 1

    class personPrivilegeAssign03:
        privilegeFK = 7
        memberFK = 2

    class personPrivilegeAssign04:
        privilegeFK = 8
        memberFK = 3

    class personPrivilegeAssign05:
        privilegeFK = 5
        memberFK = 4

    class personPrivilegeAssign06:
        privilegeFK = 6
        memberFK = 4
        
    class personPrivilegeAssign07:
        privilegeFK = 7
        memberFK = 3

class GlobalPrivilegeAssignmentData(DataSet):
    class globalPrivilegeAssign01:
        privilegeFK = 1
        personentityFK = 3

    class globalPrivilegeAssign02:
        privilegeFK = 4
        personentityFK = 3

    class globalPrivilegeAssign03:
        privilegeFK = 3
        personentityFK = 4

    class globalPrivilegeAssign04:
        privilegeFK = 4
        personentityFK = 4

    class globalPrivilegeAssign05:
        privilegeFK = 2
        personentityFK = 5

    class globalPrivilegeAssign06:
        privilegeFK = 4
        personentityFK = 5

class EventData(DataSet):
    class event1:
        name='My Event'
        description='This is my event'
        organizationFK=1

    class event2:
        name='Your Event'
        description='This is your event'
        organizationFK=2

all_data = (EntityData, PersonData, AddressData, OrganizationData, ContactData,
            PrivilegeData, MemberData, PrivilegePersonAssignmentData,
            GlobalPrivilegeAssignmentData, EventData)
entity_test_data = (EntityData, AddressData, ContactData, OrganizationData, PersonData)
address_test_data = (AddressData, EntityData)
contact_test_data = (ContactData, EntityData)
organization_test_data = (OrganizationData, EntityData, MemberData)
person_test_data = (PersonData, EntityData, MemberData, GlobalPrivilegeAssignmentData)
member_test_data = (MemberData, PersonData, OrganizationData, PrivilegePersonAssignmentData)
privilege_test_data = (PrivilegeData, PrivilegePersonAssignmentData, GlobalPrivilegeAssignmentData, MemberData)
ppa_test_data = (PrivilegeData, PrivilegePersonAssignmentData, MemberData)
gpa_test_data = (PrivilegeData, GlobalPrivilegeAssignmentData, MemberData, PersonData)
event_test_data = (EventData,)
