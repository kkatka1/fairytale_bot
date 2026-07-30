from aiogram.fsm.state import State, StatesGroup


class StoryForm(StatesGroup):
    """
    Состояния FSM для создания сказки.
    """

    child_name = State()
    child_age = State()
    story_theme = State()
    avoid_topics = State()
    preview = State()

    # Новая тема после завершения сказки
    new_theme = State()