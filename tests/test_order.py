import allure
import pytest
import json
from data.data import TestData, StatusCode, StatusResponse
from base_api_methods import OrderAPI


class TestOrder:

    @allure.title('При успешном создании заказа, тело ответа содержит номер отслеживания')
    @allure.description('Создаем заказ, используя параметризацию для проверки возможности выбора '
                        'цвета "BLACK", цвета "GREY", обоих цветов и без указания цвета, ожидаем код 201 и ответ,'
                        'содержащий номер заказа')
    @pytest.mark.parametrize('color', [["BLACK", "GREY"], None, ["BLACK"], ["GREY"]])
    def test_create_order_color_options_got_track_number(self, color):
        payload = TestData.test_order_data
        payload["color"] = color
        json_payload = json.dumps(payload)
        response = OrderAPI.response_create_order(json_payload)
        assert response.status_code == StatusCode.CREATED and 'track' in response.json()

    @allure.title('Можно запросить список заказов')
    @allure.description('Отправляем запрос без каких-либо параметров, ожидаем код 200 и список заказов')
    def test_get_orders_list_all_got_orders(self):
        response = OrderAPI.response_get_orders_list()
        assert response.status_code == StatusCode.OK and "orders" in response.json()

    def test_accept_order_with_existing_courier_and_order_ok(self, login_test_courier, get_orders_id):
        order_id = get_orders_id
        courier_id = login_test_courier
        payload = {'courierId': courier_id}
        response = OrderAPI.response_accept_order(order_id, payload)
        actual_result = response.json()["ok"]
        assert response.status_code == StatusCode.OK and actual_result is True

    @allure.title('Нельзя принять заказ без указания параметра courierId')
    @allure.description(
        'Создаем заказ, принимаем заказ, не указывая параметр courierId, ожидаем код 400 и сообщение об ошибке')
    def test_accept_order_without_courier_id_conflict(self, get_orders_id):
        order_id = get_orders_id
        payload = None
        response = OrderAPI.response_accept_order(order_id, payload)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.BAD_REQUEST and actual_result == StatusResponse.BAD_REQUEST_ORDER

    @allure.title('Нельзя принять заказ, указав несуществующий параметр courierId')
    @allure.description(
        'Создаем заказ, принимаем заказ, указав несуществующий параметр courierId, ожидаем код 404 и сообщение об ошибке')
    def test_accept_order_unregistered_courier_not_found(self, get_orders_id):
        order_id = get_orders_id
        courier_id = 100500100
        payload = {"courierId": courier_id}
        response = OrderAPI.response_accept_order(order_id, payload)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.NOT_FOUND and actual_result == StatusResponse.NOT_FOUND_COURIER_IN_ACCEPT_ORDER

    @allure.title('Нельзя принять заказ без указания параметра номер заказа')
    @allure.description(
        'Авторизуем курьера, принимаем заказ, не указывая параметр номер заказа, ожидаем код 400 и сообщение об ошибке')
    def test_accept_order_without_orders_id_bad_request(self, login_test_courier):
        order_id = None
        courier_id = login_test_courier
        payload = {"courierId": courier_id}
        response = OrderAPI.response_accept_order(order_id, payload)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.BAD_REQUEST and actual_result == StatusResponse.BAD_REQUEST_ORDER

    @allure.title('Нельзя принять заказ, указав несуществующий параметр номер заказа')
    @allure.description(
        'Авторизуем курьера, принимаем заказ, указав несуществующий параметр номер заказа, ожидаем код 404 и сообщение об ошибке')
    def test_accept_order_without_orders_id_bad_request(self, login_test_courier):
        order_id = 100500100
        courier_id = login_test_courier
        payload = {"courierId": courier_id}
        response = OrderAPI.response_accept_order(order_id, payload)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.NOT_FOUND and actual_result == StatusResponse.NOT_FOUND_ORDER

    @allure.title('При успешном получении заказа по номеру отслеживания, в ответе отображается объект с заказом')
    @allure.description(
        'Создаем заказ, запрашиваем заказ, указав  существующий параметр t, ожидаем код 200 и объект с заказом в ответе')
    def test_get_order_by_existing_track_order(self, create_order):
        track_number = create_order
        payload = {'t': track_number}
        response = OrderAPI.response_get_order_by_track(payload)
        assert response.status_code == StatusCode.OK and 'order' in response.json()

    @allure.title('Нельзя получить заказ без указания номера отслеживания')
    @allure.description('Запрашиваем заказ, не указывая параметр t, ожидаем код 400 и сообщение об ошибке')
    def test_get_order_without_track_bad_request(self):
        payload = None
        response = OrderAPI.response_get_order_by_track(payload)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.BAD_REQUEST and actual_result == StatusResponse.BAD_REQUEST_ORDER

    @allure.title('Нельзя получить заказ по несуществующему номеру отслеживания')
    @allure.description(
        'Запрашиваем заказ, указывая в параметре t несуществующее значение, ожидаем код 404 и сообщение об ошибке')
    def test_get_order_nonexistent_track_not_found(self):
        track_number = 100500100
        payload = {'t': track_number}
        response = OrderAPI.response_get_order_by_track(payload)
        actual_result = response.json()["message"]
        assert response.status_code == StatusCode.NOT_FOUND and actual_result == StatusResponse.NOT_FOUND_TRACK_ORDER
