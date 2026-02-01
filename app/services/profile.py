from __future__ import annotations

from copy import deepcopy

DEFAULT_PROFILE = {
    "level": 3,
    "health": 82,
    "radiation": 12,
    "reputation": "новичок",
    "progress": {
        "raids_completed": 1,
        "artifacts_found": 2,
        "locations_opened": 2,
    },
}

USER_PROFILES: dict[int, dict[str, object]] = {}


def get_profile(user_id: int) -> dict[str, object]:
    if user_id not in USER_PROFILES:
        USER_PROFILES[user_id] = deepcopy(DEFAULT_PROFILE)
    return deepcopy(USER_PROFILES[user_id])


def rest(user_id: int) -> str:
    profile = USER_PROFILES.setdefault(user_id, deepcopy(DEFAULT_PROFILE))
    profile["health"] = min(int(profile["health"]) + 15, 100)
    profile["radiation"] = max(int(profile["radiation"]) - 5, 0)
    return "Ты отдохнул у костра. Здоровье и радиация восстановлены."


def use_medkit(user_id: int) -> str:
    profile = USER_PROFILES.setdefault(user_id, deepcopy(DEFAULT_PROFILE))
    profile["health"] = min(int(profile["health"]) + 25, 100)
    return "Ты использовал аптечку. Здоровье восстановлено."


def handle_callback(data: str, user_id: int) -> str | None:
    if data == "profile_rest":
        return rest(user_id)
    if data == "profile_medkit":
        return use_medkit(user_id)
    return None
