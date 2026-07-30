import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bot.services.llm import generate_story
from bot.states import StoryForm

router = Router()


def split_text(text: str, max_length: int = 4000) -> list[str]:
    parts = []
    current = ""

    for paragraph in text.split("\n"):
        if len(current) + len(paragraph) + 1 <= max_length:
            current += paragraph + "\n"
        else:
            if current:
                parts.append(current.strip())

            current = paragraph + "\n"

    if current:
        parts.append(current.strip())

    return parts


def get_end_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✨ Новое приключение героя",
                    callback_data="new_hero_adventure",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎨 Новая тема",
                    callback_data="new_theme",
                )
            ],
            [
                InlineKeyboardButton(
                    text="👶 Другой ребёнок",
                    callback_data="another_child",
                )
            ],
        ]
    )


def get_error_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Попробовать ещё раз",
                    callback_data="retry_story",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 В начало",
                    callback_data="start_again",
                )
            ],
        ]
    )


async def send_story_end_menu(message: Message) -> None:
    await message.answer(
        "🌟 Сказка закончилась!\n\n"
        "Что хотите сделать дальше?",
        reply_markup=get_end_keyboard(),
    )


async def send_progress_messages(
    message: Message,
    stop_event: asyncio.Event,
) -> None:
    await message.answer(
        "✨ Придумываю сказку..."
    )

    await asyncio.sleep(12)

    if stop_event.is_set():
        return

    await message.answer(
        "⏳ Создаю волшебный мир..."
    )

    await asyncio.sleep(12)

    if stop_event.is_set():
        return

    await message.answer(
        "🪄 Почти готово..."
    )


async def generate_and_send_story(
    message: Message,
    state: FSMContext,
    story_theme: str | None = None,
) -> None:
    data = await state.get_data()

    stop_event = asyncio.Event()

    progress_task = asyncio.create_task(
        send_progress_messages(
            message,
            stop_event,
        )
    )

    try:
        story = await generate_story(
            child_name=data.get("child_name"),
            child_age=data.get("child_age"),
            story_theme=story_theme or data.get("story_theme"),
            avoid_topics=data.get(
                "avoid_topics",
                "Не указано",
            ),
        )

        stop_event.set()
        progress_task.cancel()

        await state.update_data(
            full_story=story
        )

        for chunk in split_text(story):
            await message.answer(chunk)

        await send_story_end_menu(message)

    except Exception as error: #noqa: BLE001
        stop_event.set()
        progress_task.cancel()

        print(
            f"Ошибка генерации сказки: {error}"
        )

        await message.answer(
            "❌ Не удалось создать сказку.\n\n"
            "Попробуйте ещё раз.",
            reply_markup=get_error_keyboard(),
        )

@router.callback_query(
    StoryForm.preview,
    F.data == "create_story",
)
async def create_story_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    await generate_and_send_story(
        message=callback.message,
        state=state,
    )


@router.callback_query(
    F.data == "retry_story",
)
async def retry_story_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    await generate_and_send_story(
        message=callback.message,
        state=state,
    )


@router.callback_query(
    F.data == "start_again",
)
async def start_again_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.clear()

    await state.set_state(
        StoryForm.child_name
    )

    await callback.message.answer(
        "👶 Как зовут вашего ребёнка?"
    )


@router.callback_query(
    F.data == "new_hero_adventure",
)
async def new_hero_adventure_handler(
    callback: CallbackQuery,
) -> None:
    await callback.answer(
        "Эта возможность скоро появится 🌟",
        show_alert=True,
    )


@router.callback_query(
    F.data == "new_theme",
)
async def new_theme_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.set_state(
        StoryForm.new_theme
    )

    await callback.message.answer(
        "🎨 Какая новая тема должна быть в сказке?"
    )


@router.message(
    StoryForm.new_theme,
    F.text,
)
async def process_new_theme(
    message: Message,
    state: FSMContext,
) -> None:
    await state.update_data(
        story_theme=message.text.strip()
    )

    await state.set_state(
        StoryForm.avoid_topics
    )

    await message.answer(
        "Есть ли темы, персонажи или события, "
        "которые нужно исключить?"
    )


@router.callback_query(
    F.data == "another_child",
)
async def another_child_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.answer()

    await state.clear()

    await state.set_state(
        StoryForm.child_name
    )

    await callback.message.answer(
        "👶 Как зовут вашего ребёнка?"
    )