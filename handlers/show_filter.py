from aiogram.types import CallbackQuery
from utils.models import Filter
from utils.keyboards import show_filter_kb, main_keyboard


async def show_filter(callback: CallbackQuery):
    filter_id = callback.data.split()[1]
    if filter_id == 'back':
        await callback.message.edit_text(f'''<b>👋 Здравствуйте, {callback.from_user.full_name}!</b>\n
✅ У Вас есть доступ для использования этого бота
Чтобы настроить автоматическое принятие заказов, нажмите «➕ Добавить фильтр»''', reply_markup=main_keyboard())
        return
    my_filter = Filter.get_by_id(int(filter_id))
    text = f'''⚙️ Фильтр №{filter_id}
💎 Тарифы: {my_filter.classes}
💵 Минимальная цена: {my_filter.price}
📅 Дата: {'Всегда' if my_filter.date == '0' else my_filter.date}
🕗 Время: {my_filter.time}:00-{my_filter.endtime}:00'''
    await callback.message.edit_text(text, reply_markup=show_filter_kb(filter_id))
