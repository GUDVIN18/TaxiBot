from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from utils.states import cancel_order_state
from utils.models import Orders


async def cancel_order(message: Message, state: FSMContext):
    await state.set_state(cancel_order_state)
    await message.answer('📌 Для того, чтобы отменить заказ, введите его уникальный номер (только цифры)\n',
                         reply_markup=ReplyKeyboardRemove())


async def cancel_order_handle(message: Message, state: FSMContext):
    if message.text.isdigit() and 6 >= len(message.text) >= 4:
        order = Orders.get_or_none(Orders.order_id == int(message.text))
        if order:
            order.delete_instance()
            await message.answer(f'✅ Вы успешно отменили заказ №{message.text}')
        else:
            await message.answer('⛔ Бот не принимал заказ с указанным номером')
    else:
        await message.answer('⛔ Введите номер принятого ботом заказа (только цифры)')
