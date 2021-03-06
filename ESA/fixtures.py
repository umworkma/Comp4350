from fixture import DataSet, SQLAlchemyFixture
from fixture.style import NamedDataStyle
from datetime import datetime

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

    class entity06:
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

    class person05:
        entityFK = 6
        firstname = 'Cookie'
        lastname = 'Monster'
        username = 'cookie'
        password = 'cookie'

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

    class address07:
        address1 = '123 Sesame Street'
        city = 'New York'
        province = 'Manitoba'
        country = 'United States'
        postalcode = '10023'
        entityFK = 6
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

    class member05:
        personentityFK = 6
        organizationentityFK = 1
        

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
        startdate=datetime(2013, 7, 12, 12, 0)
        enddate=datetime(2013, 7, 14, 16, 0)
        organizationFK=1

    class event2:
        name='Your Event'
        description='This is your event'
        organizationFK=2

    class event3:
        name='Comic Con - Winnipeg'
        description='A three-day pop culture event held in October or early November. The event features celebrity guests, comic book artists, exhibitors, costume contests, video rooms, gaming, and more.'
        startdate=datetime(2013, 10, 25, 12, 0)
        enddate=datetime(2013, 10, 27, 18, 0)
        organizationFK=1

    class event4:
        name='SXSW - Austin, TX'
        description='South by Southwest (SXSW) is a set of film, interactive, and music festivals and conferences that take place every spring.'
        startdate=datetime(2013, 3, 9, 12, 0)
        enddate=datetime(2013, 3, 12, 20, 0)
        organizationFK=1
        
