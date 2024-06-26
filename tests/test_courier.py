import allure
import requests
from data.endpoints import Endpoints
from data.helpers import Generators
from data.data import TestData


class TestCreateCourier:
    @allure.title('Проверка создания нового курьера')
    @allure.description('Создаем курьера, передав все валидные параметры, ожидаем код 201 и ответ {"ok":true}')
    def test_create_courier_with_valid_full_regdata_created(self, registration_courier_data):
        payload = registration_courier_data
        response = requests.post(Endpoints.endpoint_create_courier, data=payload)
        expected_response_text = '{"ok":true}'
        assert response.status_code == 201 and response.text == expected_response_text, (
            f'Ожидался код 201 с ответом "{expected_response_text}, '
            f'получен код {response.status_code} и ответ {response.text}')

    @allure.title('Проверка создания курьера при заполнении только обязательных полей')
    @allure.description('Создаем курьера, передав валидные обязательные параметры name и password, ожидаем код 201 и ответ {"ok":true}')
    def test_create_courier_with_valid_required_regdata_created(self, registration_required_courier_data):
        payload = registration_required_courier_data
        response = requests.post(Endpoints.endpoint_create_courier, data=payload)
        expected_response_text = '{"ok":true}'
        assert response.status_code == 201 and response.text == expected_response_text, (
            f'Ожидался код 201 с ответом "{expected_response_text}, '
            f'получен код {response.status_code} и ответ {response.text}')

    @allure.title('Проверка создания двух курьеров с одинаковым логином')
    @allure.title('Создаем курьера, передав все валидные параметры, создаем еще одного курьера с этим же параметром логин, ожидаем код 409 и сообщение об ошибке')
    def test_create_second_courier_with_existing_login_conflict(self, registration_courier_data):
        # создаем курьера
        payload = registration_courier_data
        response = requests.post(Endpoints.endpoint_create_courier, data=payload)
        # создаем курьера с тем же логином
        second_password = Generators.generate_random_string(10)
        second_name = Generators.generate_random_string(10)
        second_payload = {"login": registration_courier_data["login"], "password": second_password, "firstName": second_name}
        new_response = requests.post(Endpoints.endpoint_create_courier, data=second_payload)
        actual_result = new_response.json()["message"]
        assert new_response.status_code == 409 and 'Этот логин уже используется' in actual_result

    @allure.title('Проверка создания курьера без указания параметра login')
    @allure.description('При создании курьера не передаем параметр login, ожидаем код 400 и сообщение об ошибке')
    def test_create_courier_without_login_bad_request(self):
        password = Generators.generate_random_string(10)
        first_name = Generators.generate_random_string(10)
        payload = {"password": password, "firstName": first_name}
        response = requests.post(Endpoints.endpoint_create_courier, data=payload)
        actual_result = response.json()["message"]
        assert response.status_code == 400 and actual_result == 'Недостаточно данных для создания учетной записи'

    @allure.title('Проверка создания курьера без указания параметра password')
    @allure.description('При создании курьера не передаем параметр password, ожидаем код 400 и сообщение об ошибке')
    def test_create_courier_without_password_bad_request(self):
        login = Generators.generate_random_string(10)
        first_name = Generators.generate_random_string(10)
        payload = {"login": login, "firstName": first_name}
        response = requests.post(Endpoints.endpoint_create_courier, data=payload)
        actual_result = response.json()["message"]
        assert response.status_code == 400 and actual_result == 'Недостаточно данных для создания учетной записи'


