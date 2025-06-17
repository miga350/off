from aiogram.fsm.state import State, StatesGroup

class CheckPDFStates(StatesGroup):
    waiting_file = State()
    waiting_payment = State()
