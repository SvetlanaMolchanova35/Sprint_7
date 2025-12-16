import allure
import pytest
from helpers import ScooterApi
from config.urls import Urls
from data.messages import Messages


class TestCourierLogin:
    @allure.title("Позитивный тест: Логин курьера")
    def test_login_courier_success(self, setup_courier):
        """Тест на успешный логин курьера"""
        setup_data = setup_courier
        api = setup_data["api"]
        
        response = api.login_courier(
            setup_data["login"],
            setup_data["password"]
        )
        
        assert response.status_code == 200
        
        response_json = response.json()
        assert "id" in response_json
        assert isinstance(response_json["id"], int)
    
    @allure.title("Негативный тест: Логин без логина")
    def test_login_without_login(self, api_client):
        """Тест на логин без указания логина"""
        api = api_client
        
        payload = {
            "password": api.generate_random_string(10)
        }
        
        response = api.session.post(
            Urls.BASE_URL + Urls.LOGIN_COURIER,
            data=payload
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_LOGIN
    
    @allure.title("Негативный тест: Логин без пароля")
    def test_login_without_password(self, api_client):
        """Тест на логин без указания пароля"""
        api = api_client
        
        payload = {
            "login": api.generate_random_string(10)
        }
        
        response = api.session.post(
            Urls.BASE_URL + Urls.LOGIN_COURIER,
            data=payload
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_LOGIN
    
    @allure.title("Негативный тест: Логин с неверными данными")
    def test_login_with_wrong_credentials(self, api_client):
        """Тест на логин с неверными учетными данными"""
        api = api_client
        
        payload = {
            "login": "nonexistent_user",
            "password": "wrong_password"
        }
        
        response = api.session.post(
            Urls.BASE_URL + Urls.LOGIN_COURIER,
            data=payload
        )
        
        assert response.status_code == 404