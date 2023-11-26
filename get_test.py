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
import re

from main import bot, BOT_TOKEN

user_scores = {}
current_question = 1

router = Router()
web_app = WebAppInfo(url='https://timzmei.github.io/mental_help_bot')

pdfmetrics.registerFont(TTFont('DejaVu', 'dejavu-sans.book.ttf'))  
pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'dejavu-sans.bold.ttf'))  
pdfmetrics.registerFont(TTFont('DejaVu-Italic', 'dejavu-sans.oblique.ttf'))  

# Создаем PDF-файл
def create_pdf(test_data, answers_array, result_test, from_user_username, from_user_id, test_name, user_name, phone):    
    now = datetime.now()
    current_date = now.strftime("%d.%m.%Y")
    
    pdf_filename = "Результаты теста.pdf"
    
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    # Устанавливаем цвет шрифта    
    y_position = 750  # Начальная позиция на странице
    
    # Добавление информации на страницу
    def add_info(text, x_position, ypos, font, font_size, font_color):
        nonlocal y_position
        c.setFillColor(font_color)
        c.setFont(font, font_size)
        if y_position >= 50:  
            c.drawString(x_position, ypos, text)
        if y_position < 50:  # Если информация не помещается, создаем новую страницу
            c.showPage()
            c.setFillColor(font_color)
            c.setFont(font, font_size)
            y_position = 750  # Сбрасываем позицию на новой странице
            c.drawString(x_position, y_position, text)
        y_position -= 20
    
    
    # Добавляем информацию о тестируемом, лечащем враче и клинике
    
    add_info(f"Имя тестируемого:", 45, y_position, "DejaVu-Bold", 10, black)
    y_position += 20
    add_info(f"{from_user_username}, {phone}", 180, y_position, "DejaVu", 9, black)
    c.rect(170, y_position + 15, 250, 18)  # Координаты и размеры рамки
    
    # Добавление линий для разделения блоков информации
    # c.line(45, y_position - 40, 550, y_position - 40)
    # c.line(45, y_position - 70, 550, y_position - 70)

    add_info(f"Лечащий врач:", 45, y_position, "DejaVu-Bold", 10, black)  # Поле для заполнения
    c.rect(170, y_position + 15, 250, 18)  # Координаты и размеры рамки
    # Добавляем информацию о тесте и результатах
    add_info(f"Дата прохождения:", 45, y_position, "DejaVu-Bold", 10, black)
    y_position += 20
    add_info(f"{current_date}", 180, y_position, "DejaVu", 9, black)
    add_info(f"Название теста:", 45, y_position, "DejaVu-Bold", 10, black)
    y_position += 20
    add_info(f"{test_name}", 180, y_position, "DejaVu", 9, black)
  
    # Добавляем логотип клиники
    c.drawImage('MentalHelp.jpg', 450, 710, width=80, height=80)
       
    add_info("Результаты теста:", 45, y_position, "DejaVu-Bold", 10, black)
    
    for scale, score in result_test.items():
        add_info(f"{scale}:", 45, y_position, "DejaVu-Bold", 10, black)
        y_position += 20
        add_info(f"{score}", 180, y_position, "DejaVu", 9, black)
        
    # Добавление линий для разделения результатов
    # c.line(45, y_position - 5, 550, y_position - 5)
            
    # Добавление вопросов и ответов из answersArray    
    print(answers_array)
    for i, answer_dict in enumerate(answers_array, start=1):
        question_number = int(answer_dict['question'].split()[1]) - 1
        question = test_data["questions"][question_number]
        question_text = question["question"]
        answer_index = int(answer_dict['answer'])
        answer_text = question["answers"][answer_index]["text"]
        add_info(f"Вопрос {i}: {question_text}", 70, y_position, "DejaVu-Bold", 8, blue)
        add_info(f"Ответ: {answer_text}", 100, y_position, "DejaVu-Italic", 8, black)
        # Добавление линий между каждым вопросом и ответом для лучшей разбивки
        # c.line(45, y_position - 5, 550, y_position - 5)
    
    # # Добавление общего балла (GSI), индекс PSI и индекс PDSI
    # add_info(f"Общий балл (GSI): {total_score}", y_position)
    # add_info(f"Индекс PSI: {psi_count}", y_position)
    # add_info(f"Индекс PDSI: {pdsi}", y_position)
    
    c.save()
    print(f"PDF-файл с результатами теста создан: {pdf_filename}")

def get_test_data(test_name):
    # Путь к вашему JSON файлу с тестовыми данными
    json_file_path = f'{test_name}.json'

    # Загрузка данных из файла
    with open(json_file_path, 'r', encoding='utf-8') as file:
        test_data = json.load(file)
    return test_data

