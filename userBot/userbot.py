from config import API_ID, API_HASH, CHANNEL_CHAT_ID
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from utils.models import Filter, Orders, User
import re
import asyncio
import logging

app = Client("userbot", api_id=API_ID, api_hash=API_HASH)


async def handle_message_click(client, message):
    await message.click(0)
    url = message.reply_markup.inline_keyboard[0][0].url
    match = re.match(r'https?://t\.me/([^/?]+)\?start=(\w+)', url)
    if match:
        bot_username = match.group(1)
        start_param = url[url.find('?start=') + 7:]  # match.group(2)
        chat = await client.get_chat(bot_username)
        await app.send_message(chat.id, f"/start {start_param}")
    else:
        print("Формат ссылки не соответствует ожидаемому шаблону")


@app.on_message(filters.chat(CHANNEL_CHAT_ID))
async def handle_message(client, message: Message):
    try:
        if message.reply_markup.inline_keyboard[0][0].text != ' Принять':
            return
    except:
        print("NONETYPE ERROR")
    print('\n\n\nmessage.text\n\n\n', message.text)
    params = message.text.split('\n')
    my_filters = Filter.select()
    for i in my_filters:
        order_id = int(''.join(params[-1].replace('Поездка №', '').split()))
        orders = [i.order_id for i in Orders.select()]
        hour, minute = tuple(map(int, params[2][:5].split(':')))
        price = int(''.join([i for i in params[3] if i.isdigit()]))
        if ((i.date == '0' or (params[0].strip(" 🔥") == i.date and
                               i.time <= hour < i.endtime)) and (price >= i.price) and
                params[4].capitalize().split()[0] in i.classes.split(', ') and
                (order_id not in orders) and 'Без возможности отказа' not in message.text):
            try:
                await handle_message_click(client, message)
            except Exception as e:
                print(e)
                print('Message doesn\'t have a clickable keyboard')
            from main import bot
            for user in User.select():
                try:
                    await bot.send_message(user.user_id, f'🤖 Бот подал заявку на заказ №{order_id}')
                except Exception as e:
                    print(e)
            order = Orders.create(order_id=order_id)
            order.save()
            try:
                # await bot.forward_message(-1002111623353, message.chat.id, message.id)
                await bot.send_message(-1002111623353, f'🤖 Бот подал заявку на заказ №{order_id}')
            except Exception as e:
                print(e)


@app.on_message(filters.chat(5015599436))
async def handle_answer(client, message: Message):
    from main import bot
    try:
        if ' уже занята. Попробуйте выбрать другую' in message.text:
            match = re.match('Поездка №([0-9]+) уже занята. Попробуйте выбрать другую', message.text)
            order = Orders.get_or_none(Orders.order_id == int(match.group(1)))
            order.delete_instance()
            await bot.send_message(-1002111623353, f'❌ Поездку №{match.group(1)} не получилось взять')
        else:
            pass
            # await bot.forward_message(-1002111623353, message.chat.id, message.id)
    except Exception as e:
        print(e)


def userbot_main():
    logging.basicConfig(filename='userBot.log', level=logging.INFO)
    print('starting userbot')
    app.run()
    print('started userbot')
