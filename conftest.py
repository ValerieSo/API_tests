import pytest
import requests
import json
from data.helpers import Generators
from data.endpoints import Endpoints
from data.data import TestData


@pytest.fixture(scope='function')
def registration_courier_data():
    login = Generators.generate_random_string(10)
    password = Generators.generate_random_string(10)
    first_name = Generators.generate_random_string(10)
    return {"login": login, "password": password, "firstName": first_name}


@pytest.fixture(scope='function')
def registration_required_courier_data():
    login = Generators.generate_random_string(10)
    password = Generators.generate_random_string(10)
    return {"login": login, "password": password}


@pytest.fixture(scope='function')
def create_courier(registration_courier_data):
    payload = registration_courier_data
    response = requests.post(Endpoints.endpoint_create_courier, data=payload)
    del payload['firstName']
    return payload


@pytest.fixture(scope='function')
def login_courier(create_courier):
    payload = create_courier
    response = requests.post(Endpoints.endpoint_login_courier, data=payload)
    courier_id = response.json()['id']
    return courier_id

@pytest.fixture(scope='function')
def login_test_courier():
    payload = TestData.test_login_payload
    response = requests.post(Endpoints.endpoint_login_courier, data=payload)
    courier_id = response.json()['id']
    return courier_id

@pytest.fixture(scope='function')
def create_order():
    payload = TestData.test_order_data
    json_payload = json.dumps(payload)
    response = requests.post(Endpoints.endpoint_make_order, data=json_payload)
    track_number = response.json()['track']
    return track_number

@pytest.fixture(scope='function')
def get_orders_id(create_order):
    track_number = create_order
    payload = {'t': track_number}
    response = requests.get(Endpoints.endpoint_get_orders_id_by_track, params=payload)
    order_id = response.json()['order']['id']
    return order_id
