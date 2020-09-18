from operators_backend.db import mongo
from datetime import datetime


class OperatorCollection(mongo.Document):

    """
    The Operator Collection

    """

    id = mongo.IntField(primary_key=True)
    username = mongo.StringField()
    usernameMain = mongo.StringField()
    name = mongo.StringField()
    contactName = mongo.StringField()
    pin = mongo.StringField()
    phoneNo = mongo.StringField()
    email = mongo.StringField()
    contactPhoneNo = mongo.StringField()
    contactEmail = mongo.StringField()
    officeAddress = mongo.StringField()
    numberOfVehicle = mongo.StringField()
    status = mongo.StringField()
    updated = mongo.IntField(default=0)
    statusTimestamp = mongo.DateTimeField()
    timestamp = mongo.DateTimeField(default=datetime.now())

    meta = {
        'ordering': ['+id']
    }
