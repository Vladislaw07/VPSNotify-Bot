from database.db import get_connection
from typing import Any
import logging

logger = logging.getLogger(__name__)

def add_vps(owner_id:int, ip:str, login:str, password:str, rent_end:str, project_name:str) -> None:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""INSERT INTO VPS_SERVERS (OWNER_ID, IP, LOGIN, PASSWORD, RENT_END, PROJECT_NAME)
                    VALUES(?, ?, ?, ?, ?, ?)""", (owner_id, ip, login, password, rent_end, project_name))
        conn.commit()
        conn.close()
        return None
    except Exception as e:
        logger.error("Error: adding VPS-server to list | %s", e)
        raise ValueError

def list_vps(owner_id:int) -> list[str] | None:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""SELECT IP FROM VPS_SERVERS WHERE OWNER_ID = ?""", (owner_id,))
        rows = cur.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        logger.error("Error: retrieving list from VPS-servers | %s", e)
        return None

def get_vps_info(owner_id:int, ip:str) -> list[Any] | None:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""SELECT LOGIN, PASSWORD, RENT_END, PROJECT_NAME, REMINDED FROM VPS_SERVERS WHERE OWNER_ID = ? AND IP = ?""", (owner_id, ip))
        return cur.fetchone()
    except Exception as e:
        logger.error("Error: retrieving VPS-server info | %s", e)
        return None

def delete_vps(owner_id:int, ip:str) -> None:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""DELETE FROM VPS_SERVERS WHERE OWNER_ID = ? AND IP = ?""", (owner_id, ip))
        conn.commit()
        conn.close()
        return None
    except Exception as e:
        logger.error("Error: deleting VPS-server from DB | %s", e)
        return None

def update_rent(new_rent_end:str, owner_id:int, ip:str) -> None:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""UPDATE RENT_END FROM VPS_SERVERS WHERE OWNER_ID = ? AND IP = ?""",(new_rent_end, owner_id, ip))
        conn.commit()
        conn.close()
        return None
    except Exception as e:
        logger.error("Error: update rent | %s", e)
        return None


def update_reminded(reminded:bool, owner_id:int, ip:str) -> None:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""UPDATE VPS_SERVERS SET REMINDED = ? WHERE OWNER_ID = ? AND IP = ?""",(reminded, owner_id, ip))
        conn.commit()
        conn.close()
        return None
    except Exception as e:
        logger.error("Error: update reminded | %s", e)
        return None

def get_all_vps() -> list[Any] | None:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""SELECT OWNER_ID, IP FROM VPS_SERVERS""")
        return cur.fetchall()
    except Exception as e:
        logger.error("Error: retrieving all VPS-servers info | %s", e)
        return None
