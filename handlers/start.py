from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.models import User, Settings
from utils.states import Registration
from utils.keyboards import main_keyboard


async def command_start_handler(message: Message, state: FSMContext):
    await state.clear()
    user = User.get_or_none(User.user_id == message.from_user.id)
    if user:
        await message.answer(f'''<b>👋 Здравствуйте, {message.from_user.full_name}!</b>\n
✅ У Вас есть доступ для использования этого бота
Чтобы настроить автоматическое принятие заказов, нажмите «➕ Добавить фильтр»''',
                             reply_markup=main_keyboard())
    else:
        await message.answer(f'''<b>👋 Здравствуйте, {message.from_user.full_name}!</b>\n
👉 Вы не зарегистрированы в этом боте,
для того, чтобы начать пользоваться ботом – 🔐 отправьте секретный пароль''')
        await state.set_state(Registration.enter_password)


async def enter_password_handler(message: Message, state: FSMContext):
    settings = Settings.get_by_id(1)
    if message.text == settings.bot_password:
        user = User.create(user_id=message.from_user.id)
        user.save()
        await state.clear()
        await message.answer('✅ Вы получили доступ к использованию бота!',
                             reply_markup=main_keyboard())
    else:
        await message.answer('⛔ Неправильный пароль')
