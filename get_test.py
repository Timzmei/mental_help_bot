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
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, blue, green
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
from flask import send_file
from aiogram.utils import keyboard
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import json

from main import bot, BOT_TOKEN

user_scores = {}
current_question = 1

router = Router()
web_app = WebAppInfo(url='https://timzmei.github.io/mental_help_bot')

pdfmetrics.registerFont(TTFont('DejaVu', 'dejavu-sans.book.ttf'))  
pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'dejavu-sans.bold.ttf'))  
pdfmetrics.registerFont(TTFont('DejaVu-Italic', 'dejavu-sans.oblique.ttf'))  

# Создаем PDF-файл
def create_pdf(test_name, test_result, text_result, questions_answers, from_user_username, from_user_id, doctor_name='', clinic_logo='', clinic_name='MentalHelp'):
    now = datetime.now()
    current_date = now.strftime("%d.%m.%Y")

    pdf_filename = f"Результаты теста.pdf"  # Имя PDF-файла

    c = canvas.Canvas(pdf_filename, pagesize=A4)


    # Устанавливаем цвет шрифта
    c.setFillColor(black)
    # Устанавливаем стиль (жирность и курсив) для шрифта
    c.setFont("DejaVu-Bold", 10)
    
    # Добавляем информацию о тестируемом, лечащем враче и клинике
    c.rect(170, 815, 250, 18)  # Координаты и размеры рамки
    c.drawString(45, 820, f"Имя тестируемого:")
    c.rect(170, 795, 250, 18)  # Координаты и размеры рамки
    c.drawString(45, 800, f"Лечащий врач:")  # Поле для заполнения
    # Добавляем информацию о тесте и результатах
    c.drawString(45, 760, f"Дата прохождения:")
    c.drawString(45, 730, f"Название теста:")
    c.drawString(45, 715, f"Результат:")
    c.drawString(45, 700, f"Описание результата:")
    
    c.setFont("DejaVu", 9)
    c.drawString(180, 820, f"{from_user_username}")
    c.drawString(180, 760, f"{current_date}")
    c.drawString(180, 730, f"{test_name}")
    c.drawString(180, 715, f"{test_result}")
    c.drawString(180, 700, f"{text_result}")
    # Добавляем логотип клиники
    c.drawImage('MentalHelp.jpg', 450, 735, width=100, height=100)

    # Добавляем информацию о вопросах и ответах
    y = 670
    for qa in questions_answers:
        question = qa['question']
        answer = qa['answer']
        
        # Устанавливаем цвет шрифта
        c.setFillColor(blue)
        # Устанавливаем кириллический шрифт и размер
        c.setFont("DejaVu-Bold", 8)
        
        c.drawString(70, y, f"Вопрос: {question}")
        
        # Устанавливаем цвет шрифта
        c.setFillColor(black)        
        # Устанавливаем стиль (жирность и курсив) для шрифта
        c.setFont("DejaVu-Italic", 8)
        
        c.drawString(100, y - 15, f"Ответ: {answer}")
        y -= 30  # Переход на следующую строку

    c.save()

    return pdf_filename


@router.message(F.web_app_data)
async def get_answer(web_app_message):
    from_user_username = web_app_message.from_user.full_name
    from_user_id = web_app_message.from_user.id
    data_test_str = web_app_message.web_app_data.data
    print(data_test_str)
    data_test = json.loads(data_test_str)
    # data_test = data_test_str

    
    # Получаем информацию о тесте
    test_info = data_test[-1]

    test_name = test_info.get('test_name', 'Название теста не указано')
    test_result = test_info.get('result', 'Результат не указан')
    text_result = test_info.get('text_result', 'Текстовый результат не указан')
    

    # Получаем информацию о вопросах и ответах
    questions_answers = data_test[:-1]
    pdf_file = create_pdf(test_name, test_result, text_result, questions_answers, from_user_username, from_user_id)

    # Выводим информацию о тесте
    print(f"Название теста: {test_name}")
    print(f"Результат: {test_result}")
    print(f"Текстовый результат: {text_result}")

    # Выводим информацию о вопросах и ответах
    for qa in questions_answers:
        print(f"\nВопрос: {qa['question']}")
        print(f"Ответ: {qa['answer']}")
    
    
    await web_app_message.answer(f'Тест завершен.\nТестировался: {from_user_username}\nНазвание теста: {test_name}\nРезультат: {test_result}\n{text_result}', reply_markup=ReplyKeyboardRemove())
    # await bot.send_message(1563111150, f'Тест завершен.\nТестировался: {from_user_username}, id: {user_id} \n{test_info}')
    await bot.send_document(244063420, FSInputFile('Результаты теста.pdf'), caption=f'Тест завершен.\nТестировался: {from_user_username}\nНазвание теста: {test_name}\nРезультат: {test_result}\n{text_result}')
    await bot.send_document(1563111150, FSInputFile('Результаты теста.pdf'), caption=f'Тест завершен.\nТестировался: {from_user_username}\nНазвание теста: {test_name}\nРезультат: {test_result}\n{text_result}')

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
