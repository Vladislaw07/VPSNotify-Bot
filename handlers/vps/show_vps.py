import asyncio
from .router import router
from aiogram.types import CallbackQuery
from models import VPS, vps_class_builder
from aiogram import F
from typing import Any
from texts import error_messages
from aiogram import types
from texts import vps_info_messages
from services import queries_service
import logging
from utils import clear_old_msg
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove

logger = logging.getLogger(__name__)

@router.callback_query(F.data.startswith("vps:"))
async def show_vps_info(callback:CallbackQuery, state:FSMContext):
    await clear_old_msg(state=state)
    await state.clear()
    await callback.answer()
    if not callback.data:
        logger.error("Error: callback.data is None")
        return
    if not isinstance(callback.message, types.Message):
        logger.error("Error: callback.message type is not Message")
        return
    if not callback.from_user:
        logger.error("Error: callback.from_user is None")
        return
    ip = callback.data.removeprefix("vps:")
    if not ip:
        logger.error("Error: ip type is not str or None")
        return
    vps_server : VPS | None = None
    try:
        info: dict[str,Any] | None = await asyncio.to_thread(queries_service.get_vps_info,owner_id=callback.from_user.id, ip=ip)
        if not info:
            logger.error("Error: info is None")
            return
        vps_server = await vps_class_builder(owner_id=callback.from_user.id,ip=ip,login=info["login"],password=info["password"],rent_end=info["rent_end"],project_name=info["project_name"],reminded=info["reminded"])
    except Exception as e:
        logger.error("Error: operation 'vps_class_builder' invalid | %s", e)
    if not vps_server:
        try:
            await callback.message.answer(error_messages.ERROR_INFO_TEXT, reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            logger.warning("Warning: message not delivered | chat_id=%s | %s", callback.from_user.id, e)
        logger.error("Error: vps_server is None")
        await state.clear()
        return
    try:
        await callback.message.answer(vps_info_messages.VPS_INFO_TEXT.substitute(project_name=vps_server.project_name,ip=vps_server.ip, login=vps_server.login, password=vps_server.password, rent_end=vps_server.rent_end), reply_markup=ReplyKeyboardRemove())
    except Exception as e:
            logger.warning("Warning: message not delivered | chat_id=%s | %s", callback.from_user.id, e)
    await state.clear()
