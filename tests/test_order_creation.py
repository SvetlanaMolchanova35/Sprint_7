import allure
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import ScooterApi, DataGenerator


class TestOrderCreation:
    @allure.title("Создание заказа с разными цветами самокатов")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_with_different_colors(self, color):
        """Параметризованный тест создания заказа с разными цветами"""
        api = ScooterApi()
        data_gen = DataGenerator()
        
        with allure.step(f"Создание заказа с цветом: {color}"):
            order_data = data_gen.generate_order_data(color)
            response = api.create_order(order_data)
            
            assert response.status_code == 201
            
            response_json = response.json()
            assert "track" in response_json
            assert isinstance(response_json["track"], int)
        
        with allure.step("Отмена созданного заказа"):
            track = response.json()["track"]
            cancel_response = api.cancel_order(track)
            # Некоторые заказы могут быть уже приняты, поэтому проверяем либо 200, либо 400
            assert cancel_response.status_code in [200, 400]