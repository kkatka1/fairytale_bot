from google import genai
from bot.config import GEMINI_API_KEY
from bot.prompts.story_prompt import build_story_prompt

# Инициализация клиента Gemini API через официальный SDK google-genai
client = genai.Client(api_key=GEMINI_API_KEY)

# Используем актуальную модель
MODEL_NAME = "gemini-3.5-flash"

async def generate_story(
    child_name: str,
    child_age: str,
    story_theme: str,
    avoid_topics: str = "Не указано",
    style_key: str = "classic_russian"
) -> str:
    """
    Публичная функция для генерации сказки:
    - вызывает только build_story_prompt();
    - отправляет запрос в Gemini API;
    - возвращает готовый текст сказки.
    """
    prompt = build_story_prompt(
        child_name=child_name,
        child_age=child_age,
        story_theme=story_theme,
        avoid_topics=avoid_topics,
        style_key=style_key,
    )

    response = await client.aio.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    if response and response.text:
        return response.text.strip()
    
    raise ValueError("Не удалось получить текст сказки от Gemini API.")
