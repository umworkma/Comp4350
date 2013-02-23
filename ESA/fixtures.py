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
        personentityfk = 3
        organizationentityfk = 1

    class member02:
        personentityfk = 4
        organizationentityfk = 1

    class member03:
        personentityfk = 4
        organizationentityfk = 2

    class member04:
        personentityfk = 5
        organizationentityfk = 2
        

class EmpPrivilegeAssignmentData(DataSet):
    class empPrivilegeAssign01:
        privilegefk = 5
        personentityfk = 3
        organizationentityfk = 1

    class empPrivilegeAssign02:
        privilegefk = 6
        personentityfk = 3
        organizationentityfk = 1

    class empPrivilegeAssign03:
        privilegefk = 7
        personentityfk = 4
        organizationentityfk = 1

    class empPrivilegeAssign04:
        privilegefk = 8
        personentityfk = 4
        organizationentityfk = 2

    class empPrivilegeAssign05:
        privilegefk = 5
        personentityfk = 5
        organizationentityfk = 2

    class empPrivilegeAssign06:
        privilegefk = 6
        personentityfk = 5
        organizationentityfk = 2

class GlobalPrivilegeAssignmentData(DataSet):
    class globalPrivilegeAssign01:
        privilegefk = 1
        personentityfk = 3

    class globalPrivilegeAssign02:
        privilegefk = 4
        personentityfk = 3

    class globalPrivilegeAssign03:
        privilegefk = 3
        personentityfk = 4

    class globalPrivilegeAssign04:
        privilegefk = 4
        personentityfk = 4

    class globalPrivilegeAssign05:
        privilegefk = 2
        personentityfk = 5

    class globalPrivilegeAssign06:
        privilegefk = 4
        personentityfk = 5

all_data = (EntityData, AddressData, OrganizationData, ContactData, PrivilegeData, MemberData)
