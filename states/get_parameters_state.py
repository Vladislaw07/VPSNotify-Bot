from aiogram.fsm.state import State, StatesGroup

class get_parameters (StatesGroup):
    get_ip : State = State()
    get_login : State = State()
    get_password : State = State()
    get_rent_end : State = State()
    get_project_name : State = State()
