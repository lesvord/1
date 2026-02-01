from __future__ import annotations


def format_main_menu() -> str:
    return "Главное меню:"


def format_profile(profile: dict[str, int | str]) -> str:
    return (
        "Профиль сталкера:\n"
        f"Уровень: {profile['level']}\n"
        f"Здоровье: {profile['health']}\n"
        f"Радиация: {profile['radiation']}\n"
        f"Репутация: {profile['reputation']}"
    )


def format_inventory(items: list[str], empty_message: str) -> str:
    if not items:
        return empty_message
    return "Инвентарь:\n" + "\n".join(f"- {item}" for item in items)


def format_locations(locations: list[str]) -> str:
    return "Доступные локации:\n" + "\n".join(f"- {location}" for location in locations)


def format_raid_title() -> str:
    return "Рейды"


def format_faction(status: dict[str, str | bool]) -> str:
    return f"{status['message']}\n{status['hint']}"


def format_help(lines: list[str]) -> str:
    return "\n".join(lines)


def format_explore_prompt() -> str:
    return "Ты выходишь в Зону. Куда направимся?"
