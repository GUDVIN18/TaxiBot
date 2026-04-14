from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    enter_password = State()


class AddFilter(StatesGroup):
    choice_classes = State()
    set_price = State()
    choice_date = State()
    save_filter = State()


cancel_order_state = State()
