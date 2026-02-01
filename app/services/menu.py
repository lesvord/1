from __future__ import annotations

from dataclasses import dataclass
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

CallbackAction = Literal["text", "menu"]

MENU_BUTTONS = [
    "Профиль",
    "Вылазка",
    "Локации",
    "Рейд",
    "Группировка",
    "Инвентарь",
    "Помощь",
]

LOCATIONS = ["Кордон", "Свалка", "Бар"]

PROFILE = {
    "level": 1,
    "health": 100,
    "radiation": 0,
    "reputation": "нейтрал",
}

HELP_LINES = [
    "Кнопки меню запускают основные действия.",
    "Инлайн-кнопки помогают выбирать решения в событиях.",
]

FACTION_STATUS = {
    "joined": False,
    "message": "Ты пока не вступил в группировку.",
    "hint": "Выбери сторону позже, когда заработаешь репутацию.",
}

INVENTORY = {
    "items": [],
    "empty_message": "Инвентарь пуст. Найди припасы в вылазке!",
}

EXPLORE_EVENTS = {
    "explore_anomaly": "Аномалия впереди. Ты кидаешь болт и замечаешь артефакт.",
    "explore_area": "Ты находишь тайник с патронами.",
}

RAID_EVENTS = {
    "raid_create": "Рейд создан. Ожидаем напарников.",
    "raid_join": "Ты присоединился к рейду.",
}


@dataclass(frozen=True)
class CallbackResult:
    action: CallbackAction
    text: str | None = None


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


def resolve_callback(data: str) -> CallbackResult:
    if data in EXPLORE_EVENTS:
        return CallbackResult(action="text", text=EXPLORE_EVENTS[data])
    if data in RAID_EVENTS:
        return CallbackResult(action="text", text=RAID_EVENTS[data])
    if data == "back_to_menu":
        return CallbackResult(action="menu")
    return CallbackResult(action="text", text="Команда не распознана.")
