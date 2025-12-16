import pytest
import sys
import os

# Добавляем корневую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем фикстуры из helpers
from helpers import api_client, data_generator

# Импортируем классы для создания сложных фикстур
from helpers import ScooterApi, DataGenerator
import allure


@pytest.fixture
def setup_courier():
    """Сложная фикстура для создания и удаления тестового курьера"""
    api = ScooterApi()
    
    # Создание курьера
    courier_data = api.register_new_courier()
    
    # Получение ID курьера
    login_response = api.login_courier(
        courier_data["login"],
        courier_data["password"]
    )
    
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
    else:
        courier_id = None
    
    yield {
        "api": api,
        "login": courier_data["login"],
        "password": courier_data["password"],
        "first_name": courier_data["first_name"],
        "courier_id": courier_id
    }
    
    # Удаление курьера после теста
    if courier_id:
        api.delete_courier(courier_id)


@pytest.fixture
def setup_order():
    """Сложная фикстура для создания и удаления тестового заказа"""
    api = ScooterApi()
    data_gen = DataGenerator()
    
    # Создание заказа
    order_data = data_gen.generate_order_data(["BLACK"])
    response = api.create_order(order_data)
    
    if response.status_code == 201:
        track = response.json()["track"]
    else:
        track = None
    
    yield {
        "api": api,
        "order_data": order_data,
        "track": track
    }
    
    # Отмена заказа после теста
    if track:
        api.cancel_order(track)


@pytest.fixture
def setup_courier_and_order(setup_courier):
    """Сложная фикстура для создания курьера и заказа"""
    courier_fixture = setup_courier
    api = courier_fixture["api"]
    data_gen = DataGenerator()
    
    # Создание заказа
    order_data = data_gen.generate_order_data(["BLACK"])
    response = api.create_order(order_data)
    
    if response.status_code == 201:
        track = response.json()["track"]
    else:
        track = None
    
    yield {
        **courier_fixture,
        "order_data": order_data,
        "track": track
    }
    
    # Отмена заказа после теста
    if track:
        api.cancel_order(track)