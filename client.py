from webbrowser import get
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile

from aiogram import types, F, Router, Bot
from aiogram.types import Message, Chat, MenuButtonCommands
from aiogram.filters import Command
from aiogram import Dispatcher
from datetime import datetime
from unidecode import unidecode
from collections import deque
import locale
import os



import requests
import datetime


from dotenv import load_dotenv
from chat_bot import Chat_bot
# from chat import Chat  # Подключение Chat класса из файла chat.py

# Загрузить переменные окружения из .env файла
load_dotenv()
chatbot_instance = Chat_bot()

router = Router()
# Создание экземпляра Chat
# chat_instance = Chat()
my_queue = deque(maxlen=10)

commands = {'/start': 'Нажмите для запуска бота', '/тест': 'Тестирование'}

@router.message(Command("start"))
async def start_command(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    # print(id_user)
    await message.reply(f'Привет, [{user_name}](tg://user?id={user_id})\!', parse_mode="MarkdownV2")
    await message.answer('Я - телеграм бот, созданный для помощи клиентам клиники MentalHelp')

    # await message.reply('Привет!')
    
@router.message(F.text)
async def echo_happy_birthday(message: Message):
    message_id = message.message_id
    from_user_name = transliterate_text(message.from_user.first_name)
    from_user = message.from_user
    message_text = message.text
    my_queue.append({'role': 'user', 'name': from_user_name, 'content': message_text})
    
    # # Создаем экземпляр класса UsersDB, который подключится к базе данных или создаст ее, если она не существует
    # users_db = UsersDB()

    # all_users = users_db.get_all_users()
    # print("Все пользователи:", all_users)

    # # Закрываем соединение с базой данных
    # users_db.close_connection()
    

    
    normal_info = '''You are a useful chat assistant named "TherapyBot" who helps clients of the MentalHelp psychotherapy clinic. 
        You help patients with questions about their well-being and worries. Always extremely tactful and courteous. Answer only in Russian.'''
        

    
    messages = get_messages(list(my_queue), normal_info)
           
    text = await chatbot_instance.create_chat_completion(messages)
    text = text.replace('Chatbase', '***')
    text = text.replace('I am not sure. Email support@chatbase.co for more info.', 'Давай не будем, я тебя умоляю')

    await message.reply(text)

def get_messages(my_queue, info):

    
    system_info = info
    messages = []
    messages.append({'role': 'system', 'content': system_info})
    print(f'add system info = {messages}')
    for message in my_queue:
      messages.append(message)
    print(f'add messages = {messages}')
    return messages

def transliterate_text(text):
    transliterated_text = ""
    
    for char in text:
        if char.isalpha() and char.isascii():
            # Символ является буквой латинского алфавита или другим символом ASCII
            transliterated_text += char
        else:
            # Символ не является буквой латинского алфавита
            transliterated_text += unidecode(char)
    
    return transliterated_text
