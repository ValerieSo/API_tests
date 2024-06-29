class Endpoints:
    URL = 'http://qa-scooter.praktikum-services.ru/'
    # ручка создание курьера
    ENDPOINT_CREATE_COURIER = f'{URL}api/v1/courier'
    # ручка логин курьера
    ENDPOINT_LOGIN_COURIER = f'{URL}api/v1/courier/login'
    # ручка создание заказа
    ENDPOINT_MAKE_ORDER = f'{URL}api/v1/orders'
    # ручка получения заказа по его номеру
    ENDPOINT_GET_ORDERS_ID_BY_TRACK = f'{URL}api/v1/orders/track'
    # ручка принятия заказа
    ENDPOINT_ACCEPT_ORDER = f'{URL}api/v1/orders/accept/'