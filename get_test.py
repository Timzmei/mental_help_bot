from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram import types, Bot, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Dispatcher
from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonDefault,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)
from datetime import datetime

from aiogram.utils import keyboard
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from main import session, bot, BOT_TOKEN

user_scores = {}
current_question = 1

router = Router()
web_app = WebAppInfo(url='https://timzmei.github.io/pto_bot')


@router.message(F.web_app_data)
async def buy_process(web_app_message):
    from_user_username = web_app_message.from_user.username
    from_user_id = web_app_message.from_user.id
    test_info = web_app_message.web_app_data.data
    print(from_user_username, web_app_message.web_app_data.data)
    # await web_app_message.answer(f'{web_app_message.data.data}')
    await web_app_message.answer(f'Тест завершен.\nТестировался: @{from_user_username}\n{test_info}', reply_markup=ReplyKeyboardRemove())
    await bot.send_message(244063420, f'Тест завершен.\nТестировался: @{from_user_username}\n{test_info}', reply_markup=ReplyKeyboardRemove())
    
@router.message(Command("test"))
async def command_webview(message: Message):
    param_name = "test_BDI"
    kb = [
        [
            types.KeyboardButton(text="Шкала депрессии Бека"
                                 , web_app=WebAppInfo(url=f"https://timzmei.github.io/mental_help_bot?paramName=test_BDI"))
        ],
        [
            types.KeyboardButton(text="Шкала тревоги Бека"
                                 , web_app=WebAppInfo(url=f"https://timzmei.github.io/mental_help_bot?paramName=test_BAI"))
        ],
        [
            types.KeyboardButton(text="Шкала безнадежности Бека"
                                 , web_app=WebAppInfo(url=f"https://timzmei.github.io/mental_help_bot?paramName=test_BHI"))
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Шкала депрессии Бека"
    )

    await message.answer(
        "Отлично\!\n Тесты разработаны психотерапевтом и создателем когнитивной психотерапии Аароном Беком\.\nБек работал в основном в области изучения и лечения депрессивных расстройств\.\n*Шкала депрессии Бека\.*\n_Тест предлагает оценить ваше состояние за прошедшую неделю по нескольким параметрам — отношение к будущему и к неудачам в прошлом\, испытываете ли вы чувство вины и грусти\, самокритика\.\n_*Шкала тревоги Бека\.*\n_Тест предлагает оценить ваше состояние за прошедшую неделю по нескольким симптомам тревоги — ощущение жара\, дрожь в ногах\, неспособность расслабиться\, страх\, затруднённое дыхание\._\n*Шкала Безнадежности Бека\.*\n_Тест предлагает оценить выраженность негативного отношения субъекта к собственному будущему\. Особую ценность данная методика представляет в качестве косвенного индикатора суицидального риска у пациентов\, страдающих депрессией\, а также у людей\, ранее уже совершавших попытки самоубийства\._",
        parse_mode="MarkdownV2", reply_markup=keyboard
    )
