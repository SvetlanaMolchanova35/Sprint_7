"""Конфигурация URL для API Яндекс Самокат"""

class Urls:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    # Эндпоинты курьера
    CREATE_COURIER = "/api/v1/courier"
    LOGIN_COURIER = "/api/v1/courier/login"
    DELETE_COURIER = "/api/v1/courier/{id}"
    
    # Эндпоинты заказов
    CREATE_ORDER = "/api/v1/orders"
    GET_ORDERS = "/api/v1/orders"
    GET_ORDER_BY_TRACK = "/api/v1/orders/track"
    ACCEPT_ORDER = "/api/v1/orders/accept/{id}"
    CANCEL_ORDER = "/api/v1/orders/cancel"