def get_result_test_scl(answersArray, test_data):
    
    # Суммирование баллов по каждой шкале
    scales = test_data["keys"][0]  # Получаем ключи для шкал
    # print(f'scales = {scales}')
    scale_scores = {}  # Словарь для хранения баллов по каждой шкале
    # print(f'scales.items() = {scales.items()}')
    for scale, items in scales.items():
            scale_scores[scale] = round(sum(1 for item in answersArray if int(item["answer"]) in items) / len(items), 2)

    

    # Вычисление общего балла (индекс GSI)
    gsi_index = round(sum(scale_scores.values()) / len(answersArray), 2)

    # Подсчет количества пунктов от 1 до 4 (индекс PSI)
    psi_count = sum(1 for item in answersArray if 1 <= int(item["answer"]) <= 4)

    # Расчет индекса выраженности дистресса PDSI
    pdsi_index = round((gsi_index * len(answersArray)) / psi_count if psi_count != 0 else 0, 2)
    
    scale_scores['gsi_index'] = gsi_index
    scale_scores['psi_count'] = psi_count
    scale_scores['pdsi_index'] = pdsi_index
    
    # Форматирование результатов в строку в формате Markdown
    result_string = ''
    
    for key, value in scale_scores.items():
        if isinstance(value, float):
            result_string += f"*{key.capitalize()}:* {value:.2f}\n"
        else:
            result_string += f"*{key.capitalize()}:* {value}\n"

    return scale_scores, re.escape(result_string)

def get_total_scores(answersArray, test_data):
    
    result_test = {}
    total_score = 0
    
    for answer_dict in answersArray:
        question_number = int(answer_dict['question'].split()[1]) - 1  # Получаем номер вопроса из словаря
        question = test_data["questions"][question_number]
        selected_answer = next((ans for ans in question["answers"] if ans["value"] == int(answer_dict['answer'])), None)
        if selected_answer:
            total_score += selected_answer["value"]
    
    result_ranges = test_data['resultRanges']
    result_text = ''

    for result_range in result_ranges:
        if result_range["minScore"] <= total_score <= result_range["maxScore"]:
            result_text = result_range["resultText"]

    # Округление значения общего балла до сотых
    total_score = round(total_score, 2)

    result_test['total_score'] = total_score
    result_test['result_text'] = result_text
    
    result_test['Баллы'] = result_test.pop('total_score')
    result_test['Описание'] = result_test.pop('result_text')
    
     # Форматирование результатов в строку в формате Markdown
    result_string = f"*Баллы:* {total_score}\n*Описание:* {re.escape(result_text)}"


    return result_test, result_string


@router.message(F.web_app_data)
async def get_answer(web_app_message):
    from_user_username = web_app_message.from_user.full_name
    from_user_id = web_app_message.from_user.id
    data_test_str = web_app_message.web_app_data.data
    print(f'data_test_str: {data_test_str}')
    data_test = json.loads(data_test_str)
    # Получаем информацию о тесте
    test_info = data_test[-1]
    print(f'data_test: {data_test}')
    print(f'test_info: {test_info}')
    test_name = test_info.get('test_name', 'Название теста не указано')
    user_name = test_info.get('name', 'Имя не указано')
    phone = test_info.get('phone', 'Номер телефона не указан')
    
    print(f'data_test: {data_test}')
    print(f'test_info: {test_info}')
    # test_result = test_info.get('result', 'Результат не указан')
    # text_result = test_info.get('text_result', 'Текстовый результат не указан')
    
    file_data = get_test_data(test_name)
    
    full_test_name = file_data['testName']

    # Получаем информацию о вопросах и ответах
    answers_array = data_test[:-1]
    
    result_test = {}
    result_string = ''
    
    if (test_name == 'SCL_90_R'):
        result_test, result_string = get_result_test_scl(answers_array, file_data)
    else:
        result_test, result_string = get_total_scores(answers_array, file_data)
    
    
    pdf_file = create_pdf(file_data, answers_array, result_test, from_user_username, from_user_id, full_test_name, user_name, phone)

    # Выводим информацию о тесте
    print(f"Название теста: {full_test_name}")
    print(f"Результат теста: {result_string}")

    
    await web_app_message.answer(f'Тест завершен\.\nТестировался: {from_user_username}\nНазвание теста: {full_test_name}\nРезультат: \n{result_string}\n', reply_markup=ReplyKeyboardRemove(), parse_mode="MarkdownV2")
    await bot.send_document(244063420, FSInputFile('Результаты теста.pdf'), caption=f'Тест завершен\.\nТестировался: {from_user_username}\nНазвание теста: {full_test_name}\nРезультат: \n{result_string}', parse_mode="MarkdownV2")
    await bot.send_document(1563111150, FSInputFile('Результаты теста.pdf'), caption=f'Тест завершен\.\nТестировался: {from_user_username}\nНазвание теста: {full_test_name}\nРезультат: \n{result_string}', parse_mode="MarkdownV2")

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
        [
            types.KeyboardButton(text="Опросник выраженности психопатологической симптоматики"
                                 , web_app=WebAppInfo(url=f"https://timzmei.github.io/mental_help_bot?paramName=SCL_90_R"))
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
