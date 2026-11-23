from aiogram.fsm.context import FSMContext
from aiogram import types
import logging

logger = logging.getLogger(__name__)

async def clear_old_msg(state:FSMContext):
    data = await state.get_data()
    old_msg = data.get("old_msg")
    if old_msg and isinstance(old_msg, types.Message):
        try:
            await old_msg.delete()
        except:
            pass
