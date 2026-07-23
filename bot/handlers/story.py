from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.states import StoryForm

router = Router()

@router.callback_query(StoryForm.preview, F.data == "create_story")
async def create_story_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик кнопки «📖 Создать сказку».
    Подготовлен для интеграции AI на следующем этапе с сохранением FSM архитектуры.
    """
    await callback.answer()
    
    # Получаем все данные из FSM (будут использованы на следующем этапе для запроса к AI)
    story_data = await state.get_data()
    
    # В будущем здесь будет:
    # 1. Запрос к AI с использованием story_data
    # 2. Сохранение полной сказки в FSM или отправка первых двух абзацев
    # 3. Добавление кнопки «📖 Читать дальше»
    
    # Временная заглушка согласно ТЗ:
    await callback.message.answer("Генерация сказки будет реализована на следующем этапе.")
