import allure
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import ScooterApi


class TestCourierCreation:
    @allure.title("Позитивный тест: Создание курьера")
    def test_create_courier_success(self):
        """Тест на успешное создание курьера"""
        api = ScooterApi()
        
        with allure.step("Регистрация нового курьера"):
            courier_data = api.register_new_courier()
            response = courier_data["response"]
        
        with allure.step("Проверка кода ответа"):
            assert response.status_code == 201
        
        with allure.step("Проверка тела ответа"):
            assert response.json()["ok"] is True
        
        with allure.step("Удаление тестового курьера"):
            login_response = api.login_courier(
                courier_data["login"],
                courier_data["password"]
            )
            
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                api.delete_courier(courier_id)
    
    @allure.title("Негативный тест: Создание курьера без логина")
    def test_create_courier_without_login(self):
        """Тест на создание курьера без обязательного поля логин"""
        api = ScooterApi()
        
        payload = {
            "password": api.generate_random_string(10),
            "firstName": api.generate_random_string(10)
        }
        
        response = api.session.post(
            f"{api.BASE_URL}/api/v1/courier",
            data=payload
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
    
    @allure.title("Негативный тест: Создание курьера без пароля")
    def test_create_courier_without_password(self):
        """Тест на создание курьера без обязательного поля пароль"""
        api = ScooterApi()
        
        payload = {
            "login": api.generate_random_string(10),
            "firstName": api.generate_random_string(10)
        }
        
        response = api.session.post(
            f"{api.BASE_URL}/api/v1/courier",
            data=payload
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
    
    @allure.title("Негативный тест: Создание дубликата курьера")
    def test_create_duplicate_courier(self):
        """Тест на создание курьера с уже существующим логином"""
        api = ScooterApi()
        
        with allure.step("Создание первого курьера"):
            courier_data = api.register_new_courier()
            assert courier_data["response"].status_code == 201
        
        with allure.step("Попытка создания второго курьера с тем же логином"):
            payload = {
                "login": courier_data["login"],
                "password": api.generate_random_string(10),
                "firstName": api.generate_random_string(10)
            }
            
            response = api.session.post(
                f"{api.BASE_URL}/api/v1/courier",
                data=payload
            )
            
            assert response.status_code == 409
        
        with allure.step("Удаление тестового курьера"):
            login_response = api.login_courier(
                courier_data["login"],
                courier_data["password"]
            )
            
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                api.delete_courier(courier_id)