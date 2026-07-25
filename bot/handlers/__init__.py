from aiogram import Router

from .start import router as start_router
from .story import router as story_router

router = Router()

# Объединяем роутеры из отдельных файлов
router.include_routers(start_router, story_router)
