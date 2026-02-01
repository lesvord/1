from __future__ import annotations

from copy import deepcopy
from uuid import uuid4

DEFAULT_OVERVIEW = {
    "active_raids": 0,
    "message": "Рейды пока не запущены.",
}

RAIDS: list[dict[str, object]] = []


def get_overview() -> dict[str, object]:
    overview = deepcopy(DEFAULT_OVERVIEW)
    overview["active_raids"] = len(RAIDS)
    if RAIDS:
        overview["message"] = f"Доступно рейдов: {len(RAIDS)}"
    return overview


def create_raid(user_id: int) -> str:
    raid_id = uuid4().hex[:6]
    RAIDS.append({"id": raid_id, "leader": user_id, "members": [user_id]})
    return f"Рейд создан (#{raid_id}). Ожидаем напарников."


def join_raid(user_id: int) -> str:
    if not RAIDS:
        return "Нет активных рейдов. Создай новый рейд."
    raid = RAIDS[0]
    members = raid["members"]
    if user_id in members:
        return "Ты уже в этом рейде."
    members.append(user_id)
    return f"Ты присоединился к рейду #{raid['id']}."


def handle_callback(data: str, user_id: int) -> str | None:
    if data == "raid_create":
        return create_raid(user_id)
    if data == "raid_join":
        return join_raid(user_id)
    return None
