from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Apartment, Tenant, Lease

from models import db

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )

# for our get and post
# ALWAYS DO POST WITH MAIN GET, post should not be added when singing an item by id
@app.route('/apartments', methods=["GET","POST"])
def get_apartments():
    if request.method == "GET":
        apartment = [apartment.to_dict() for apartment in Apartment.query.all()]
        return make_response(apartment,   200  )
    elif request.method == "POST":
        json_dict = request.get_json()
        new_apartment = Apartment(
            number = json_dict.get("number"), 
        )
        db.session.add(new_apartment)
        db.session.commit()
        return new_apartment.to_dict(),201

@app.route('/apartments/<int:id>', methods=["GET", "PATCH", "DELETE"])
def apartment_by_id(id):
    apartment = Apartment.query.filter_by(id=id).first()
    if request.method == "GET":
        apartment_serialized = apartment.to_dict()
        return make_response ( apartment_serialized, 200  )
    elif request.method == "PATCH":
        json_dict = request.get_json()
        for attr in json_dict:
            setattr(apartment, attr, json_dict.get(attr))
        db.session.add(apartment)
        db.session.commit()
        return apartment.to_dict(),200
    elif request.method == "DELETE":
        db.session.delete(apartment)
        db.session.commit()
        return "", 200



@app.route('/tenants', methods=["GET","POST"])
def get_tenants():
    if request.method == "GET":
        tenant = [tenant.to_dict() for tenant in Tenant.query.all()]
        return make_response(tenant,   200  )

    elif request.method == "POST":
        json_dict = request.get_json()
        new_tenant = Tenant(
            name = json_dict.get("name"),
            age = json_dict.get("age")
            
        )
        db.session.add(new_tenant)
        db.session.commit()
        # this adds it to our table
        return new_tenant.to_dict(),201

@app.route('/tenants/<int:id>', methods=["GET","PATCH","DELETE"])
def tenant_by_id(id):
    tenant = Tenant.query.filter_by(id=id).first()
    if request.method == "GET":
        tenant_serialized = tenant.to_dict()
        return make_response ( tenant_serialized, 200)
    elif request.method == "PATCH":
        json_dict = request.get_json()
        for attr in json_dict:
            setattr(tenant, attr, json_dict.get(attr))
        db.session.add(tenant)
        db.session.commit()
        return tenant.to_dict(),200
    elif request.method == "DELETE":
        db.session.delete(tenant)
        db.session.commit()
        return "", 200

@app.route('/leases', methods=["POST"])
def lease():
    if request.method == "POST":
        json_dict = request.get_json()
        new_lease = Lease(
            rent = json_dict.get("rent"),
            apartment_id = json_dict.get("apartment_id"),
            tenant_id = json_dict.get("tenant_id")
        )
        db.session.add(new_lease)
        db.session.commit()
        # this adds it to our table
        return new_lease.to_dict(),201

@app.route('/lease/<int:id>', methods=["DELETE"])
def lease_by_id(id):
    lease = Lease.query.filter_by(id=id).first()
    if request.method == "DELETE":
        db.session.delete(lease)
        db.session.commit()
        return "", 200


if __name__ == '__main__':
    app.run( port = 5556, debug = True )