import asyncio
from services import queries_service
from .router import router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from states import get_parameters, add_vps
from texts import get_parameters_messages, error_messages, vps_info_messages
from aiogram import types
from utils import clear_old_msg, get_ip_func, valid_ip, get_rent_end_func
from typing import Any
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
import logging

logger = logging.getLogger(__name__)

async def add_vps_func(message:types.Message, state:FSMContext):
    await clear_old_msg(state=state)
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    data = await state.get_data()
    owner_id = data.get("owner_id")
    ip = data.get("ip")
    login = data.get("login")
    password = data.get("password")
    rent_end = data.get("rent_end")
    project_name = data.get("project_name")
    if not (
    isinstance(owner_id, int) and
    isinstance(ip, str) and
    isinstance(login, str) and
    isinstance(password, str) and
    isinstance(rent_end, str) and
    isinstance(project_name, str)
):
        logger.error("Error: incompatible variable type | owner_id=%s | ip=%s | login=%s | password=%s | rent_end=%s | project_name=%s |",owner_id, ip, login, password, rent_end, project_name)
        return
    try:
        await asyncio.to_thread(queries_service.add_vps, owner_id=owner_id, ip=ip, login=login, password=password, rent_end=rent_end, project_name=project_name)
    except Exception as e:
        logger.error("Error: operation 'queries_service.add_vps' invalid | %s", e)
        try:
            await message.answer(error_messages.ERROR_ADD_VPS_TEXT)
        except Exception as e:
            logger.warning("Warning: message not delivered | chat_id=%s | %s", message.from_user.id, e)
        await state.clear()
        return
    try:
        await message.answer(vps_info_messages.VPS_ADDED_TEXT)
    except Exception as e:
        logger.warning("Warning: message not delivered | chat_id=%s | %s", message.from_user.id, e)
    await state.clear()

@router.message(Command("add_vps"))
async def add_vps_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == add_vps.adding_vps:
        return
    await clear_old_msg(state)
    await state.clear()
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    owner_id = message.from_user.id
    await state.update_data(owner_id=owner_id)
    await state.set_state(get_parameters.get_ip)
    try:
        await message.answer(get_parameters_messages.GET_IP_TEXT, reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        logger.warning("Warning: message not delivered | chat_id=%s | %s", owner_id, e)
        return

@router.message(get_parameters.get_ip)
async def get_ip(message:types.Message, state:FSMContext):
    await clear_old_msg(state=state)
    if not message.text:
        logger.error("Error: message.text is None")
        return
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    info: dict[str,Any] | None = await asyncio.to_thread(queries_service.get_vps_info,owner_id=message.from_user.id,ip=message.text.strip())
    if info:
        try:
            await message.answer(error_messages.DUPLICATE_VPS_TEXT)
        except Exception as e:
            logger.warning("Warning: message not delivered | chat_id=%s | %s", message.from_user.id, e)
        return
    valid = await get_ip_func(message=message)
    if await valid_ip(valid=valid,message=message,state=state,second_state=get_parameters.get_login) is False:
        await message.answer(error_messages.INVALID_VPS_IP_TRY_AGAIN_TEXT)
        return
    try:
        await message.answer(get_parameters_messages.GET_LOGIN_TEXT)
    except Exception as e:
        logger.warning("Warning: message not delivered | chat_id=%s | %s", message.from_user.id, e)
        return

@router.message(get_parameters.get_login)
async def get_login(message:types.Message, state:FSMContext):
    await clear_old_msg(state=state)
    if not message.text:
        logger.error("Error: message.text is None")
        return
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    await state.update_data(login=message.text.strip())
    await state.set_state(get_parameters.get_password)
    try:
        await message.answer(get_parameters_messages.GET_PASSWORD_TEXT)
    except Exception as e:
        logger.warning("Warning: message not delivered | chat_id=%s | %s", message.from_user.id, e)
        return

@router.message(get_parameters.get_password)
async def get_password(message:types.Message, state:FSMContext):
    await clear_old_msg(state=state)
    if not message.text:
        logger.error("Error: message.text is None")
        return
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    await state.update_data(password=message.text.strip())
    await state.set_state(get_parameters.get_rent_end)
    try:
        await message.answer(get_parameters_messages.GET_RENT_END_TEXT)
    except Exception as e:
        logger.warning("Warning: message not delivered | chat_id=%s | %s", message.from_user.id, e)
        return

@router.message(get_parameters.get_rent_end)
async def get_rent_end(message:types.Message, state:FSMContext):
    await clear_old_msg(state=state)
    if not message.text:
        logger.error("Error: message.text is None")
        return
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    date: str | None = await get_rent_end_func(message=message)
    if date is None:
        await message.answer(error_messages.INVALID_FORMAT_TEXT)
        return
    await state.update_data(rent_end=date)
    await state.set_state(get_parameters.get_project_name)
    try:
        await message.answer(get_parameters_messages.GET_PROJECT_NAME_TEXT)
    except Exception as e:
        logger.warning("Warning: message not delivered | chat_id=%s | %s", message.from_user.id, e)
        return

@router.message(get_parameters.get_project_name)
async def get_project_name(message:types.Message, state:FSMContext):
    await clear_old_msg(state=state)
    if not message.text:
        logger.error("Error: message.text is None")
        return
    if not message.from_user:
        logger.error("Error: message.from_user is None")
        return
    project_name = message.text.strip()
    await state.update_data(project_name=project_name)
    await state.set_state(add_vps.adding_vps)
    await add_vps_func(message=message, state=state)