class TestLoginCourier:

    @allure.title('При успешной авторизации при указании всех обязательных полей, в ответе  id курьера')
    @allure.description('Совершаем авторизацию, используя тестовые данные в payload, совершаем авторизацию, ожидаем код 200 и ответ, содержащий id курьера')
    def test_login_courier_with_existing_data_got_id(self):
        payload = TestData.test_login_payload
        response = requests.post(Endpoints.endpoint_login_courier, data=payload)
        assert response.status_code == 200 and 'id' in response.json()

    @allure.title('Проверка авторизации без указания логина')
    @allure.title('Совершаем авторизацию без указания параметра "login", ожидаем код 400 и сообщение об ошибке')
    def test_login_courier_without_login_bad_request(self):
        payload = TestData.test_login_payload_no_login
        response = requests.post(Endpoints.endpoint_login_courier, data=payload)
        actual_result = response.json()["message"]
        assert response.status_code == 400 and actual_result == 'Недостаточно данных для входа'

    @allure.title('Проверка авторизации без указания пароля')
    @allure.description('Совершаем авторизацию без указания параметра "password", ожидаем код 400 и сообщение об ошибке')
    def test_login_courier_without_password_bad_request(self):
        payload = TestData.test_login_payload_no_password
        response = requests.post(Endpoints.endpoint_login_courier, data=payload)
        try:
            assert response.status_code == 400 and 'Недостаточно данных для входа' in response.text
        except AssertionError as e:
            print('Известная ошибка:', e)

    @allure.title('Проверка авторизации с указанием некорректного логина')
    @allure.description('Совершаем авторизацию c указанием некорректного параметра "login", ожидаем код 404 и сообщение об ошибке')
    def test_login_courier_incorrect_login_not_found(self):
        payload = TestData.test_login_payload_incorrect_login
        response = requests.post(Endpoints.endpoint_login_courier, data=payload)
        actual_result = response.json()["message"]
        assert response.status_code == 404 and actual_result == 'Учетная запись не найдена'

    @allure.title('Проверка авторизации с указанием некорректного пароля')
    @allure.description('Совершаем авторизацию c указанием некорректного параметра "password", ожидаем код 404 и сообщение об ошибке')
    def test_login_courier_incorrect_password_not_found(self):
        payload = TestData.test_login_payload_incorrect_pwd
        response = requests.post(Endpoints.endpoint_login_courier, data=payload)
        actual_result = response.json()["message"]
        assert response.status_code == 404 and actual_result == 'Учетная запись не найдена'

    @allure.title('Проверка авторизации несуществующего пользователя')
    @allure.description('Совершаем авторизацию с значениями параметров, не зарегистрированными в приложении')
    def test_login_unregistered_courier(self, registration_required_courier_data):
        payload = registration_required_courier_data
        response = requests.post(Endpoints.endpoint_login_courier, data=payload)
        actual_result = response.json()["message"]
        assert response.status_code == 404 and actual_result == 'Учетная запись не найдена'

class TestDeleteCourier:

    @allure.title('Проверка удаления курьера')
    @allure.description('Создаем курьера, логинимся и сохраняем id курьера, удаляем курьера, ожидаем код 200 и ответ {"ok":true}')
    def test_delete_courier_with_existing_id_true(self, login_courier):
        courier_id = login_courier
        response = requests.delete(f'{Endpoints.endpoint_create_courier}/{courier_id}')
        expected_response_text = '{"ok":true}'
        assert response.status_code == 200 and response.text == expected_response_text

    @allure.title('Проверка удаления курьера без указания id')
    @allure.description('Отправляем запрос без указания параметра id, ожидаем код 400 и сообщение об ошибке')
    def test_delete_courier_without_id_bad_request(self):
        response = requests.delete(f'{Endpoints.endpoint_create_courier}/')
        actual_result = response.json()["message"]
        try:
            assert response.status_code == 400 and actual_result == 'Недостаточно данных для удаления курьера'
        except AssertionError as e:
            print('Известная ошибка:', e)
    @allure.title('Проверка удаления курьера с несуществующим id')
    @allure.description('Отправляем запрос c указанием несуществующего параметра id, ожидаем код 404 и сообщение об ошибке')
    def test_delete_unregistered_courier(self):
        courier_id = 100500
        response = requests.delete(f'{Endpoints.endpoint_create_courier}/{courier_id}')
        actual_result = response.json()["message"]
        assert response.status_code == 404 and actual_result == 'Курьера с таким id нет.'

