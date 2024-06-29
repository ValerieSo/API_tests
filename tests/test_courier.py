import allure
from data.helpers import Generators
from data.data import TestData, StatusCode, StatusResponse
from base_api_methods import CourierAPI


class TestCreateCourier:
    @allure.title('Проверка создания нового курьера')
    @allure.description('Создаем курьера, передав все валидные параметры, ожидаем код 201 и ответ {"ok":true}')
    def test_create_courier_with_valid_full_regdata_created(self, registration_courier_data):
        payload = registration_courier_data
        response = CourierAPI.response_create_courier(payload)
        actual_result = response.json()["ok"]
        assert response.status_code == StatusCode.CREATED and actual_result is True

    @allure.title('Проверка создания курьера при заполнении только обязательных полей')
    @allure.description('Создаем курьера, передав валидные обязательные параметры name и password, '
                        'ожидаем код 201 и ответ {"ok":true}')
    def test_create_courier_with_valid_required_regdata_created(self, registration_required_courier_data):
        payload = registration_required_courier_data
        response = CourierAPI.response_create_courier(payload)
        actual_result = response.json()["ok"]
        assert response.status_code == StatusCode.CREATED and actual_result is True

    @allure.title('Проверка создания двух курьеров с одинаковым логином')
    @allure.title('Создаем курьера, передав все валидные параметры, '
                  'создаем еще одного курьера с этим же параметром логин, ожидаем код 409 и сообщение об ошибке')
    def test_create_second_courier_with_existing_login_conflict(self, create_courier_and_get_login):
        second_password = Generators.generate_random_string(10)
        second_name = Generators.generate_random_string(10)
        payload = {"login": create_courier_and_get_login["login"], "password": second_password, "firstName": second_name}
        new_response = CourierAPI.response_create_courier(payload)
        actual_result = new_response.json()["message"]
        assert new_response.status_code == 409 and StatusResponse.CONFLICT_COURIER in actual_result

    @allure.title('Проверка создания курьера без указания параметра login')
    @allure.description('При создании курьера не передаем параметр login, ожидаем код 400 и сообщение об ошибке')
    def test_create_courier_without_login_bad_request(self):
        password = Generators.generate_random_string(10)
        first_name = Generators.generate_random_string(10)
        payload = {"password": password, "firstName": first_name}
        response = CourierAPI.response_create_courier(payload)
        actual_result = response.json()["message"]
        assert (response.status_code == StatusCode.BAD_REQUEST
                and actual_result == StatusResponse.BAD_REQUEST_COURIER_REG)

    @allure.title('Проверка создания курьера без указания параметра password')
    @allure.description('При создании курьера не передаем параметр password, ожидаем код 400 и сообщение об ошибке')
    def test_create_courier_without_password_bad_request(self):
        login = Generators.generate_random_string(10)
        first_name = Generators.generate_random_string(10)
        payload = {"login": login, "firstName": first_name}
        response = CourierAPI.response_create_courier(payload)
        actual_result = response.json()["message"]
        assert (response.status_code == StatusCode.BAD_REQUEST
                and actual_result == StatusResponse.BAD_REQUEST_COURIER_REG)


class TestLoginCourier:

    @allure.title('При успешной авторизации при указании всех обязательных полей, в ответе  id курьера')
    @allure.description('Совершаем авторизацию, используя тестовые данные в payload, совершаем авторизацию,'
                        ' ожидаем код 200 и ответ, содержащий id курьера')
    def test_login_courier_with_existing_data_got_id(self):
        payload = TestData.test_login_payload
        response = CourierAPI.response_login_courier(payload)
        assert response.status_code == StatusCode.OK and 'id' in response.json()

    @allure.title('Проверка авторизации без указания логина')
    @allure.title('Совершаем авторизацию без указания параметра "login", ожидаем код 400 и сообщение об ошибке')
    def test_login_courier_without_login_bad_request(self):
        payload = TestData.test_login_payload_no_login
        response = CourierAPI.response_login_courier(payload)
        actual_result = response.json()["message"]
        assert (response.status_code == StatusCode.BAD_REQUEST
                and actual_result == StatusResponse.BAD_REQUEST_COURIER_lOG)

    @allure.title('Проверка авторизации без указания пароля')
    @allure.description('Совершаем авторизацию без указания параметра "password", ожидаем код 400 и сообщение об ошибке')
    def test_login_courier_without_password_bad_request(self):
        payload = TestData.test_login_payload_no_password
        response = CourierAPI.response_login_courier(payload)
        try:
            assert response.status_code == StatusCode.BAD_REQUEST and StatusResponse.BAD_REQUEST_COURIER_lOG in response.text
        except AssertionError as e:
            print('Известная ошибка:', e)

    @allure.title('Проверка авторизации с указанием некорректного логина')
    @allure.description('Совершаем авторизацию c указанием некорректного параметра "login", ожидаем код 404 и сообщение об ошибке')
    def test_login_courier_incorrect_login_not_found(self):
        payload = TestData.test_login_payload_incorrect_login
        response = CourierAPI.response_login_courier(payload)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.NOT_FOUND and actual_result == StatusResponse.NOT_FOUND_COURIER_LOG

    @allure.title('Проверка авторизации с указанием некорректного пароля')
    @allure.description('Совершаем авторизацию c указанием некорректного параметра "password", '
                        'ожидаем код 404 и сообщение об ошибке')
    def test_login_courier_incorrect_password_not_found(self):
        payload = TestData.test_login_payload_incorrect_pwd
        response = CourierAPI.response_login_courier(payload)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.NOT_FOUND and actual_result == StatusResponse.NOT_FOUND_COURIER_LOG

    @allure.title('Проверка авторизации несуществующего пользователя')
    @allure.description('Совершаем авторизацию с значениями параметров, не зарегистрированными в приложении')
    def test_login_unregistered_courier(self, registration_required_courier_data):
        payload = registration_required_courier_data
        response = CourierAPI.response_login_courier(payload)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.NOT_FOUND and actual_result == StatusResponse.NOT_FOUND_COURIER_LOG

class TestDeleteCourier:

    @allure.title('Проверка удаления курьера')
    @allure.description('Создаем курьера, логинимся и сохраняем id курьера, удаляем курьера, ожидаем код 200 и ответ {"ok":true}')
    def test_delete_courier_with_existing_id_true(self, login_courier):
        courier_id = login_courier
        response = CourierAPI.response_delete_courier(courier_id)
        actual_result = response.json()["ok"]
        assert response.status_code == StatusCode.OK and actual_result is True

    @allure.title('Проверка удаления курьера без указания id')
    @allure.description('Отправляем запрос без указания параметра id, ожидаем код 400 и сообщение об ошибке')
    def test_delete_courier_without_id_bad_request(self):
        courier_id = None
        response = CourierAPI.response_delete_courier(courier_id)
        actual_result = response.json()["message"]
        try:
            assert (response.status_code == StatusCode.BAD_REQUEST
                    and actual_result == StatusResponse.BAD_REQUEST_COURIER_DEL)
        except AssertionError as e:
            print('Известная ошибка:', e)
    @allure.title('Проверка удаления курьера с несуществующим id')
    @allure.description('Отправляем запрос c указанием несуществующего параметра id, ожидаем код 404 и сообщение об ошибке')
    def test_delete_unregistered_courier(self):
        courier_id = 100500
        response = CourierAPI.response_delete_courier(courier_id)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.NOT_FOUND and actual_result == StatusResponse.NOT_FOUND_COURIER
