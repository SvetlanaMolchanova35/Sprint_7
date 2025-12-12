import allure
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import ScooterApi


class TestOrderList:
    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        """Тест на получение списка заказов"""
        api = ScooterApi()
        
        response = api.get_orders_list()
        
        assert response.status_code == 200
        
        response_json = response.json()
        assert "orders" in response_json
        assert "pageInfo" in response_json
        assert "availableStations" in response_json
        
        # Проверка структуры данных
        page_info = response_json["pageInfo"]
        assert "page" in page_info
        assert "total" in page_info
        assert "limit" in page_info
    
    @allure.title("Получение списка заказов с лимитом")
    def test_get_orders_list_with_limit(self):
        """Тест на получение списка заказов с ограничением количества"""
        api = ScooterApi()
        
        params = {"limit": 5}
        response = api.get_orders_list(params)
        
        assert response.status_code == 200
        
        response_json = response.json()
        assert len(response_json["orders"]) <= 5
        assert response_json["pageInfo"]["limit"] == 5