from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db=SQLAlchemy()

class Admin(db.Model,UserMixin):
    __tablename__="admin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String,unique=True)
    password=db.Column(db.String)
    def get_id(self):
        return self.email

class Services(db.Model):
    __tablename__="services"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String,unique=True)
    baseprice=db.Column(db.Integer)
    description=db.Column(db.String)
    Sproviders=db.relationship("ServiceProvider", backref="service")

class ServiceProvider(db.Model,UserMixin):
    __tablename__='serviceprovider'

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String)
    city=db.Column(db.String)
    email=db.Column(db.String,unique=True, nullable=False)
    password=db.Column(db.String)
    exp=db.Column(db.Integer)
    phone=db.Column(db.String)
    status=db.Column(db.String)
    servicename= db.Column(db.String, db.ForeignKey("services.name"))
    receive_request=db.relationship("Request",backref="service", cascade="all, delete-orphan")
    avail_slots=db.relationship("ProvidersAvailability",backref="servprovider",cascade="all, delete-orphan")
    def get_id(self):
        return self.email


class Customer(db.Model,UserMixin):
    __tablename__='customer'

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String)
    city=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    password=db.Column(db.String)
    exp=db.Column(db.Integer)
    phone=db.Column(db.String)
    status=db.Column(db.String)
    sent_request=db.relationship("Request", backref="cust")
    def get_id(self):
        return self.email


class Request(db.Model):
    __tablename__="request"

    r_id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    sp_id=db.Column(db.Integer, db.ForeignKey("serviceprovider.id"),nullable=False)
    c_id=db.Column(db.Integer, db.ForeignKey("customer.id"),nullable=False)
    r_date=db.Column(db.Date)
    start_time=db.Column(db.Time)
    end_time=db.Column(db.Time)
    r_status=db.Column(db.String) # booked cancelled complete
    slot_id=db.Column(db.Integer,db.ForeignKey("providersavailability.id"),unique=True)



class ProvidersAvailability(db.Model):
    __tablename__="providersavailability"

    id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    sp_id=db.Column(db.Integer, db.ForeignKey("serviceprovider.id"),nullable=False)
    date=db.Column(db.Date,nullable=False)
    start_time=db.Column(db.Time,nullable=False)
    end_time=db.Column(db.Time,nullable=False)
    status=db.Column(db.String,nullable=False) # available, booked





