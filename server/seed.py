from app import app
from models import db, Apartment, Lease, Tenant
from faker import Faker

fake = Faker()

with app.app_context():

    Apartment.query.delete()
    Lease.query.delete()
    Tenant.query.delete()
    

    apartments = []
    apartments.append(Apartment(number = 12))
    apartments.append(Apartment(number = 14))
    apartments.append(Apartment(number = 1))
    apartments.append(Apartment(number = 2))
    db.session.add_all(apartments)

    tenants = []
    tenants.append(Tenant(name=fake.name(), age=fake.random_int(min=18, max=80, step=1)))
    tenants.append(Tenant(name=fake.name(), age=fake.random_int(min=18, max=80, step=1)))
    tenants.append(Tenant(name=fake.name(), age=fake.random_int(min=18, max=80, step=1)))
    tenants.append(Tenant(name=fake.name(), age=fake.random_int(min=18, max=80, step=1)))
    db.session.add_all(tenants)

    leases = []
    leases.append(Lease(rent="130", apartment_id=1,tenant_id=1))
    leases.append(Lease(rent="280", apartment_id=2,tenant_id=2))
    leases.append(Lease(rent="1130", apartment_id=3,tenant_id=3))
    leases.append(Lease(rent="1300", apartment_id=4,tenant_id=4))

    db.session.add_all(leases)


    db.session.commit()