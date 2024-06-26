class Endpoints:
    URL = 'http://qa-scooter.praktikum-services.ru/'
    # ручка создание курьера
    endpoint_create_courier = f'{URL}api/v1/courier'
    # ручка логин курьера
    endpoint_login_courier = f'{URL}api/v1/courier/login'
    # ручка создание заказа
    endpoint_make_order = f'{URL}api/v1/orders'
    # ручка получения заказа по его номеру
    endpoint_get_orders_id_by_track = f'{URL}api/v1/orders/track'
    # ручка принятия заказа
    endpoint_accept_order = f'{URL}api/v1/orders/accept/'