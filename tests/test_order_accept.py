import allure
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import ScooterApi, DataGenerator


class TestOrderAccept:
    @allure.title("Позитивный тест: Принятие заказа курьером")
    def test_accept_order_success(self):
        """Тест на успешное принятие заказа"""
        api = ScooterApi()
        data_gen = DataGenerator()
        
        with allure.step("Создание тестового курьера"):
            courier_data = api.register_new_courier()
            login_response = api.login_courier(
                courier_data["login"],
                courier_data["password"]
            )
            courier_id = login_response.json()["id"]
        
        with allure.step("Создание тестового заказа"):
            order_data = data_gen.generate_order_data(["BLACK"])
            create_order_response = api.create_order(order_data)
            assert create_order_response.status_code == 201
            track = create_order_response.json()["track"]
        
        with allure.step("Получение ID заказа по трек-номеру"):
            track_response = api.get_order_by_track(track)
            assert track_response.status_code == 200
            order_id = track_response.json()["order"]["id"]
        
        with allure.step("Принятие заказа курьером"):
            response = api.accept_order(order_id, courier_id)
            assert response.status_code == 200
            assert response.json()["ok"] is True
        
        with allure.step("Очистка тестовых данных"):
            api.cancel_order(track)
            api.delete_courier(courier_id)
    
    @allure.title("Негативный тест: Принятие заказа без ID курьера")
    def test_accept_order_without_courier_id(self):
        """Тест на принятие заказа без указания ID курьера"""
        api = ScooterApi()
        
        data_gen = DataGenerator()
        order_data = data_gen.generate_order_data(["BLACK"])
        create_order_response = api.create_order(order_data)
        track = create_order_response.json()["track"]
        
        track_response = api.get_order_by_track(track)
        order_id = track_response.json()["order"]["id"]
        
        response = api.session.put(
            f"{api.BASE_URL}/api/v1/orders/accept/{order_id}"
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"
        
        api.cancel_order(track)
    
    @allure.title("Негативный тест: Принятие заказа с несуществующим ID курьера")
    def test_accept_order_with_nonexistent_courier(self):
        """Тест на принятие заказа несуществующим курьером"""
        api = ScooterApi()
        
        data_gen = DataGenerator()
        order_data = data_gen.generate_order_data(["BLACK"])
        create_order_response = api.create_order(order_data)
        track = create_order_response.json()["track"]
        
        track_response = api.get_order_by_track(track)
        order_id = track_response.json()["order"]["id"]
        
        nonexistent_courier_id = 999999
        response = api.accept_order(order_id, nonexistent_courier_id)
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"
        
        api.cancel_order(track)