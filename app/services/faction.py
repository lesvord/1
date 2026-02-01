from __future__ import annotations

from copy import deepcopy

DEFAULT_STATUS = {
    "joined": False,
    "faction": None,
    "reputation": 5,
    "available": ["Долг", "Свобода"],
    "message": "Ты пока не вступил в группировку.",
    "hint": "Выбери сторону, чтобы открыть новые задания.",
}

USER_STATUS: dict[int, dict[str, object]] = {}


def get_status(user_id: int) -> dict[str, object]:
    if user_id not in USER_STATUS:
        USER_STATUS[user_id] = deepcopy(DEFAULT_STATUS)
    return deepcopy(USER_STATUS[user_id])


def join_faction(user_id: int, faction: str) -> str:
    status = USER_STATUS.setdefault(user_id, deepcopy(DEFAULT_STATUS))
    if status["joined"]:
        return f"Ты уже состоишь в группировке: {status['faction']}."
    if faction not in status["available"]:
        return "Эта группировка пока недоступна."
    status["joined"] = True
    status["faction"] = faction
    status["message"] = f"Ты вступил в группировку «{faction}»."
    status["hint"] = "Новые союзники ждут тебя в штабе."
    return status["message"]


def handle_callback(data: str, user_id: int) -> str | None:
    if data.startswith("faction_join_"):
        faction = data.removeprefix("faction_join_")
        return join_faction(user_id, faction)
    return None
