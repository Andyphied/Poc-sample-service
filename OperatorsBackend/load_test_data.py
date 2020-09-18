from operators_backend.app import create_app
from operators_backend.models import OperatorModel
from datetime import datetime

if __name__ == '__main__':
    application = create_app()
    application.app_context().push()

    # Create some test data
    test_data = [
        # username, timestamp, text
        ('bruce', datetime.now(), "k1G", "Karu", "1", "54",
         "Karu4", "A2J", "K4G", datetime.now(), 'test2', 'ken',
         '3344', 't@c.com'),
        ('bruce', datetime.now(), "K2G", "Karu2", "1", "12",
         "Karu4", "A2J", "K4G", datetime.now(), 'test2', 'ben',
         '3344', 'ts@c.com'),
        ('bruce', datetime.now(), "K3G", "Karu3", "0", "34",
         "Karu4", "A2J", "K4G", datetime.now(), 'test2', 'Wen',
         '3344', 'h@c.com'),
        ('stephen', datetime.now(), "K4G", "Karu4", "0", "122",
         "Karu4", "A2J", "K4G", datetime.now(), 'test2', 'Jen',
         '3344', 'w@c.com')
    ]
    for username, timestamp, phoneNo, email, status, pin,\
            name, numberOfVehicle, officeAddress, statusTimestamp,\
            usernameMain, contactName, contactPhoneNo, contactEmail,\
            in test_data:
        operator = OperatorModel(
            username=username, officeAddress=officeAddress,
            email=email, status=status, phoneNo=phoneNo,
            timestamp=timestamp, name=name, pin=pin,
            numberOfVehicle=numberOfVehicle,
            statusTimestamp=statusTimestamp, contactName=contactName,
            usernameMain=usernameMain, contactEmail=contactEmail,
            contactPhoneNo=contactPhoneNo,
            )
        application.db.session.add(operator)

    application.db.session.commit()
