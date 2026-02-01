from __future__ import annotations

from app.services import explore as explore_service


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


def format_explore_event(event: dict[str, object]) -> str:
    title = event.get("title", "Событие")
    description = event.get("description", "Вокруг тихо, но что-то происходит.")
    risk_level = int(event.get("risk_level", 0))
    risk_label = explore_service.get_risk_label(risk_level)
    rewards = event.get("rewards", [])
    reward_text = ", ".join(rewards) if rewards else "неизвестно"
    return (
        f"{title}\n"
        f"{description}\n"
        f"Риск: {risk_label}\n"
        f"Награды: {reward_text}"
    )
