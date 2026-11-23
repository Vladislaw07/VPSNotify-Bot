import asyncio
from aiogram import Router
from aiogram import types
from services import queries_service
from aiogram.filters.command import Command
from typing import Any
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from utils import clear_old_msg
import logging

logger = logging.getLogger(__name__)

router = Router()

async def send_stats(vps_list : list[Any] | None, owner_id : int) -> str:
    all_vps: int = 0
    expired_vps: int = 0
    if vps_list:
        for vps in vps_list:
            all_vps += 1
            info: dict[str,Any] | None = await asyncio.to_thread(queries_service.get_vps_info,owner_id=owner_id,ip=vps)
            if not info:
                continue
            reminded : bool = info["reminded"] if info else False
            if reminded:
                expired_vps += 1
    stats_text: str = f"""
<blockquote>📊 Статистика</blockquote>
🖥 Усього VPS: <b>{all_vps}</b>
🔴 Прострочені: <b>{expired_vps}</b>
"""
    return stats_text

@router.message(Command("stats"))
async def stats_command(message:types.Message, state:FSMContext):
    await clear_old_msg(state)
    await state.clear()
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    vps_list :list[Any] | None = await asyncio.to_thread(queries_service.list_vps, owner_id=message.from_user.id)
    await message.answer(text=await send_stats(vps_list=vps_list,owner_id=message.from_user.id), reply_markup=ReplyKeyboardRemove())
