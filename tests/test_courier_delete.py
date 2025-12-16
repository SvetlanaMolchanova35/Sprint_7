import allure
import pytest
from helpers import ScooterApi
from config.urls import Urls
from data.messages import Messages


class TestCourierDelete:
    @allure.title("Позитивный тест: Удаление курьера")
    def test_delete_courier_success(self, setup_courier):
        """Тест на успешное удаление курьера"""
        setup_data = setup_courier
        api = setup_data["api"]
        courier_id = setup_data["courier_id"]
        
        response = api.delete_courier(courier_id)
        
        assert response.status_code == 200
        assert response.json() == Messages.OK_TRUE
    
    @allure.title("Негативный тест: Удаление без ID")
    def test_delete_courier_without_id(self, api_client):
        """Тест на удаление курьера без указания ID"""
        api = api_client
        
        response = api.session.delete(
            Urls.BASE_URL + Urls.DELETE_COURIER.format(id="")
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_DELETE
    
    @allure.title("Негативный тест: Удаление с несуществующим ID")
    def test_delete_courier_with_nonexistent_id(self, api_client):
        """Тест на удаление курьера с несуществующим ID"""
        api = api_client
        
        nonexistent_id = 999999
        
        response = api.delete_courier(nonexistent_id)
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_DELETE
    
    @allure.title("Проверка тела ответа при успешном удалении")
    def test_delete_courier_response_body(self, setup_courier):
        """Тест на проверку тела ответа при удалении курьера"""
        setup_data = setup_courier
        api = setup_data["api"]
        courier_id = setup_data["courier_id"]
        
        response = api.delete_courier(courier_id)
        
        response_json = response.json()
        assert response_json == Messages.OK_TRUE