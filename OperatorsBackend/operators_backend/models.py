from sqlalchemy import func
from operators_backend.db import db


class OperatorModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    usernameMain = db.Column(db.String(250))
    name = db.Column(db.String(250))
    contactName = db.Column(db.String(250))
    pin = db.Column(db.String(250))
    phoneNo = db.Column(db.String(250))
    email = db.Column(db.String(250))
    contactPhoneNo = db.Column(db.String(250))
    contactEmail = db.Column(db.String(250))
    officeAddress = db.Column(db.String(250))
    numberOfVehicle = db.Column(db.String(250))
    status = db.Column(db.String(250))
    moved = db.Column(db.Integer, default=0)
    statusTimestamp = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime, server_default=func.now())
