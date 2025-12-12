import allure
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import ScooterApi, DataGenerator


class TestOrderTrack:
    @allure.title("Позитивный тест: Получение заказа по трек-номеру")
    def test_get_order_by_track_success(self):
        """Тест на успешное получение заказа по трек-номеру"""
        api = ScooterApi()
        data_gen = DataGenerator()
        
        with allure.step("Создание тестового заказа"):
            order_data = data_gen.generate_order_data(["BLACK"])
            create_response = api.create_order(order_data)
            assert create_response.status_code == 201
            track = create_response.json()["track"]
        
        with allure.step("Получение заказа по трек-номеру"):
            response = api.get_order_by_track(track)
            assert response.status_code == 200
            
            response_json = response.json()
            assert "order" in response_json
            
            order = response_json["order"]
            assert order["track"] == track
            assert "id" in order
            assert "firstName" in order
            assert "lastName" in order
            assert "address" in order
            assert "phone" in order
        
        with allure.step("Очистка тестовых данных"):
            api.cancel_order(track)
    
    @allure.title("Негативный тест: Получение заказа без трек-номера")
    def test_get_order_without_track(self):
        """Тест на получение заказа без указания трек-номера"""
        api = ScooterApi()
        
        response = api.session.get(
            f"{api.BASE_URL}/api/v1/orders/track"
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"
    
    @allure.title("Негативный тест: Получение заказа с несуществующим трек-номером")
    def test_get_order_with_nonexistent_track(self):
        """Тест на получение заказа с несуществующим трек-номером"""
        api = ScooterApi()
        
        nonexistent_track = 999999
        response = api.get_order_by_track(nonexistent_track)
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"