class ShiftData(DataSet):
    class shift01:
        eventFK=1
        startdatetime=datetime(2013, 7, 12, 12, 0)
        enddatetime=datetime(2013, 7, 12, 13, 0)
        location='Booth A'
        minWorkers=2
        maxWorkers=4
        
    class shift02:
        eventFK=1
        startdatetime=datetime(2013, 7, 12, 13, 0)
        enddatetime=datetime(2013, 7, 12, 14, 0)
        location='Booth A'
        minWorkers=2
        maxWorkers=4
        
    class shift03:
        eventFK=1
        startdatetime=datetime(2013, 7, 12, 14, 0)
        enddatetime=datetime(2013, 7, 12, 15, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4
        
    class shift04:
        eventFK=1
        startdatetime=datetime(2013, 7, 12, 15, 0)
        enddatetime=datetime(2013, 7, 12, 16, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift05:
        eventFK=3
        startdatetime=datetime(2013, 10, 25, 12, 0)
        enddatetime=datetime(2013, 10, 25, 13, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift06:
        eventFK=3
        startdatetime=datetime(2013, 10, 25, 13, 0)
        enddatetime=datetime(2013, 10, 25, 14, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift07:
        eventFK=3
        startdatetime=datetime(2013, 10, 25, 14, 0)
        enddatetime=datetime(2013, 10, 25, 15, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift08:
        eventFK=3
        startdatetime=datetime(2013, 10, 25, 15, 0)
        enddatetime=datetime(2013, 10, 25, 16, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift09:
        eventFK=3
        startdatetime=datetime(2013, 10, 25, 16, 0)
        enddatetime=datetime(2013, 10, 25, 17, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift10:
        eventFK=3
        startdatetime=datetime(2013, 10, 25, 17, 0)
        enddatetime=datetime(2013, 10, 25, 18, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift11:
        eventFK=3
        startdatetime=datetime(2013, 10, 26, 12, 0)
        enddatetime=datetime(2013, 10, 26, 13, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift12:
        eventFK=3
        startdatetime=datetime(2013, 10, 26, 13, 0)
        enddatetime=datetime(2013, 10, 26, 14, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift13:
        eventFK=3
        startdatetime=datetime(2013, 10, 26, 14, 0)
        enddatetime=datetime(2013, 10, 26, 15, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift14:
        eventFK=3
        startdatetime=datetime(2013, 10, 26, 15, 0)
        enddatetime=datetime(2013, 10, 26, 16, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift15:
        eventFK=3
        startdatetime=datetime(2013, 10, 26, 16, 0)
        enddatetime=datetime(2013, 10, 26, 17, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift16:
        eventFK=3
        startdatetime=datetime(2013, 10, 26, 17, 0)
        enddatetime=datetime(2013, 10, 26, 18, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift17:
        eventFK=3
        startdatetime=datetime(2013, 10, 27, 12, 0)
        enddatetime=datetime(2013, 10, 27, 13, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift18:
        eventFK=3
        startdatetime=datetime(2013, 10, 27, 13, 0)
        enddatetime=datetime(2013, 10, 27, 14, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift19:
        eventFK=3
        startdatetime=datetime(2013, 10, 27, 14, 0)
        enddatetime=datetime(2013, 10, 27, 15, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift20:
        eventFK=3
        startdatetime=datetime(2013, 10, 27, 15, 0)
        enddatetime=datetime(2013, 10, 27, 16, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift21:
        eventFK=3
        startdatetime=datetime(2013, 10, 27, 16, 0)
        enddatetime=datetime(2013, 10, 27, 17, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift22:
        eventFK=3
        startdatetime=datetime(2013, 10, 27, 17, 0)
        enddatetime=datetime(2013, 10, 27, 18, 0)
        location='Booth A'
        minWorkers=3
        maxWorkers=4

    class shift23:
        eventFK=4
        startdatetime=datetime(2013, 3, 9, 16, 0)
        enddatetime=datetime(2013, 3, 9, 17, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift24:
        eventFK=4
        startdatetime=datetime(2013, 3, 9, 17, 0)
        enddatetime=datetime(2013, 3, 9, 18, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift25:
        eventFK=4
        startdatetime=datetime(2013, 3, 9, 18, 0)
        enddatetime=datetime(2013, 3, 9, 19, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift26:
        eventFK=4
        startdatetime=datetime(2013, 3, 9, 19, 0)
        enddatetime=datetime(2013, 3, 9, 20, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift27:
        eventFK=4
        startdatetime=datetime(2013, 3, 10, 16, 0)
        enddatetime=datetime(2013, 3, 10, 17, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift28:
        eventFK=4
        startdatetime=datetime(2013, 3, 10, 17, 0)
        enddatetime=datetime(2013, 3, 10, 18, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift29:
        eventFK=4
        startdatetime=datetime(2013, 3, 10, 18, 0)
        enddatetime=datetime(2013, 3, 10, 19, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift30:
        eventFK=4
        startdatetime=datetime(2013, 3, 10, 19, 0)
        enddatetime=datetime(2013, 3, 10, 20, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift31:
        eventFK=4
        startdatetime=datetime(2013, 3, 11, 16, 0)
        enddatetime=datetime(2013, 3, 11, 17, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift32:
        eventFK=4
        startdatetime=datetime(2013, 3, 11, 17, 0)
        enddatetime=datetime(2013, 3, 11, 18, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift33:
        eventFK=4
        startdatetime=datetime(2013, 3, 11, 18, 0)
        enddatetime=datetime(2013, 3, 11, 19, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift34:
        eventFK=4
        startdatetime=datetime(2013, 3, 11, 19, 0)
        enddatetime=datetime(2013, 3, 11, 20, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift35:
        eventFK=4
        startdatetime=datetime(2013, 3, 12, 16, 0)
        enddatetime=datetime(2013, 3, 12, 17, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift36:
        eventFK=4
        startdatetime=datetime(2013, 3, 12, 17, 0)
        enddatetime=datetime(2013, 3, 12, 18, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift37:
        eventFK=4
        startdatetime=datetime(2013, 3, 12, 18, 0)
        enddatetime=datetime(2013, 3, 12, 19, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

    class shift38:
        eventFK=4
        startdatetime=datetime(2013, 3, 12, 19, 0)
        enddatetime=datetime(2013, 3, 12, 20, 0)
        location='Topfer Theatre'
        minWorkers=3
        maxWorkers=4

        
class ShiftPersonData(DataSet):
    class shiftperson01:
        shiftFK=1
        personFK=3
        
    class shiftperson02:
        shiftFK=1
        personFK=4
        
    class shiftperson03:
        shiftFK=2
        personFK=4
        
    class shiftperson04:
        shiftFK=2
        personFK=5
        
    class shiftperson05:
        shiftFK=3
        personFK=3
        
    class shiftperson06:
        shiftFK=3
        personFK=5
        
    class shiftperson07:
        shiftFK=4
        personFK=3
        
    class shiftperson08:
        shiftFK=4
        personFK=4
        
    class shiftperson09:
        shiftFK=4
        personFK=5
        

all_data = (EntityData, PersonData, AddressData, OrganizationData, ContactData,
            PrivilegeData, MemberData, PrivilegePersonAssignmentData,
            GlobalPrivilegeAssignmentData, EventData, ShiftData, ShiftPersonData)
entity_test_data = (EntityData, AddressData, ContactData, OrganizationData, PersonData)
address_test_data = (AddressData, EntityData)
contact_test_data = (ContactData, EntityData)
organization_test_data = (OrganizationData, EntityData, MemberData, EventData)
person_test_data = (PersonData, EntityData, MemberData, GlobalPrivilegeAssignmentData)
member_test_data = (MemberData, PersonData, OrganizationData, PrivilegePersonAssignmentData)
privilege_test_data = (PrivilegeData, PrivilegePersonAssignmentData, GlobalPrivilegeAssignmentData, MemberData, PersonData, OrganizationData)
ppa_test_data = (PrivilegeData, PrivilegePersonAssignmentData, MemberData)
gpa_test_data = (PrivilegeData, GlobalPrivilegeAssignmentData, MemberData, PersonData)
event_test_data = (EventData, OrganizationData, ShiftData)
shift_test_data = (ShiftData, EventData, ShiftPersonData, EntityData, PersonData, OrganizationData)
