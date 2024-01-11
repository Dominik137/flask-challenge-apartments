from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy


db = SQLAlchemy()


# Since Apartment and tenant can live on their own they don't need to inheret foregin keys, we just have to build the relationship to connect it
# to lease which has the foregin keys to both, Lease is the "Join table"
class Apartment(db.Model, SerializerMixin):
    __tablename__ = "apartments"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
   
#rule of thumb, make sure to add serialize rule to each of the stand alone classes,
# always start with the join table which is leases!
    serialize_rules = ("-leases",)
    leases = db.relationship('Lease', back_populates='apartment')
    

class Tenant(db.Model, SerializerMixin):
    __tablename__ = "tenants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
   
    serialize_rules = ("-leases",)
    leases = db.relationship('Lease', back_populates="tenant")

    @validates('age')
    def validate_age(self, key, age):
        if age < 18:
            raise ValueError("Tenant must be at least 18 years old.")
        return age

class Lease(db.Model, SerializerMixin):
    __tablename__ = "leases"
    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.String)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    # Define reverse relationship
    apartment = db.relationship('Apartment', back_populates='leases')
    tenant = db.relationship('Tenant', back_populates="leases")



