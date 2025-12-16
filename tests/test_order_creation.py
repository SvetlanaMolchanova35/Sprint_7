import allure
import pytest
from helpers import ScooterApi, DataGenerator
from config.urls import Urls
from data.messages import Messages


class TestOrderCreation:
    @allure.title("Создание заказа с цветом BLACK")
    def test_create_order_with_black_color(self, api_client, data_generator):
        """Тест создания заказа с цветом BLACK"""
        api = api_client
        
        order_data = data_generator.generate_order_data(["BLACK"])
        response = api.create_order(order_data)
        
        assert response.status_code == 201
        
        response_json = response.json()
        assert "track" in response_json
        assert isinstance(response_json["track"], int)
        
        # Отмена заказа после теста
        track = response.json()["track"]
        cancel_response = api.cancel_order(track)
        assert cancel_response.status_code in [200, 400]
    
    @allure.title("Создание заказа с цветом GREY")
    def test_create_order_with_grey_color(self, api_client, data_generator):
        """Тест создания заказа с цветом GREY"""
        api = api_client
        
        order_data = data_generator.generate_order_data(["GREY"])
        response = api.create_order(order_data)
        
        assert response.status_code == 201
        
        response_json = response.json()
        assert "track" in response_json
        assert isinstance(response_json["track"], int)
        
        track = response.json()["track"]
        cancel_response = api.cancel_order(track)
        assert cancel_response.status_code in [200, 400]
    
    @allure.title("Создание заказа с обоими цветами")
    def test_create_order_with_both_colors(self, api_client, data_generator):
        """Тест создания заказа с обоими цветами"""
        api = api_client
        
        order_data = data_generator.generate_order_data(["BLACK", "GREY"])
        response = api.create_order(order_data)
        
        assert response.status_code == 201
        
        response_json = response.json()
        assert "track" in response_json
        assert isinstance(response_json["track"], int)
        
        track = response.json()["track"]
        cancel_response = api.cancel_order(track)
        assert cancel_response.status_code in [200, 400]
    
    @allure.title("Создание заказа без указания цвета")
    def test_create_order_without_color(self, api_client, data_generator):
        """Тест создания заказа без указания цвета"""
        api = api_client
        
        order_data = data_generator.generate_order_data()
        response = api.create_order(order_data)
        
        assert response.status_code == 201
        
        response_json = response.json()
        assert "track" in response_json
        assert isinstance(response_json["track"], int)
        
        track = response.json()["track"]
        cancel_response = api.cancel_order(track)
        assert cancel_response.status_code in [200, 400]