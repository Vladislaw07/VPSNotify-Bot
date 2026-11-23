import asyncio
from .router import router
from aiogram.filters.command import Command, CommandObject
from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from aiogram.fsm.context import FSMContext
from texts import vps_info_messages, error_messages
from services import queries_service
from utils import clear_old_msg
from keyboards.confirmation_to_delete_keyboard import confirmation_keyboard
from states import delete_vps
from typing import Any
from aiogram import F
import logging

logger = logging.getLogger(__name__)

async def deleting_vps(message:types.Message, state:FSMContext):
    data = await state.get_data()
    ip = data.get("ip")
    if not isinstance(ip, str):
        logger.error("Error: invalid format of ip")
        await state.clear()
        return
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        await state.clear()
        return
    try:
        await asyncio.to_thread(queries_service.delete_vps, owner_id=message.from_user.id, ip=ip)
        await message.answer(vps_info_messages.VPS_DELETED_TEXT, reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        logger.error("Error: operation 'queries_service.delete_vps' invalid | %s", e)
    await state.clear()

@router.message(Command("delete_vps"))
async def delete_vps_command(message:types.Message, command:CommandObject, state:FSMContext):
    current_state = await state.get_state()
    if current_state == delete_vps.deleting_vps:
        return
    await clear_old_msg(state=state)
    await state.clear()
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    ip = command.args
    if not isinstance(ip, str):
        logger.warning("Warning: invalid format of ip")
        return
    await state.update_data(ip=ip)
    try:
        info: dict[str, Any] | None = await asyncio.to_thread(queries_service.get_vps_info,owner_id=message.from_user.id,ip=ip)
        if info is None:
            logger.error("Error: info about VPS absent")
            await message.answer(error_messages.INVALID_VPS_IP_TEXT, reply_markup=ReplyKeyboardRemove())
            await state.clear()
            return
        kb = confirmation_keyboard()
        await message.answer(vps_info_messages.VPS_DELETE_TEXT.substitute(project_name=info["project_name"]), reply_markup=kb)
        await state.set_state(delete_vps.confirmation_to_delete)
    except Exception as e:
        logger.error("Error: operation denied | %s", e)

@router.message(delete_vps.confirmation_to_delete, F.text.in_({"Так", "Ні"}))
async def confirmation_to_delete(message:types.Message, state:FSMContext):
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    if message.text == "Ні":
        try:
            await message.answer(text=" ", reply_markup=ReplyKeyboardRemove())
            await state.clear()
        except Exception as e:
            logger.warning("Warning: message not delivered | chat_id=%s | %s", message.from_user.id, e)
        return
    elif message.text == "Так":
        await state.set_state(delete_vps.deleting_vps)
        await deleting_vps(message=message, state=state)
