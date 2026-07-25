from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.services.llm import generate_story
from bot.states import StoryForm

router = Router()


def split_text(text: str, max_length: int = 4000) -> list[str]:
    """
    Разбивает длинный текст на части для отправки в Telegram.
    Старается резать по абзацам.
    """
    parts = []
    current = ""

    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 1 <= max_length:
            current += paragraph + "\n"
        else:
            if current:
                parts.append(current.strip())

            current = paragraph + "\n"

    if current:
        parts.append(current.strip())

    return parts


@router.callback_query(StoryForm.preview, F.data == "create_story")
async def create_story_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Создание персональной сказки через Gemini.
    """

    await callback.answer()

    data = await state.get_data()

    child_name = data.get("child_name")
    child_age = data.get("child_age")
    story_theme = data.get("story_theme")
    avoid_topics = data.get("avoid_topics", "Не указано")

    await callback.message.answer(
        "✨ Придумываю сказку...\n\nЭто может занять немного времени."
    )

    try:
        story = await generate_story(
            child_name=child_name,
            child_age=child_age,
            story_theme=story_theme,
            avoid_topics=avoid_topics,
        )

        # Сохраняем сказку в FSM (на будущее для кнопки "читать дальше")
        await state.update_data(full_story=story)

        chunks = split_text(story)

        for chunk in chunks:
            await callback.message.answer(chunk)

    except Exception as e: #noqa: BLE001
        await callback.message.answer(
            "Не удалось создать сказку. Попробуйте позже."
        )
        print(f"Ошибка генерации сказки: {e}")

        await callback.message.answer(
            "❌ Не удалось создать сказку. Попробуйте позже."
        )