from aiogram.types import CallbackQuery
from utils.models import Filter
from utils.keyboards import filters_kb


async def my_filters(callback: CallbackQuery):
    filters = [i.id for i in Filter.select().where(Filter.user_id == callback.from_user.id)]
    if filters:
        await callback.message.edit_text('🔍 Ниже перечислены Ваши фильтры по порядковым номерам',
                                         reply_markup=filters_kb(filters))
    else:
        await callback.answer('⛔ У Вас нет сохраненных фильтров')
