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


def test_list_me_operators(client, operator_fixture):
    username = fake.name()
    officeAddress = fake.text(240)
    usernameMain = fake.text(240)
    email = fake.text(240)
    status = fake.text(240)
    pin = fake.text(240)
    contactName = fake.text(240)
    contactPhoneNo = fake.text(240)
    contactEmail = fake.text(240)
    name = fake.text(240)
    phoneNo = fake.text(240)
    numberOfVehicle = fake.text(240)

    # Create a new operator
    new_operator = {
        'officeAddress': officeAddress,
        'usernameMain': usernameMain,
        'email': email,
        'status': status,
        'pin': pin,
        'contactName': contactName,
        'contactPhoneNo': contactPhoneNo,
        'contactEmail': contactEmail,
        'name': name,
        'phoneNo': phoneNo,
        'numberOfVehicle': numberOfVehicle,
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/operators/', data=new_operator,
                           headers=headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    # Get the operators of the user
    response = client.get('/api/me/operators/', headers=headers)
    results = response.json

    assert http.client.OK == response.status_code
    assert len(results) == 1
    result = results[0]
    expected_result = {
        'id': ANY,
        'username': username,
        'officeAddress': officeAddress,
        'usernameMain': usernameMain,
        'email': email,
        'status': status,
        'pin': pin,
        'contactName': contactName,
        'contactPhoneNo': contactPhoneNo,
        'contactEmail': contactEmail,
        'name': name,
        'phoneNo': phoneNo,
        'numberOfVehicle': numberOfVehicle,
        'statusTimestamp': ANY,
        'timestamp': ANY,
    }
    assert result == expected_result


def test_list_me_unauthorized(client):
    response = client.get('/api/me/operators/')
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_operators(client, operator_fixture):
    response = client.get('/api/operators/')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the ids are increasing
    previous_id = -1
    for operator in result:
        expected = {
            'officeAddress': ANY,
            'usernameMain': ANY,
            'email': ANY,
            'status': ANY,
            'pin': ANY,
            'contactName': ANY,
            'contactPhoneNo': ANY,
            'contactEmail': ANY,
            'name': ANY,
            'phoneNo': ANY,
            'numberOfVehicle': ANY,
            'statusTimestamp': ANY,
            'username': ANY,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == operator
        assert operator['id'] > previous_id
        previous_id = operator['id']


def test_list_operators_search(client, operator_fixture):
    username = fake.name()
    officeAddress = fake.text(240)
    usernameMain = fake.text(240)
    email = fake.text(240)
    status = fake.text(240)
    pin = fake.text(240)
    contactName = fake.text(240)
    contactPhoneNo = fake.text(240)
    contactEmail = fake.text(240)
    name = 'platypus'
    phoneNo = fake.text(240)
    numberOfVehicle = fake.text(240)
    new_operator = {
        'officeAddress': officeAddress,
        'usernameMain': usernameMain,
        'email': email,
        'status': status,
        'pin': pin,
        'contactName': contactName,
        'contactPhoneNo': contactPhoneNo,
        'contactEmail': contactEmail,
        'name': name,
        'phoneNo': phoneNo,
        'numberOfVehicle': numberOfVehicle,
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/me/operators/', data=new_operator,
                           headers=headers)
    assert http.client.CREATED == response.status_code

    response = client.get('/api/operators/?search=platypus')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the returned values contain "platypus"
    for operator in result:
        expected = {
            'officeAddress': ANY,
            'usernameMain': usernameMain,
            'email': ANY,
            'status': ANY,
            'pin': ANY,
            'contactName': contactName,
            'contactPhoneNo': contactPhoneNo,
            'contactEmail': contactEmail,
            'name': ANY,
            'phoneNo': ANY,
            'numberOfVehicle': ANY,
            'statusTimestamp': ANY,
            'username': username,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == operator
        assert 'platypus' in operator['name'].lower()


def test_get_operator(client, operator_fixture):
    operator_id = operator_fixture[0]
    response = client.get(f'/api/operators/{operator_id}/')
    result = response.json

    assert http.client.OK == response.status_code
    assert 'officeAddress' in result
    assert 'usernameMain' in result
    assert 'email' in result
    assert 'status' in result
    assert 'pin' in result
    assert 'contactName' in result
    assert 'contactPhoneNo' in result
    assert 'contactEmail' in result
    assert 'name' in result
    assert 'phoneNo' in result
    assert 'numberOfVehicle' in result
    assert 'username' in result
    assert 'statusTimestamp' in result
    assert 'timestamp' in result
    assert 'id' in result


def test_get_non_existing_operator(client, operator_fixture):
    operator_id = 123456
    response = client.get(f'/api/operators/{operator_id}/')

    assert http.client.NOT_FOUND == response.status_code
