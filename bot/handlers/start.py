from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from bot.states import StoryForm

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /start. Сбрасывает состояние и запрашивает имя ребёнка.
    """
    await state.clear()
    await state.set_state(StoryForm.child_name)
    await message.answer(
        "Привет! Я бот для создания персональных сказок.\n\n"
        "Как зовут вашего ребёнка?",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(StoryForm.child_name, F.text)
async def process_child_name(message: Message, state: FSMContext) -> None:
    """
    Получение имени ребёнка и запрос возраста.
    """
    await state.update_data(child_name=message.text.strip())
    await state.set_state(StoryForm.child_age)
    await message.answer("Сколько лет ребёнку?")


@router.message(StoryForm.child_age, F.text)
async def process_child_age(message: Message, state: FSMContext) -> None:
    """
    Получение возраста ребёнка и запрос темы сказки.
    """
    await state.update_data(child_age=message.text.strip())
    await state.set_state(StoryForm.story_theme)
    await message.answer("Какая тема или сюжет должны быть в сказке?")


@router.message(StoryForm.story_theme, F.text)
async def process_story_theme(message: Message, state: FSMContext) -> None:
    """
    Получение темы сказки и запрос информации о том, чего следует избегать (с кнопкой «Пропустить»).
    """
    await state.update_data(story_theme=message.text.strip())
    await state.set_state(StoryForm.avoid_topics)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏩ Пропустить", callback_data="skip_avoid")]
        ]
    )
    await message.answer(
        "Какие темы, персонажей или моменты нужно избегать в сказке?\n"
        "Если избегать нечего, нажмите кнопку «Пропустить».",
        reply_markup=keyboard
    )


@router.callback_query(StoryForm.avoid_topics, F.data == "skip_avoid")
async def skip_avoid_topics(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Пропуск шага с избегаемыми темами.
    """
    await callback.answer()
    await state.update_data(avoid_topics="Не указано")
    await show_preview(callback.message, state)


@router.message(StoryForm.avoid_topics, F.text)
async def process_avoid_topics(message: Message, state: FSMContext) -> None:
    """
    Получение информации о том, чего следует избегать.
    """
    await state.update_data(avoid_topics=message.text.strip())
    await show_preview(message, state)


async def show_preview(message: Message, state: FSMContext) -> None:
    """
    Показывает экран подтверждения (превью) с введённой информацией и кнопками управления.
    """
    await state.set_state(StoryForm.preview)
    data = await state.get_data()

    child_name = data.get("child_name")
    child_age = data.get("child_age")
    story_theme = data.get("story_theme")
    avoid_topics = data.get("avoid_topics")

    text = (
        "📖 <b>Проверьте введённые данные:</b>\n\n"
        f"• <b>Имя ребёнка:</b> {child_name}\n"
        f"• <b>Возраст:</b> {child_age}\n"
        f"• <b>Тема сказки:</b> {story_theme}\n"
        f"• <b>Что нужно избегать:</b> {avoid_topics}\n\n"
        "Всё верно?"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Создать сказку", callback_data="create_story")],
            [InlineKeyboardButton(text="✏️ Изменить данные", callback_data="edit_data")]
        ]
    )

    # Если вызов был из CallbackQuery, message может быть объектом Message
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(StoryForm.preview, F.data == "edit_data")
async def edit_data_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик кнопки «✏️ Изменить данные» — возвращает к первому вопросу (имя ребёнка).
    """
    await callback.answer()
    await state.set_state(StoryForm.child_name)
    await callback.message.answer("Давайте начнем сначала. Как зовут вашего ребёнка?")
