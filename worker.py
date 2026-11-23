import asyncio
from typing import Any
from aiogram import Bot
from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import timedelta
from services import queries_service, worker_service
from models import VPS, vps_class_builder
from html import escape
import logging

logger = logging.getLogger(__name__)
KYIV_TZ : ZoneInfo = ZoneInfo("Europe/Kyiv")

async def send_remind(bot: Bot, chat_id: int, vps: VPS):
    rent_end = datetime.strptime(vps.rent_end, "%d.%m.%Y")
    rent_end_date = rent_end.strftime("%d.%m.%Y")
    message = ("🔔 Нагадування!\n\n"
    f"🖥 <b>{escape(vps.project_name)}</b>\n"
    f"🌐 IP: <code>{escape(vps.ip)}</code>\n"
    f"👤 Логін: <code>{escape(vps.login)}</code>\n"
    f"🔑 Пароль: <code>{escape(vps.password)}</code>\n"
    f"📅 Аренда закінчується <b>ЗАВТРА</b> <i>{escape(rent_end_date)}</i>\n"
    "<blockquote>Продовжи аренду або перенеси проект</blockquote>")
    await bot.send_message(chat_id=chat_id,text=message)

async def worker(bot: Bot):
    while True:

        try:
            now = datetime.now(tz=KYIV_TZ).date()
            tomorrow = now + timedelta(days=1)
            all_vps :list[Any] | None = await asyncio.to_thread(worker_service.get_all_vps)
            if all_vps:
                for vps in all_vps:
                    info: dict[str,Any] | None = await asyncio.to_thread(queries_service.get_vps_info,owner_id=vps[0],ip=vps[1])
                    if info is None:
                        continue
                    rent_end = datetime.strptime(info["rent_end"], "%d.%m.%Y")
                    if rent_end.date() != tomorrow and bool(info["reminded"]):
                        await asyncio.to_thread(worker_service.update_reminded,reminded=False,owner_id=vps[0],ip=vps[1])
                        continue
                    if not bool(info["reminded"]):
                        if rent_end.date() != tomorrow:
                            continue
                        chat_id=vps[0]
                        vps_server=await vps_class_builder(owner_id=vps[0],ip=vps[1],login=info["login"],password=info["password"],rent_end=info["rent_end"],project_name=info["project_name"],reminded=info["reminded"])
                        try:
                            await send_remind(bot=bot,chat_id=chat_id,vps=vps_server)
                        except Exception as e:
                            logger.warning("Warning: message not delivered | chat_id=%s | %s", chat_id, e)
                            continue
                        await asyncio.to_thread(worker_service.update_reminded,reminded=True,owner_id=vps[0],ip=vps[1])
                        continue
        except Exception as e:
            logger.exception("Exception: worker cycle failed | %s", e)

        await asyncio.sleep(60)
