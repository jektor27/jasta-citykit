"""Shared defaults for CityKit."""

from __future__ import annotations

DEFAULT_CITY = "Примерск"
DEFAULT_MIN_SCORE = 0.82
DEFAULT_LANG = "ru"
DEFAULT_TIMEZONE = "Europe/Kaliningrad"

NOISE_HINTS = (
    "банкомат",
    "парковка",
    "автомойка",
    "stop",
    "остановка",
    "переход",
    "жилой дом",
)

STREET_WORDS = ("улица", "ул", "переулок", "пер", "проспект", "пр", "шоссе")

CATEGORIES = (
    "stroymaterialy",
    "avto",
    "cvety",
    "cafe",
    "zootovary",
    "apteka",
)
