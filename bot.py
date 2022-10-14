from aiogram import Bot,Dispatcher,types,executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from datetime import datetime
from analyzer import Analyzer
from server import KscServer
from database import Database
from writer import Writer
from keyboard import Keyboards
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.utils.exceptions import MessageTextIsEmpty, MessageIsTooLong

TOKEN = ''
SUPER_USER_ID = ''

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot,storage=MemoryStorage())
scheduler = AsyncIOScheduler()
db = Database()
kb = Keyboards()
server = KscServer(ip='', username='', password='', server_port=13299).get_server()

@dp.message_handler(commands = ['start'],state=None)
async def start(message: types.Message):
    await message.answer('Запрос на добавление в список доверенных пользователей отправлен администратору.')
    await bot.send_message(SUPER_USER_ID,f'Добавить пользователя в доверенные пользователи?\nid = {message.from_user.id}\nname = {message.from_user.username}',reply_markup=kb.inline_add_user_buttons(message.from_user.id,message.from_user.username))


@dp.message_handler(content_types=['text'],state=None)
async def not_response(message: types.Message, state:FSMContext):
    pass


@dp.callback_query_handler(text_contains="useradd_")
async def add_question(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    answer, id, name = bool(int(call.data.split('_')[1])),int(call.data.split('_')[2]), str(call.data.split('_')[3])
    if answer:
        await bot.send_message(id,'Доступ разрешен')
        await bot.send_message(SUPER_USER_ID,f'Пользователь\nid={id}\nname={name}\nДобавлен в список разрешенных пользователей')
        db.create_user(id, name)
    else:
        await bot.send_message(id,'Вам отказано в доступе к боту')


async def main():
    analyzer_message, suspect_host_list = Analyzer(server).compare_dicts()
    Writer(suspect_host_list)
    # print(analyzer_message)
    for id in db.get_user_list():
        try:
            await bot.send_message(id, analyzer_message)
        except MessageTextIsEmpty:
            break
        except MessageIsTooLong:
            await send_long_message(id, analyzer_message)
            
async def send_long_message(id, analyzer_message):
    if len(analyzer_message) > 4096:
        for x in range(0, len(analyzer_message), 4096):
            await bot.send_message(id, analyzer_message[x:x+4096])
        else:
            await bot.send_message(id, analyzer_message)


if __name__=='__main__':
    scheduler.add_job(main,"interval",seconds=60)
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)