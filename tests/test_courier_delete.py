import allure
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import ScooterApi


class TestCourierDelete:
    @allure.title("Позитивный тест: Удаление курьера")
    def test_delete_courier_success(self):
        """Тест на успешное удаление курьера"""
        api = ScooterApi()
        
        with allure.step("Создание тестового курьера"):
            courier_data = api.register_new_courier()
            assert courier_data["response"].status_code == 201
        
        with allure.step("Логин для получения ID"):
            login_response = api.login_courier(
                courier_data["login"],
                courier_data["password"]
            )
            assert login_response.status_code == 200
            courier_id = login_response.json()["id"]
        
        with allure.step("Удаление курьера"):
            response = api.delete_courier(courier_id)
            assert response.status_code == 200
            assert response.json()["ok"] is True
        
        with allure.step("Проверка, что курьер удален"):
            login_again_response = api.login_courier(
                courier_data["login"],
                courier_data["password"]
            )
            assert login_again_response.status_code == 404
    
    @allure.title("Негативный тест: Удаление без ID")
    def test_delete_courier_without_id(self):
        """Тест на удаление курьера без указания ID"""
        api = ScooterApi()
        
        response = api.session.delete(
            f"{api.BASE_URL}/api/v1/courier/"
        )
        
        assert response.status_code in [400, 404, 405]
    
    @allure.title("Негативный тест: Удаление с несуществующим ID")
    def test_delete_courier_with_nonexistent_id(self):
        """Тест на удаление курьера с несуществующим ID"""
        api = ScooterApi()
        
        nonexistent_id = 999999
        
        response = api.delete_courier(nonexistent_id)
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для удаления курьера"
    
    @allure.title("Проверка тела ответа при успешном удалении")
    def test_delete_courier_response_body(self):
        """Тест на проверку тела ответа при удалении курьера"""
        api = ScooterApi()
        
        with allure.step("Создание и удаление курьера"):
            courier_data = api.register_new_courier()
            login_response = api.login_courier(
                courier_data["login"],
                courier_data["password"]
            )
            courier_id = login_response.json()["id"]
            
            response = api.delete_courier(courier_id)
            
            response_json = response.json()
            assert response_json == {"ok": True}