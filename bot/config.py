import os

from dotenv import load_dotenv

# Загружаем переменные из файла .env, если он существует
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")

if not GEMINI_API_KEY:
    raise ValueError("Переменная окружения GEMINI_API_KEY не задана!")