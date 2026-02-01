import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = "8375612756:AAETA9v_wzZSXvKso6utmUpzJNHQCp-iXOE"

MENU_BUTTONS = [
    "Профиль",
    "Вылазка",
    "Локации",
    "Рейд",
    "Группировка",
    "Инвентарь",
    "Помощь",
]


async def build_menu() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    for label in MENU_BUTTONS:
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


async def send_menu(message: Message) -> None:
    builder = await build_menu()
    await message.answer(
        "Главное меню:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


async def show_profile(message: Message) -> None:
    await message.answer(
        "Профиль сталкера:\n"
        "Уровень: 1\n"
        "Здоровье: 100\n"
        "Радиация: 0\n"
        "Репутация: нейтрал",
    )


async def show_inventory(message: Message) -> None:
    await message.answer("Инвентарь пуст. Найди припасы в вылазке!")


async def show_locations(message: Message) -> None:
    await message.answer(
        "Доступные локации:\n"
        "- Кордон\n"
        "- Свалка\n"
        "- Бар",
        reply_markup=explore_inline_keyboard(),
    )


async def show_raid(message: Message) -> None:
    await message.answer("Рейды", reply_markup=raid_inline_keyboard())


async def show_faction(message: Message) -> None:
    await message.answer(
        "Ты пока не вступил в группировку.\n"
        "Выбери сторону позже, когда заработаешь репутацию.",
    )


async def show_help(message: Message) -> None:
    await message.answer(
        "Кнопки меню запускают основные действия.\n"
        "Инлайн-кнопки помогают выбирать решения в событиях.",
    )


async def on_menu_choice(message: Message) -> None:
    text = message.text or ""
    if text == "Профиль":
        await show_profile(message)
    elif text == "Вылазка":
        await message.answer(
            "Ты выходишь в Зону. Куда направимся?",
            reply_markup=explore_inline_keyboard(),
        )
    elif text == "Локации":
        await show_locations(message)
    elif text == "Рейд":
        await show_raid(message)
    elif text == "Группировка":
        await show_faction(message)
    elif text == "Инвентарь":
        await show_inventory(message)
    elif text == "Помощь":
        await show_help(message)
    else:
        await send_menu(message)


async def handle_callback(callback: CallbackQuery) -> None:
    data = callback.data or ""
    if data == "explore_anomaly":
        await callback.message.answer(
            "Аномалия впереди. Ты кидаешь болт и замечаешь артефакт.",
        )
    elif data == "explore_area":
        await callback.message.answer("Ты находишь тайник с патронами.")
    elif data == "raid_create":
        await callback.message.answer("Рейд создан. Ожидаем напарников.")
    elif data == "raid_join":
        await callback.message.answer("Ты присоединился к рейду.")
    elif data == "back_to_menu":
        if callback.message:
            await send_menu(callback.message)
    await callback.answer()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.message.register(send_menu, CommandStart())
    dp.message.register(on_menu_choice, F.text.in_(MENU_BUTTONS))
    dp.message.register(send_menu)
    dp.callback_query.register(handle_callback)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
