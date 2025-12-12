import allure
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import ScooterApi


class TestCourierLogin:
    @allure.title("Позитивный тест: Логин курьера")
    def test_login_courier_success(self):
        """Тест на успешный логин курьера"""
        api = ScooterApi()
        
        with allure.step("Регистрация курьера"):
            courier_data = api.register_new_courier()
            assert courier_data["response"].status_code == 201
        
        with allure.step("Логин курьера"):
            response = api.login_courier(
                courier_data["login"],
                courier_data["password"]
            )
            
            assert response.status_code == 200
            
            response_json = response.json()
            assert "id" in response_json
            assert isinstance(response_json["id"], int)
        
        with allure.step("Удаление тестового курьера"):
            courier_id = response.json()["id"]
            api.delete_courier(courier_id)
    
    @allure.title("Негативный тест: Логин без логина")
    def test_login_without_login(self):
        """Тест на логин без указания логина"""
        api = ScooterApi()
        
        payload = {
            "password": api.generate_random_string(10)
        }
        
        response = api.session.post(
            f"{api.BASE_URL}/api/v1/courier/login",
            data=payload
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"
    
    @allure.title("Негативный тест: Логин без пароля")
    def test_login_without_password(self):
        """Тест на логин без указания пароля"""
        api = ScooterApi()
        
        payload = {
            "login": api.generate_random_string(10)
        }
        
        response = api.session.post(
            f"{api.BASE_URL}/api/v1/courier/login",
            data=payload
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"
    
    @allure.title("Негативный тест: Логин с неверными данными")
    def test_login_with_wrong_credentials(self):
        """Тест на логин с неверными учетными данными"""
        api = ScooterApi()
        
        payload = {
            "login": "nonexistent_user",
            "password": "wrong_password"
        }
        
        response = api.session.post(
            f"{api.BASE_URL}/api/v1/courier/login",
            data=payload
        )
        
        assert response.status_code == 404