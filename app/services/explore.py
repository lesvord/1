from __future__ import annotations

LOCATIONS = ["Кордон", "Свалка", "Бар"]

EXPLORE_EVENTS = {
    "explore_anomaly": "Аномалия впереди. Ты кидаешь болт и замечаешь артефакт.",
    "explore_area": "Ты находишь тайник с патронами.",
}


def get_locations() -> list[str]:
    return list(LOCATIONS)


def handle_callback(data: str) -> str | None:
    return EXPLORE_EVENTS.get(data)
