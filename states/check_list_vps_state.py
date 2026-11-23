from aiogram.fsm.state import State, StatesGroup

class check_list (StatesGroup):
    show_list : State = State()
