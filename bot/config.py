import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env, если он существует
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")
