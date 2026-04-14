from aiogram.types import CallbackQuery, Message
from utils.models import Filter
from utils.keyboards import filters_kb


async def delete_filter(callback: CallbackQuery):
    filter_id = int(callback.data.split()[1])
    Filter.delete_by_id(filter_id)
    filters = [i.id for i in Filter.select().where(Filter.user_id == callback.from_user.id)]
    await callback.message.edit_text(f'✅ Вы успешно удалили Фильтр №{filter_id}\n'
                                     f'🔍 Ниже перечислены Ваши фильтры по порядковым номерам',
                                     reply_markup=filters_kb(filters))
