from aiogram import executor
from .loader import dp, db
from . import middlewares, filters, handlers
from .utils.notify_admins import on_startup_notify
from .utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    


from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'
    # executor.start_polling(dp, on_startup=on_startup)
  
    



