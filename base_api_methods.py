import allure
import requests
from data.endpoints import Endpoints


class CourierAPI:
    @staticmethod
    def response_create_courier(payload):
        response = requests.post(Endpoints.ENDPOINT_CREATE_COURIER, data=payload)
        return response

    @staticmethod
    def response_login_courier(payload):
        response = requests.post(Endpoints.ENDPOINT_LOGIN_COURIER, data=payload)
        return response

    @staticmethod
    def response_delete_courier(courier_id):
        response = requests.delete(f'{Endpoints.ENDPOINT_CREATE_COURIER}/{courier_id}')
        return response

class OrderAPI:
    @staticmethod
    def response_create_order(json_payload):
        response = requests.post(Endpoints.ENDPOINT_MAKE_ORDER, data=json_payload)
        return response

    @staticmethod
    def response_get_orders_list():
        response = requests.get(Endpoints.ENDPOINT_MAKE_ORDER)
        return response

    @staticmethod
    def response_accept_order(order_id, payload):
        response = requests.put(f'{Endpoints.ENDPOINT_ACCEPT_ORDER}{order_id}', params=payload)
        return response

    @staticmethod
    def response_get_order_by_track(payload):
        response = requests.get(Endpoints.ENDPOINT_GET_ORDERS_ID_BY_TRACK, params=payload)
        return response
