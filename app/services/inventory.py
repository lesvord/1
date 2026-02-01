from __future__ import annotations

from copy import deepcopy

DEFAULT_INVENTORY = {
    "capacity": 6,
    "empty_message": "Инвентарь пуст. Найди припасы в вылазке!",
    "items": [
        {"id": "pistol", "name": "Пистолет Макарова", "type": "weapon", "equipped": True},
        {"id": "knife", "name": "Боевой нож", "type": "weapon", "equipped": False},
        {"id": "medkit", "name": "Аптечка", "type": "consumable", "equipped": False},
    ],
}

USER_INVENTORIES: dict[int, dict[str, object]] = {}


def get_inventory(user_id: int) -> dict[str, object]:
    if user_id not in USER_INVENTORIES:
        USER_INVENTORIES[user_id] = deepcopy(DEFAULT_INVENTORY)
    return deepcopy(USER_INVENTORIES[user_id])


def equip_item(user_id: int, item_id: str) -> str:
    inventory = USER_INVENTORIES.setdefault(user_id, deepcopy(DEFAULT_INVENTORY))
    items = inventory["items"]
    for item in items:
        if item["type"] == "weapon":
            item["equipped"] = item["id"] == item_id
    return "Экипировка обновлена."


def use_item(user_id: int, item_id: str) -> str:
    inventory = USER_INVENTORIES.setdefault(user_id, deepcopy(DEFAULT_INVENTORY))
    items = inventory["items"]
    for item in items:
        if item["id"] == item_id and item["type"] == "consumable":
            items.remove(item)
            return f"Ты использовал предмет: {item['name']}."
    return "Предмет не найден."


def handle_callback(data: str, user_id: int) -> str | None:
    if data.startswith("inventory_equip_"):
        return equip_item(user_id, data.removeprefix("inventory_equip_"))
    if data.startswith("inventory_use_"):
        return use_item(user_id, data.removeprefix("inventory_use_"))
    return None
