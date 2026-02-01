import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from app.services import explore as explore_service
from app.services import faction as faction_service
from app.services import help as help_service
from app.services import inventory as inventory_service
from app.services import menu as menu_service
from app.services import profile as profile_service
from app.services import raid as raid_service
from app.ui import keyboards, messages

BOT_TOKEN = "8375612756:AAETA9v_wzZSXvKso6utmUpzJNHQCp-iXOE"


def get_user_id(message: Message | CallbackQuery) -> int:
    if isinstance(message, CallbackQuery):
        return message.from_user.id
    return message.from_user.id


async def send_menu(message: Message) -> None:
    builder = keyboards.build_menu_keyboard(menu_service.MENU_BUTTONS)
    await message.answer(
        messages.format_main_menu(),
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


async def show_profile(message: Message) -> None:
    profile = profile_service.get_profile(get_user_id(message))
    await message.answer(
        messages.format_profile(profile),
        reply_markup=keyboards.profile_inline_keyboard(),
    )


async def show_inventory(message: Message) -> None:
    inventory = inventory_service.get_inventory(get_user_id(message))
    await message.answer(
        messages.format_inventory(inventory),
        reply_markup=keyboards.inventory_inline_keyboard(inventory["items"]),
    )


async def show_locations(message: Message) -> None:
    await message.answer(
        messages.format_locations(explore_service.get_locations()),
        reply_markup=keyboards.explore_inline_keyboard(explore_service.get_locations()),
    )


async def show_raid(message: Message) -> None:
    overview = raid_service.get_overview()
    await message.answer(
        messages.format_raid_overview(overview),
        reply_markup=keyboards.raid_inline_keyboard(),
    )


async def show_faction(message: Message) -> None:
    status = faction_service.get_status(get_user_id(message))
    await message.answer(
        messages.format_faction(status),
        reply_markup=keyboards.faction_inline_keyboard(status["available"]),
    )


async def show_help(message: Message) -> None:
    await message.answer(
        messages.format_help(help_service.HELP_OVERVIEW_LINES),
        reply_markup=keyboards.help_inline_keyboard(),
    )


async def on_menu_choice(message: Message) -> None:
    text = message.text or ""
    action = menu_service.resolve_menu_choice(text)
    if action == "profile":
        await show_profile(message)
    elif action == "explore":
        await message.answer(
            messages.format_explore_prompt(),
            reply_markup=keyboards.explore_inline_keyboard(explore_service.get_locations()),
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
    if data == menu_service.BACK_TO_MENU:
        if callback.message:
            await send_menu(callback.message)
        await callback.answer()
        return

    if data in help_service.HELP_SECTIONS:
        section = help_service.HELP_SECTIONS[data]
        if callback.message:
            await callback.message.answer(
                messages.format_help_section(section["title"], section["lines"]),
                reply_markup=keyboards.help_inline_keyboard(),
            )
        await callback.answer()
        return

    user_id = callback.from_user.id
    handlers = (
        lambda payload: explore_service.handle_callback(payload, user_id),
        lambda payload: profile_service.handle_callback(payload, user_id),
        lambda payload: inventory_service.handle_callback(payload, user_id),
        lambda payload: faction_service.handle_callback(payload, user_id),
        lambda payload: raid_service.handle_callback(payload, user_id),
    )
    for handler in handlers:
        result = handler(data)
        if result:
            if callback.message:
                if isinstance(result, dict):
                    event_text = messages.format_explore_event(result["event"])
                    intro = result.get("message")
                    text = f"{intro}\n\n{event_text}" if intro else event_text
                    await callback.message.answer(
                        text,
                        reply_markup=keyboards.explore_event_keyboard(result["options"]),
                    )
                else:
                    await callback.message.answer(result)
            await callback.answer()
            return

    if callback.message:
        await callback.message.answer("Команда не распознана.")
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
