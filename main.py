import asyncio
from multiprocessing import Process
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand, ErrorEvent, Message
from aiogram.exceptions import TelegramNetworkError, TelegramConflictError
from aiogram.filters import ExceptionTypeFilter

from config import BOT_TOKEN
from utils.states import Registration, AddFilter
from userBot.userbot import userbot_main
from handlers.start import command_start_handler, enter_password_handler
from handlers.add_filter import add_filter, choice_class, set_price_filter, choice_date_filter, save_filter
from handlers.my_filters import my_filters
from handlers.show_filter import show_filter
from handlers.delete_filter import delete_filter
from handlers.cancel_order import cancel_order, cancel_order_handle, cancel_order_state
import logging

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.message.register(command_start_handler, Command(commands='start'))
dp.message.register(cancel_order, Command(commands='cancel')) # команда отмены заказа
dp.message.register(enter_password_handler, Registration.enter_password) # ввод пароля для доступа к боту
dp.callback_query.register(add_filter, F.data == 'add_filter') # Основное меню после ввода пароля
dp.callback_query.register(choice_class, F.data.split()[0] == 'class', AddFilter.choice_classes) # выбор класса, для добавление фильтра
dp.message.register(set_price_filter, AddFilter.set_price) # установка суммы, от которой принимать заказы
dp.callback_query.register(choice_date_filter, F.data.split()[0] == 'date', AddFilter.choice_date) # выбор даты, когда будет действовать
dp.message.register(save_filter, AddFilter.save_filter) # сохранение надстроек фильтра в БД
dp.callback_query.register(my_filters, F.data == 'my_filters') # отображение фильтров пользователя
dp.callback_query.register(show_filter, F.data.split()[0] == 'show_filter') # отображение выбранного фильтра
dp.callback_query.register(delete_filter, F.data.split()[0] == 'delete_filter') # удалить выбранный фильтр
dp.message.register(cancel_order_handle, cancel_order_state) # отменяем введённый заказ


@dp.error(ExceptionTypeFilter(TelegramNetworkError, TelegramConflictError))
async def exception_handling(event: ErrorEvent):
    logging.error('=============== [ NETWORK ERROR ] =============')
    import subprocess
    subprocess.call(["sudo", "systemctl", "restart", "bot"])


@dp.message(Command("restart"))
async def restart(message: Message):
    if message.from_user.id == 566466985:
        import subprocess
        subprocess.call(["sudo", "systemctl", "restart", "bot"])
        await message.answer("Ушел на перезагрузку")


#async def set_default_commands():
#    await bot.set_my_commands([
#        BotCommand(command="start", description="🤖 Запустить бота"),
#        BotCommand(command="cancel", description="⛔ Отменить заказ")
#    ])


from aiogram.exceptions import TelegramNetworkError

async def set_default_commands():
    try:
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="🤖 Запустить бота"),
                BotCommand(command="cancel", description="⛔ Отменить заказ"),
            ],
            request_timeout=30
        )
    except TelegramNetworkError:
        print("Telegram timeout при установке команд")



async def main():
    await set_default_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(filename='mainBot.log', level=logging.INFO)
    p = Process(target=userbot_main)
    p.start()
    print('started')
    asyncio.run(main())
