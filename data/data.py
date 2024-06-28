class TestData:

    test_login_payload = {
        "login": "daisy",
        "password": "zeitan"
    }

    test_login_payload_no_login = {"password": "zeitan"}

    test_login_payload_no_password = {"login": "daisy"}

    test_login_payload_incorrect_login = {
        "login": "incorrect",
        "password": "zeitan"
    }

    test_login_payload_incorrect_pwd = {
        "login": "daisy",
        "password": "incorrect"
    }

    test_order_data = {
        "firstName": "Harry",
        "lastName": "Potter",
        "address": "Hogwarts, 4 Privet Drive",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 2,
        "deliveryDate": "2024-06-30",
        "comment": "bring snack for Hegwig",
        "color": []
    }


class StatusCode:

    CREATED = 201
    CONFLICT = 409
    BAD_REQUEST = 400
    OK = 200
    NOT_FOUND = 404

class StatusResponse:
    CONFLICT_COURIER = 'Этот логин уже используется'
    BAD_REQUEST_COURIER_REG = 'Недостаточно данных для создания учетной записи'
    BAD_REQUEST_COURIER_lOG = 'Недостаточно данных для входа'
    BAD_REQUEST_COURIER_DEL = 'Недостаточно данных для удаления курьера'
    BAD_REQUEST_ORDER = 'Недостаточно данных для поиска'
    NOT_FOUND_COURIER_LOG = 'Учетная запись не найдена'
    NOT_FOUND_COURIER = 'Курьера с таким id нет.'
    NOT_FOUND_COURIER_IN_ACCEPT_ORDER = 'Курьера с таким id не существует'
    NOT_FOUND_ORDER = 'Заказа с таким id не существует'
    NOT_FOUND_TRACK_ORDER = 'Заказ не найден'
