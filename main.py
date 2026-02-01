import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from app.services import menu as menu_service
from app.ui import keyboards, messages

BOT_TOKEN = "8375612756:AAETA9v_wzZSXvKso6utmUpzJNHQCp-iXOE"


async def send_menu(message: Message) -> None:
    builder = keyboards.build_menu_keyboard(menu_service.MENU_BUTTONS)
    await message.answer(
        messages.format_main_menu(),
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


async def show_profile(message: Message) -> None:
    await message.answer(messages.format_profile(menu_service.PROFILE))


async def show_inventory(message: Message) -> None:
    await message.answer(
        messages.format_inventory(
            menu_service.INVENTORY["items"],
            menu_service.INVENTORY["empty_message"],
        )
    )


async def show_locations(message: Message) -> None:
    await message.answer(
        messages.format_locations(menu_service.LOCATIONS),
        reply_markup=keyboards.explore_inline_keyboard(),
    )


async def show_raid(message: Message) -> None:
    await message.answer(
        messages.format_raid_title(),
        reply_markup=keyboards.raid_inline_keyboard(),
    )


async def show_faction(message: Message) -> None:
    await message.answer(messages.format_faction(menu_service.FACTION_STATUS))


async def show_help(message: Message) -> None:
    await message.answer(messages.format_help(menu_service.HELP_LINES))


async def on_menu_choice(message: Message) -> None:
    text = message.text or ""
    action = menu_service.resolve_menu_choice(text)
    if action == "profile":
        await show_profile(message)
    elif action == "explore":
        await message.answer(
            messages.format_explore_prompt(),
            reply_markup=keyboards.explore_inline_keyboard(),
        )
    elif action == "locations":
        await show_locations(message)
    elif action == "raid":
        await show_raid(message)
    elif action == "faction":
        await show_faction(message)
    elif action == "inventory":
        await show_inventory(message)
    elif action == "help":
        await show_help(message)
    else:
        await send_menu(message)


async def handle_callback(callback: CallbackQuery) -> None:
    data = callback.data or ""
    result = menu_service.resolve_callback(data)
    if result.action == "menu":
        if callback.message:
            await send_menu(callback.message)
    else:
        if callback.message and result.text:
            await callback.message.answer(result.text)
    await callback.answer()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.message.register(send_menu, CommandStart())
    dp.message.register(on_menu_choice, F.text.in_(menu_service.MENU_BUTTONS))
    dp.message.register(send_menu)
    dp.callback_query.register(handle_callback)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
