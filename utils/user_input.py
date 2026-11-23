from aiogram import types
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import ipaddress
import logging

logger = logging.getLogger(__name__)

async def get_ip_func(message:types.Message) -> bool:
        if not message.text:
                logger.error("Error: message.text is None")
                return False
        try:
           _: ipaddress.IPv4Address | ipaddress.IPv6Address = ipaddress.ip_address(message.text.strip())
        except ValueError:
            logger.error("Error: ip is invalid")
            return False
        return True

async def valid_ip(valid:bool, message:types.Message, state:FSMContext, second_state:State) -> bool:
    if valid:
        ip:str | None = message.text.strip() if message.text else None
        if isinstance(ip, str):
            await state.update_data(ip=ip)
            await state.set_state(second_state)
            return True
    return False

async def get_rent_end_func(message:types.Message) -> str | None:
    if not message.text:
                logger.error("Error: message.text is None")
                return None
    date: str | None = None
    for fmt in ["%d.%m.%Y", "%d.%m.%y"]:
        try:
            rent_end: datetime = datetime.strptime(message.text.strip(), fmt)
            date = rent_end.strftime("%d.%m.%Y")
            break
        except ValueError:
            continue
    return date if date else None
