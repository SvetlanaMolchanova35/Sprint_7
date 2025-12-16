import allure
import pytest
from helpers import ScooterApi
from config.urls import Urls
from data.messages import Messages


class TestCourierCreation:
    @allure.title("Позитивный тест: Создание курьера")
    def test_create_courier_success(self, api_client):
        """Тест на успешное создание курьера - проверка только статуса 201"""
        api = api_client
        
        response = api.register_new_courier()["response"]
        
        assert response.status_code == 201
    
    @allure.title("Позитивный тест: Тело ответа при создании курьера")
    def test_create_courier_response_body(self, api_client):
        """Тест на успешное создание курьера - проверка только тела ответа"""
        api = api_client
        
        response = api.register_new_courier()["response"]
        
        assert response.json() == Messages.OK_TRUE
    
    @allure.title("Негативный тест: Создание курьера без логина")
    def test_create_courier_without_login(self, api_client):
        """Тест на создание курьера без обязательного поля логин"""
        api = api_client
        
        payload = {
            "password": api.generate_random_string(10),
            "firstName": api.generate_random_string(10)
        }
        
        response = api.session.post(
            Urls.BASE_URL + Urls.CREATE_COURIER,
            data=payload
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_ACCOUNT
    
    @allure.title("Негативный тест: Создание курьера без пароля")
    def test_create_courier_without_password(self, api_client):
        """Тест на создание курьера без обязательного поля пароль"""
        api = api_client
        
        payload = {
            "login": api.generate_random_string(10),
            "firstName": api.generate_random_string(10)
        }
        
        response = api.session.post(
            Urls.BASE_URL + Urls.CREATE_COURIER,
            data=payload
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_ACCOUNT
    
    @allure.title("Негативный тест: Создание дубликата курьера")
    def test_create_duplicate_courier(self, api_client, setup_courier):
        """Тест на создание курьера с уже существующим логином"""
        api = api_client
        
        # Используем курьера из фикстуры setup_courier
        existing_login = setup_courier["login"]
        
        payload = {
            "login": existing_login,
            "password": api.generate_random_string(10),
            "firstName": api.generate_random_string(10)
        }
        
        response = api.session.post(
            Urls.BASE_URL + Urls.CREATE_COURIER,
            data=payload
        )
        
        assert response.status_code == 409