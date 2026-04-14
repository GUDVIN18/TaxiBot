from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.keyboards import choice_class_kb, choice_date_kb, main_keyboard
from utils.states import AddFilter
from utils.models import Filter
import datetime


async def add_filter(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('💎 Выберите тарифы, которые необходимо принимать',
                                     reply_markup=choice_class_kb())
    await state.set_state(AddFilter.choice_classes)


async def choice_class(callback: CallbackQuery, state: FSMContext):
    data = int(callback.data.split()[1])
    if data < 5:
        button = callback.message.reply_markup.inline_keyboard[data][0].text
        button = '🟢' + button[1:] if '🔴' in button else '🔴' + button[1:]
        callback.message.reply_markup.inline_keyboard[data][0].text = button
        buttons = [i for i in callback.message.reply_markup.inline_keyboard]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    elif data == 5:
        classes = [i[0].text for i in callback.message.reply_markup.inline_keyboard]
        classes.pop(-1)
        results = list(map(lambda item: item[2:] if '🟢' in item else None, classes))
        while None in results:
            results.remove(None)
        if not results:
            await callback.answer('⛔ Выберите хотя бы 1 тариф')
            return
        message = "✅ Вы выбрали тарифы:\n{classes}\nТеперь введите от какой суммы принимать заказы:"

        await callback.message.edit_text(message.format(classes="\n".join(classes)))
        await state.update_data(classes=results)
        await state.set_state(AddFilter.set_price)


async def set_price_filter(message: Message, state: FSMContext):
    if message.text.isdigit():
        today, tomorrow = (datetime.date.today().strftime('%d.%m.%Y'),
                           (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%Y'))
        await state.update_data(price=int(message.text))
        await state.set_state(AddFilter.choice_date)
        await message.answer(f'✅ Вы успешно ввели минимальную сумму для заказа <b>{message.text}₽</b>\n'
                             '📆 Выберите дату, для которой будет действовать фильтр',
                             reply_markup=choice_date_kb(str(today), str(tomorrow)))
    else:
        await message.answer('⛔ Введите число, без букв и лишних символов')


async def choice_date_filter(callback: CallbackQuery, state: FSMContext):
    await state.update_data(date=callback.data.split()[1])
    if callback.data.split()[1] != 'always':
        await callback.message.edit_text('🕓 Введите час, с какого необходимо принимать заказы (от 00 до 24) '
                                         'и через пробел час до которого необходимо принимать заказы')
        await state.set_state(AddFilter.save_filter)
    else:
        data = await state.get_data()
        classes = data['classes']
        myfilter = Filter.create(user_id=callback.from_user.id,
                                 price=int(data['price']),
                                 classes=', '.join(classes),
                                 date='0',
                                 time=0,
                                 endtime=24)
        myfilter.save()
        await callback.message.edit_text('✅ Фильтр добавлен\nВы вернулись в главное меню',
                                         reply_markup=main_keyboard())
        await state.clear()


async def save_filter(message: Message, state: FSMContext):
    time = message.text.split()
    if len(message.text) == 5 and len(time) == 2 and time[0].isdigit() and time[1].isdigit()\
            and int(time[0]) < int(time[1]) <= 24:
        data = await state.get_data()
        classes = data['classes']
        myfilter = Filter.create(user_id=message.from_user.id,
                                 price=int(data['price']),
                                 classes=', '.join(classes),
                                 date=data['date'],
                                 time=int(time[0]),
                                 endtime=int(time[1]))
        myfilter.save()
        await message.answer('✅ Фильтр добавлен\nВы вернулись в главное меню',
                             reply_markup=main_keyboard())
        await state.clear()
    else:
        await message.answer('🕓 Введите час, с какого необходимо принимать заказы (от 00 до 24) и через пробел до какого часа принимать.\n'
                             'Например: 04 (4 часа утра) или 17 (5 часов вечера)')
