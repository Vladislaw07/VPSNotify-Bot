from aiogram.fsm.state import State, StatesGroup

class delete_vps (StatesGroup):
    confirmation_to_delete: State = State()
    deleting_vps : State = State()
