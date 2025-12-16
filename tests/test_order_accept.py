import allure
import pytest
from helpers import ScooterApi, DataGenerator
from config.urls import Urls
from data.messages import Messages


class TestOrderAccept:
    @allure.title("Позитивный тест: Принятие заказа курьером")
    def test_accept_order_success(self, setup_courier_and_order):
        """Тест на успешное принятие заказа с использованием фикстуры"""
        setup_data = setup_courier_and_order
        api = setup_data["api"]
        track = setup_data["track"]
        courier_id = setup_data["courier_id"]
        
        # Получение ID заказа по трек-номеру
        track_response = api.get_order_by_track(track)
        order_id = track_response.json()["order"]["id"]
        
        # Принятие заказа курьером
        response = api.accept_order(order_id, courier_id)
        
        assert response.status_code == 200
        assert response.json()["ok"] is True
    
    @allure.title("Негативный тест: Принятие заказа без ID курьера")
    def test_accept_order_without_courier_id(self, setup_order):
        """Тест на принятие заказа без указания ID курьера"""
        setup_data = setup_order
        api = setup_data["api"]
        track = setup_data["track"]
        
        # Получение ID заказа
        track_response = api.get_order_by_track(track)
        order_id = track_response.json()["order"]["id"]
        
        # Пытаемся принять заказ без courierId в параметрах
        response = api.session.put(
            Urls.BASE_URL + Urls.ACCEPT_ORDER.format(id=order_id)
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_SEARCH
    
    @allure.title("Негативный тест: Принятие заказа с несуществующим ID курьера")
    def test_accept_order_with_nonexistent_courier(self, setup_order):
        """Тест на принятие заказа несуществующим курьером"""
        setup_data = setup_order
        api = setup_data["api"]
        track = setup_data["track"]
        
        # Получение ID заказа
        track_response = api.get_order_by_track(track)
        order_id = track_response.json()["order"]["id"]
        
        # Пытаемся принять заказ несуществующим курьером
        nonexistent_courier_id = 999999
        response = api.accept_order(order_id, nonexistent_courier_id)
        
        assert response.status_code == 400
        assert response.json()["message"] == Messages.NOT_ENOUGH_DATA_FOR_SEARCH