from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from models import VPS

def list_keyboard(servers:list[VPS]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for vps in servers:
        builder.button(text=f"🗄️ {vps.project_name} 🗄️", callback_data=f"vps:{vps.ip}")
    builder.adjust(2)
    return builder.as_markup()
