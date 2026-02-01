from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.services import menu as menu_service


def build_menu_keyboard(buttons: list[str]) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    for label in buttons:
        builder.button(text=label)
    builder.adjust(2, 2, 2, 1)
    return builder


def explore_inline_keyboard(locations: list[str]) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []
    for index, location in enumerate(locations):
        buttons.append(
            [
                InlineKeyboardButton(
                    text=location,
                    callback_data=f"explore_start_{index}",
                )
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=buttons
        + [[InlineKeyboardButton(text="Вернуться", callback_data=menu_service.BACK_TO_MENU)]]
    )


def explore_event_keyboard(options: list[dict[str, str]]) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []
    for option in options:
        callback = option.get("callback") or f"explore_choice_{option['id']}"
        buttons.append([InlineKeyboardButton(text=option["label"], callback_data=callback)])
    if not any(option.get("callback") == menu_service.BACK_TO_MENU for option in options):
        buttons.append([InlineKeyboardButton(text="Вернуться", callback_data=menu_service.BACK_TO_MENU)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def profile_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отдохнуть", callback_data="profile_rest")],
            [InlineKeyboardButton(text="Использовать аптечку", callback_data="profile_medkit")],
            [InlineKeyboardButton(text="Вернуться", callback_data=menu_service.BACK_TO_MENU)],
        ]
    )


def inventory_inline_keyboard(items: list[dict[str, object]]) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []
    for item in items:
        item_id = item["id"]
        if item["type"] == "weapon":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"Экипировать: {item['name']}",
                        callback_data=f"inventory_equip_{item_id}",
                    )
                ]
            )
        elif item["type"] == "consumable":
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"Использовать: {item['name']}",
                        callback_data=f"inventory_use_{item_id}",
                    )
                ]
            )
    buttons.append([InlineKeyboardButton(text="Вернуться", callback_data=menu_service.BACK_TO_MENU)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def faction_inline_keyboard(available: list[str]) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"Вступить: {faction}",
                callback_data=f"faction_join_{faction}",
            )
        ]
        for faction in available
    ]
    buttons.append([InlineKeyboardButton(text="Вернуться", callback_data=menu_service.BACK_TO_MENU)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def raid_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать рейд", callback_data="raid_create")],
            [InlineKeyboardButton(text="Присоединиться", callback_data="raid_join")],
            [InlineKeyboardButton(text="Вернуться", callback_data=menu_service.BACK_TO_MENU)],
        ]
    )


def help_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Правила", callback_data="help_rules")],
            [InlineKeyboardButton(text="FAQ", callback_data="help_faq")],
            [InlineKeyboardButton(text="Подсказки", callback_data="help_tips")],
            [InlineKeyboardButton(text="Вернуться", callback_data=menu_service.BACK_TO_MENU)],
        ]
    )
