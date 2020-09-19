'''
Test the Operators operations


Use the operator_fixture to have data to retrieve, it generates three operators
'''
from unittest.mock import ANY
import http.client
from freezegun import freeze_time
from .constants import PRIVATE_KEY
from operators_backend import token_validation
from faker import Faker
fake = Faker()


@freeze_time('2019-05-07 13:47:34')
def test_create_me_operator(client):
    new_operator = {
        'username': fake.name(),
        'officeAddress': fake.text(240),
        'usernameMain': fake.text(240),
        'email': fake.text(240),
        'status': fake.text(240),
        'pin': fake.text(240),
        'contactName': fake.text(240),
        'contactPhoneNo': fake.text(240),
        'contactEmail': fake.text(240),
        'name': fake.text(240),
        'phoneNo': fake.text(240),
        'numberOfVehicle': fake.text(240),
    }
    header = token_validation.generate_token_header(fake.name(),
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/operators/', data=new_operator,
                           headers=headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    expected = {
        'id': ANY,
        'username': ANY,
        'officeAddress': new_operator['officeAddress'],
        'email': new_operator['email'],
        'status': new_operator['status'],
        'usernameMain': new_operator['usernameMain'],
        'pin': new_operator['pin'],
        'contactName': new_operator['contactName'],
        'contactPhoneNo': new_operator['contactPhoneNo'],
        'contactEmail': new_operator['contactEmail'],
        'name': new_operator['name'],
        'phoneNo': new_operator['phoneNo'],
        'numberOfVehicle': new_operator['numberOfVehicle'],
        'statusTimestamp': ANY,
        'timestamp': '2019-05-07T13:47:34',
    }
    assert result == expected


def test_create_me_unauthorized(client):
    new_operator = {
        'username': fake.name(),
        'officeAddress': fake.text(240),
        'usernameMain': fake.text(240),
        'email': fake.text(240),
        'status': fake.text(240),
        'pin': fake.text(240),
        'contactName': fake.text(240),
        'contactPhoneNo': fake.text(240),
        'contactEmail': fake.text(240),
        'name': fake.text(240),
        'phoneNo': fake.text(240),
        'numberOfVehicle': fake.text(240),
    }
    response = client.post('/api/me/operators/', data=new_operator)
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_me_unauthorized(client):
    response = client.get('/api/me/operators/')
    assert http.client.UNAUTHORIZED == response.status_code


def test_get_non_existing_operator(client, operator_fixture):
    operator_id = 123456
    response = client.get(f'/api/operators/{operator_id}/')

    assert http.client.NOT_FOUND == response.status_code
