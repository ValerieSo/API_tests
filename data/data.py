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