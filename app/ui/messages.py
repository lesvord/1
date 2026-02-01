from __future__ import annotations


def format_main_menu() -> str:
    return "Главное меню:"


def format_profile(profile: dict[str, object]) -> str:
    progress = profile["progress"]
    return (
        "Профиль сталкера:\n"
        f"Уровень: {profile['level']}\n"
        f"Здоровье: {profile['health']}\n"
        f"Радиация: {profile['radiation']}\n"
        f"Репутация: {profile['reputation']}\n"
        "Прогресс:\n"
        f"- Рейды: {progress['raids_completed']}\n"
        f"- Артефакты: {progress['artifacts_found']}\n"
        f"- Локации: {progress['locations_opened']}"
    )


def format_inventory(inventory: dict[str, object]) -> str:
    items = inventory["items"]
    if not items:
        return inventory["empty_message"]
    lines = []
    for item in items:
        marker = " (экипировано)" if item.get("equipped") else ""
        lines.append(f"- {item['name']}{marker}")
    return "Инвентарь:\n" + "\n".join(lines)


def format_locations(locations: list[str]) -> str:
    return "Доступные локации:\n" + "\n".join(f"- {location}" for location in locations)


def format_raid_overview(overview: dict[str, object]) -> str:
    return f"Рейды\n{overview['message']}"


def format_faction(status: dict[str, object]) -> str:
    if status["joined"]:
        return f"{status['message']}\nРепутация: {status['reputation']}"
    available = ", ".join(status["available"])
    return f"{status['message']}\n{status['hint']}\nДоступно: {available}"


def format_help(lines: list[str]) -> str:
    return "\n".join(lines)


def format_help_section(title: str, lines: list[str]) -> str:
    return f"{title}:\n" + "\n".join(f"- {line}" for line in lines)


def format_explore_prompt() -> str:
    return "Ты выходишь в Зону. Куда направимся?"
