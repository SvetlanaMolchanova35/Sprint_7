import requests
import random
import string
import allure
import datetime
import pytest
from config.urls import Urls
from data.messages import Messages


class ScooterApi:
    def __init__(self):
        self.session = requests.Session()
    
    @allure.step("Генерация случайной строки")
    def generate_random_string(self, length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    @allure.step("Регистрация нового курьера")
    def register_new_courier(self):
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = self.session.post(
            Urls.BASE_URL + Urls.CREATE_COURIER,
            data=payload
        )
        
        return {
            "login": login,
            "password": password,
            "first_name": first_name,
            "response": response
        }
    
    @allure.step("Логин курьера")
    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        
        response = self.session.post(
            Urls.BASE_URL + Urls.LOGIN_COURIER,
            data=payload
        )
        
        return response
    
    @allure.step("Удаление курьера")
    def delete_courier(self, courier_id):
        response = self.session.delete(
            Urls.BASE_URL + Urls.DELETE_COURIER.format(id=courier_id)
        )
        
        return response
    
    @allure.step("Создание заказа")
    def create_order(self, order_data):
        response = self.session.post(
            Urls.BASE_URL + Urls.CREATE_ORDER,
            json=order_data
        )
        
        return response
    
    @allure.step("Получение списка заказов")
    def get_orders_list(self, params=None):
        response = self.session.get(
            Urls.BASE_URL + Urls.GET_ORDERS,
            params=params
        )
        
        return response
    
    @allure.step("Получение заказа по трек-номеру")
    def get_order_by_track(self, track):
        response = self.session.get(
            Urls.BASE_URL + Urls.GET_ORDER_BY_TRACK,
            params={"t": track}
        )
        
        return response
    
    @allure.step("Принятие заказа курьером")
    def accept_order(self, order_id, courier_id):
        response = self.session.put(
            Urls.BASE_URL + Urls.ACCEPT_ORDER.format(id=order_id),
            params={"courierId": courier_id}
        )
        
        return response
    
    @allure.step("Отмена заказа")
    def cancel_order(self, track):
        response = self.session.put(
            Urls.BASE_URL + Urls.CANCEL_ORDER,
            params={"track": track}
        )
        
        return response


class DataGenerator:
    def __init__(self):
        self.russian_names = ["Иван", "Петр", "Сергей", "Алексей", "Дмитрий", 
                              "Андрей", "Михаил", "Александр", "Николай", "Владимир"]
        self.russian_lastnames = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", 
                                  "Попов", "Васильев", "Михайлов", "Новиков", "Федоров"]
        self.streets = ["Ленина", "Гагарина", "Пушкина", "Мира", "Советская", 
                        "Центральная", "Молодежная", "Школьная", "Садовая", "Набережная"]
    
    def _generate_russian_name(self):
        return random.choice(self.russian_names)
    
    def _generate_russian_last_name(self):
        return random.choice(self.russian_lastnames)
    
    @allure.step("Генерация данных для заказа")
    def generate_order_data(self, color=None):
        order_data = {
            "firstName": self._generate_russian_name(),
            "lastName": self._generate_russian_last_name(),
            "address": f"ул. {random.choice(self.streets)}, д. {random.randint(1, 100)}, кв. {random.randint(1, 200)}",
            "metroStation": str(random.randint(1, 10)),
            "phone": f"+79{random.randint(100000000, 999999999)}",
            "rentTime": random.randint(1, 7),
            "deliveryDate": (datetime.date.today() + datetime.timedelta(days=random.randint(1, 30))).isoformat(),
            "comment": "Позвоните за час до доставки",
        }
        
        if color is not None:
            order_data["color"] = color if isinstance(color, list) else [color]
        
        return order_data
    
    def generate_random_string(self, length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))


# Простые фикстуры, которые должны храниться в helpers.py согласно ревью
@pytest.fixture
def api_client():
    """Фикстура для создания клиента API"""
    return ScooterApi()

@pytest.fixture
def data_generator():
    """Фикстура для генератора данных"""
    return DataGenerator()