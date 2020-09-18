import pytest
import http.client
from operators_backend.app import create_app
from .constants import PRIVATE_KEY
from operators_backend import token_validation
from faker import Faker
fake = Faker()


@pytest.fixture
def app():
    application = create_app()

    application.app_context().push()
    # Initialise the DB
    application.db.create_all()

    return application


@pytest.fixture
def operator_fixture(client):
    '''
    Generate three operators in the system.
    '''

    operator_ids = []
    for _ in range(3):
        operator = {
            'officeAddress': fake.text(240),
            'usernameMain': fake.text(240),
            'email': fake.text(240),
            'status': fake.text(240),
            'pin': fake.text(240),
            'name': fake.text(240),
            'contactName': fake.text(240),
            'contactPhoneNo': fake.text(240),
            'contactEmail': fake.text(240),
            'phoneNo': fake.text(240),
            'numberOfVehicle': fake.text(240),
        }
        header = token_validation.generate_token_header(fake.name(),
                                                        PRIVATE_KEY)
        headers = {
            'Authorization': header,
        }
        response = client.post('/api/me/operators/', data=operator,
                               headers=headers)
        assert http.client.CREATED == response.status_code
        result = response.json
        operator_ids.append(result['id'])

    yield operator_ids

    # Clean up all operators
    response = client.get('/api/operators/')
    operators = response.json
    for operator in operators:
        operator_id = operator['id']
        url = f'/admin/operators/{operator_id}/'
        response = client.delete(url)
        assert http.client.NO_CONTENT == response.status_code
