from __future__ import annotations

from typing import Literal

MenuAction = Literal[
    "profile",
    "explore",
    "locations",
    "raid",
    "faction",
    "inventory",
    "help",
    "menu",
]

BACK_TO_MENU = "back_to_menu"

MENU_BUTTONS = [
    "Профиль",
    "Вылазка",
    "Локации",
    "Рейд",
    "Группировка",
    "Инвентарь",
    "Помощь",
]


def resolve_menu_choice(text: str) -> MenuAction:
    mapping = {
        "Профиль": "profile",
        "Вылазка": "explore",
        "Локации": "locations",
        "Рейд": "raid",
        "Группировка": "faction",
        "Инвентарь": "inventory",
        "Помощь": "help",
    }
    return mapping.get(text, "menu")
