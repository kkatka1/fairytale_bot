from bot.prompts.age_groups import get_age_rules
from bot.prompts.base_rules import BASE_RULES
from bot.prompts.immersion_rules import IMMERSION_RULES
from bot.prompts.memory_rules import MEMORY_RULES
from bot.prompts.safety_rules import SAFETY_RULES
from bot.prompts.story_rules import STORY_RULES
from bot.prompts.styles import get_style_rules


def build_story_prompt(
    child_name: str,
    child_age: str,
    story_theme: str,
    avoid_topics: str = "Не указано",
    style_key: str = "classic_russian",
) -> str:
    """
    Формирует единый промпт путём объединения блоков правил и данных пользователя.
    """
    age_rules = get_age_rules(child_age)
    style_rules = get_style_rules(style_key)

    prompt = f"""{BASE_RULES.strip()}

{SAFETY_RULES.strip()}

{MEMORY_RULES.strip()}

{STORY_RULES.strip()}

{IMMERSION_RULES.strip()}

{age_rules.strip()}

{style_rules.strip()}

Данные пользователя:
- Имя ребёнка: {child_name}
- Возраст: {child_age}
- Тема сказки: {story_theme}
- Темы или персонажи, которых необходимо избегать: {avoid_topics}
"""
    return prompt.strip()
