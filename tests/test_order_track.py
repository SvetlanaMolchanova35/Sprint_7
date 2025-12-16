import allure
import pytest
from helpers import ScooterApi, DataGenerator
from config.urls import Urls
from data.messages import Messages


class TestOrderTrack:
    @allure.title("Позитивный тест: Получение заказа по трек-номеру")
    def test_get_order_by_track_success(self, setup_order):
        """Тест на успешное получение заказа по трек-номеру"""
        setup_data = setup_order
        api = setup_data["api"]
        track = setup_data["track"]
        
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
    
    @allure.title("Негативный тест: Получение заказа без трек-номера")
    def test_get_order_without_track(self, api_client):
        """Тест на получение заказа без указания трек-номера"""
        api = api_client
        
        response = api.session.get(
            Urls.BASE_URL + Urls.GET_ORDER_BY_TRACK
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_SEARCH
    
    @allure.title("Негативный тест: Получение заказа с несуществующим трек-номером")
    def test_get_order_with_nonexistent_track(self, api_client):
        """Тест на получение заказа с несуществующим трек-номером"""
        api = api_client
        
        nonexistent_track = 999999
        response = api.get_order_by_track(nonexistent_track)
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_SEARCH