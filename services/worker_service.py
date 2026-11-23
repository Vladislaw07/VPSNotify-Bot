from typing import Any
from database import queries

__all__ = [
    "update_reminded",
    "get_all_vps"
]

def update_reminded(reminded:bool, owner_id:int, ip:str) -> None:
    queries.update_reminded(reminded,owner_id,ip)
    return None

def get_all_vps() -> list[Any] | None:
    result = queries.get_all_vps()
    return result
