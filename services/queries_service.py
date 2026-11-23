from typing import Any
from database import queries

__all__ = [
    "add_vps",
    "list_vps",
    "get_vps_info",
    "delete_vps",
    "update_rent"
]

def add_vps(owner_id:int, ip:str, login:str, password:str, rent_end:str, project_name:str) -> None:
    queries.add_vps(owner_id,ip,login,password,rent_end,project_name)
    return None

def list_vps(owner_id:int) -> list[str] | None:
    result = queries.list_vps(owner_id)
    return result

def get_vps_info(owner_id:int, ip:str) -> dict[str,Any] | None:
    result = queries.get_vps_info(owner_id,ip)
    if result:
        return {
            "login": result[0],
            "password": result[1],
            "rent_end": result[2],
            "project_name": result[3],
            "reminded": result[4]
        }
    return None

def delete_vps(owner_id:int, ip:str) -> None:
    queries.delete_vps(owner_id,ip)
    return None

def update_rent(new_rent_end:str, owner_id:int, ip:str) -> None:
    queries.update_rent(new_rent_end,owner_id,ip)
    return None
