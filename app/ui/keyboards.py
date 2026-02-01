from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def build_menu_keyboard(buttons: list[str]) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    for label in buttons:
        builder.button(text=label)
    builder.adjust(2, 2, 2, 1)
    return builder


def explore_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Проверить аномалию", callback_data="explore_anomaly")],
            [InlineKeyboardButton(text="Осмотреть окрестности", callback_data="explore_area")],
            [InlineKeyboardButton(text="Вернуться", callback_data="back_to_menu")],
        ]
    )


def raid_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать рейд", callback_data="raid_create")],
            [InlineKeyboardButton(text="Присоединиться", callback_data="raid_join")],
            [InlineKeyboardButton(text="Вернуться", callback_data="back_to_menu")],
        ]
    )
