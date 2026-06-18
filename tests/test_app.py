from datetime import datetime

from api.app import is_open_now, parse_bool, select_recommendation


def test_parse_bool():
    assert parse_bool("true") is True
    assert parse_bool("yes") is True
    assert parse_bool("false") is False
    assert parse_bool(None) is None


def test_is_open_now_same_day():
    assert is_open_now("09:00", "17:00", datetime(2026, 1, 1, 12, 0)) is True
    assert is_open_now("09:00", "17:00", datetime(2026, 1, 1, 20, 0)) is False


def test_is_open_now_overnight():
    assert is_open_now("20:00", "02:00", datetime(2026, 1, 1, 23, 0)) is True
    assert is_open_now("20:00", "02:00", datetime(2026, 1, 1, 1, 0)) is True
    assert is_open_now("20:00", "02:00", datetime(2026, 1, 1, 12, 0)) is False


def test_select_recommendation_returns_open_restaurant():
    restaurants = [
        {"id": "1", "name": "Closed", "openHour": "09:00", "closeHour": "10:00"},
        {"id": "2", "name": "Open", "openHour": "09:00", "closeHour": "23:00"},
    ]
    assert select_recommendation(restaurants, datetime(2026, 1, 1, 12, 0))["name"] == "Open"
