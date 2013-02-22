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

all_data = (EntityData, AddressData, OrganizationData, ContactData,)
