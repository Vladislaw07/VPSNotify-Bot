# pyright: reportUnusedImport=false
from .router import router
from . import add, delete_vps, list_vps, show_vps

__all__ = ["router"]
