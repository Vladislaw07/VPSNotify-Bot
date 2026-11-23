from aiogram import Bot
from aiogram.types import BotCommand

async def on_startup(bot:Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск"),
        BotCommand(command="help", description="Допомога"),
        BotCommand(command="cancel", description="Відмінити поточну дію"),
        BotCommand(command="stats", description="Статистика"),
        BotCommand(command="add_vps", description="Додати VPS"),
        BotCommand(command="list_vps", description="Показати всі VPS"),
        BotCommand(command="delete_vps", description="Видалити VPS за IP"),
    ])
