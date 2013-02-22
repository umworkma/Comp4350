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

    class person02:
        entityFK = 4
        firstname = 'Ryoji'
        lastname = 'Betchaku'

    class person04:
        entityFK = 5
        firstname = 'Dan'
        lastname = 'Nelson'

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

all_data = (EntityData, AddressData, OrganizationData, ContactData, PersonData,)
