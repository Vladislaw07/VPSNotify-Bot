import asyncio
from .router import router
from aiogram.filters.command import Command
from aiogram import types
from aiogram.fsm.context import FSMContext
from services import queries_service
from texts import user_messages, error_messages
from typing import Any
from states import check_list
from utils import clear_old_msg
import logging
from models import VPS, vps_class_builder
from keyboards.my_vps_list_keyboard import list_keyboard
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove

logger = logging.getLogger(__name__)

async def show_all_vps(message:types.Message, state:FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    if not user_id:
        logger.error("Error: user_id from data is None")
        return
    vps_list :list[Any] | None = await asyncio.to_thread(queries_service.list_vps, owner_id=user_id)
    if not vps_list:
        try:
            await message.answer(error_messages.NO_HAVE_LIST_TEXT, reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            logger.warning("Warning: message not delivered | chat_id=%s | %s", user_id, e)
        await state.clear()
        return
    servers:list[VPS] = []
    for vps_ip in vps_list:
        info: dict[str,Any] | None = await asyncio.to_thread(queries_service.get_vps_info,owner_id=user_id, ip=vps_ip)
        if info is None:
            continue
        vps_server: VPS = await vps_class_builder(owner_id=user_id,ip=vps_ip,login=info["login"],password=info["password"],rent_end=info["rent_end"],project_name=info["project_name"],reminded=info["reminded"])
        servers.append(vps_server)
    if not servers:
        try:
            await message.answer(error_messages.ERROR_INFO_TEXT, reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            logger.warning("Warning: message not delivered | chat_id=%s | %s", user_id, e)
        await state.clear()
        return
    kb = list_keyboard(servers=servers)
    await state.clear()
    try:
        old_msg = await message.answer(user_messages.SELECT_VPS_TEXT, reply_markup=kb)
        await state.update_data(old_msg=old_msg)
    except Exception as e:
            logger.warning("Warning: message not delivered | chat_id=%s | %s", user_id, e)


@router.message(Command("list_vps"))
async def list_vps_command(message:types.Message, state:FSMContext):
    current_state = await state.get_state()
    if current_state == check_list.show_list:
        return
    await clear_old_msg(state=state)
    await state.clear()
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    await state.set_state(check_list.show_list)
    await show_all_vps(message=message, state=state)
