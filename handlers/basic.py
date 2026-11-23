from aiogram import Router
from aiogram.filters.command import Command
from aiogram import types
from texts import user_messages
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from utils import clear_old_msg

router: Router = Router()

@router.message(Command("start"))
async def basic_start(message: types.Message, state:FSMContext):
    await clear_old_msg(state)
    await state.clear()
    await message.answer(user_messages.START_TEXT,reply_markup=ReplyKeyboardRemove())

@router.message(Command("help"))
async def basic_help(message: types.Message, state:FSMContext):
    await clear_old_msg(state)
    await state.clear()
    await message.answer(user_messages.HELP_TEXT,reply_markup=ReplyKeyboardRemove())

@router.message(Command("cancel"))
async def basic_cancel(message: types.Message, state:FSMContext):
    await clear_old_msg(state)
    await state.clear()
    await message.answer(user_messages.CANCEL_ACTION_TEXT,reply_markup=ReplyKeyboardRemove())
