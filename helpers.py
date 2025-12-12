import requests
import random
import string
import allure
from faker import Faker


class ScooterApi:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    def __init__(self):
        self.session = requests.Session()
    
    @allure.step("Генерация случайной строки")
    def generate_random_string(self, length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    @allure.step("Регистрация нового курьера")
    def register_new_courier(self):
        """Метод для регистрации нового курьера"""
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/courier",
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
        """Метод для авторизации курьера"""
        payload = {
            "login": login,
            "password": password
        }
        
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/courier/login",
            data=payload
        )
        
        return response
    
    @allure.step("Удаление курьера")
    def delete_courier(self, courier_id):
        """Метод для удаления курьера"""
        response = self.session.delete(
            f"{self.BASE_URL}/api/v1/courier/{courier_id}"
        )
        
        return response
    
    @allure.step("Создание заказа")
    def create_order(self, order_data):
        """Метод для создания заказа"""
        response = self.session.post(
            f"{self.BASE_URL}/api/v1/orders",
            json=order_data
        )
        
        return response
    
    @allure.step("Получение списка заказов")
    def get_orders_list(self, params=None):
        """Метод для получения списка заказов"""
        response = self.session.get(
            f"{self.BASE_URL}/api/v1/orders",
            params=params
        )
        
        return response
    
    @allure.step("Получение заказа по трек-номеру")
    def get_order_by_track(self, track):
        """Метод для получения заказа по трек-номеру"""
        response = self.session.get(
            f"{self.BASE_URL}/api/v1/orders/track",
            params={"t": track}
        )
        
        return response
    
    @allure.step("Принятие заказа курьером")
    def accept_order(self, order_id, courier_id):
        """Метод для принятия заказа"""
        response = self.session.put(
            f"{self.BASE_URL}/api/v1/orders/accept/{order_id}",
            params={"courierId": courier_id}
        )
        
        return response
    
    @allure.step("Отмена заказа")
    def cancel_order(self, track):
        """Метод для отмены заказа"""
        response = self.session.put(
            f"{self.BASE_URL}/api/v1/orders/cancel",
            params={"track": track}
        )
        
        return response


class DataGenerator:
    """Класс для генерации тестовых данных"""
    
    def __init__(self):
        self.fake = Faker('ru_RU')
    
    @allure.step("Генерация данных для заказа")
    def generate_order_data(self, color=None):
        """Генерация данных для создания заказа"""
        order_data = {
            "firstName": self.fake.first_name(),
            "lastName": self.fake.last_name(),
            "address": self.fake.address(),
            "metroStation": str(random.randint(1, 10)),
            "phone": f"+7{self.fake.numerify('##########')}",
            "rentTime": random.randint(1, 7),
            "deliveryDate": self.fake.date_this_year().isoformat(),
            "comment": self.fake.text(max_nb_chars=50),
        }
        
        if color is not None:
            order_data["color"] = color if isinstance(color, list) else [color]
        
        return order_data
    
    def generate_random_string(self, length=10):
        """Генерация случайной строки"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))