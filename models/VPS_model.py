from dataclasses import dataclass

@dataclass()
class VPS:
    _owner_id:int
    _ip:str
    _login:str
    _password:str
    _rent_end:str
    _project_name:str
    reminded:bool

    @property
    def owner_id(self) -> int:
        return self._owner_id
    @property
    def ip(self) -> str:
        return self._ip
    @property
    def login(self) -> str:
        return self._login
    @property
    def password(self) -> str:
        return self._password
    @property
    def rent_end(self) -> str:
        return self._rent_end
    @property
    def project_name(self) -> str:
        return self._project_name

async def vps_class_builder(owner_id:int, ip:str, login:str, password:str, rent_end:str, project_name:str, reminded:bool ) -> VPS:
    vps : VPS = VPS(_owner_id=owner_id, _ip=ip, _login=login, _password=password, _rent_end=rent_end, _project_name=project_name, reminded=reminded)
    return vps
