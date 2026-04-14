from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, KeyboardButton, InlineKeyboardButton


def main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='⚙️ Мои фильтры', callback_data='my_filters'))
    builder.add(InlineKeyboardButton(text='➕ Добавить фильтр', callback_data='add_filter'))
    return builder.adjust(1).as_markup(resize_keyboard=True, one_time_keyboard=True)


def choice_class_kb():
    buttons = ['🔴 Стандарт', '🔴 Комфорт', '🔴 Бизнес', '🔴 Представительский', '🔴 Минивэн', '➡️ Продолжить']
    builder = InlineKeyboardBuilder()
    for i, item in enumerate(buttons):
        builder.add(InlineKeyboardButton(text=item, callback_data=f"class {i}"))
    return builder.adjust(1).as_markup()


def choice_date_kb(today, tomorrow):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='📅 Сегодня', callback_data=f'date {today}'))
    builder.add(InlineKeyboardButton(text='🗓️ Завтра', callback_data=f'date {tomorrow}'))
    builder.add(InlineKeyboardButton(text='♾️ Всегда', callback_data='date always'))
    return builder.adjust(2).as_markup()


def filters_kb(filters):
    builder = InlineKeyboardBuilder()
    for i in filters:
        builder.add(InlineKeyboardButton(text=f'Фильтр №{i}', callback_data=f'show_filter {i}'))
    builder.add(InlineKeyboardButton(text='↩️ Назад', callback_data=f'show_filter back'))
    return builder.adjust(2).as_markup()


def show_filter_kb(filter_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🗑️ Удалить фильтр', callback_data=f'delete_filter {filter_id}'))
    builder.add(InlineKeyboardButton(text='↩️ Назад', callback_data='my_filters'))
    return builder.adjust(1).as_markup()
