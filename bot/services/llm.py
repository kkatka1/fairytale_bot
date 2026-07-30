from google import genai

from bot.config import GEMINI_API_KEY
from bot.prompts.story_prompt import build_story_prompt


client = genai.Client(api_key=GEMINI_API_KEY)


PRIMARY_MODEL = "gemini-3.5-flash"
BACKUP_MODEL = "gemini-3.5-flash-lite"


async def generate_story(
    child_name: str,
    child_age: str,
    story_theme: str,
    avoid_topics: str = "Не указано",
    style_key: str = "classic_russian",
) -> str:
    """
    Генерация персональной сказки через Gemini.

    Основная модель:
    gemini-3.5-flash

    При временной ошибке Gemini
    используется запасная модель:
    gemini-3.5-flash-lite
    """

    prompt = build_story_prompt(
        child_name=child_name,
        child_age=child_age,
        story_theme=story_theme,
        avoid_topics=avoid_topics,
        style_key=style_key,
    )

    models = [
        PRIMARY_MODEL,
        BACKUP_MODEL,
    ]

    last_error = None

    for model in models:
        try:
            response = await client.aio.models.generate_content(
                model=model,
                contents=prompt,
            )

            if response and response.text:
                return response.text.strip()

        except Exception as error:
            last_error = error
            print(
                f"Ошибка модели {model}: {error}"
            )

    raise RuntimeError(
        f"Gemini не смог создать сказку: {last_error}"
    )