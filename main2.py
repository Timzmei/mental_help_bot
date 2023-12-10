from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, blue, green
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import simpleSplit
from datetime import datetime
import json
import re


pdfmetrics.registerFont(TTFont('DejaVu', 'dejavu-sans.book.ttf'))  
pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'dejavu-sans.bold.ttf'))  
pdfmetrics.registerFont(TTFont('DejaVu-Italic', 'dejavu-sans.oblique.ttf'))  
pdfmetrics.registerFont(TTFont('helvetica', 'helveticaneuecyr-ultralight3.ttf')) 
pdfmetrics.registerFont(TTFont('helvetica-AG', 'AG_Helvetica.ttf')) 
pdfmetrics.registerFont(TTFont('helvetica-Neue', 'Helvetica_Neue.ttf')) 


def create_pdf_2(test_data, answers_array, result_test, from_user_username, from_user_id, test_name, user_name, doc_name):
    now = datetime.now()
    current_date = now.strftime("%d.%m.%Y")
    
    pdf_filename = "Результаты теста.pdf"
    
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    # Устанавливаем цвет шрифта    
    y_position = 750  # Начальная позиция на странице
    
    # Добавление информации на страницу
    def add_info(text, x_position, ypos, font, font_size, font_color, al=None):
        nonlocal y_position
        c.setFillColor(font_color)
        c.setFont(font, font_size)
        width, height = letter

        lines = simpleSplit(text, font, 12, width-x_position)
        print(lines)
        
        for line in lines:
            if al == "center":
                c.drawCentredString(x_position, ypos, line)
            else:
                c.drawString(x_position, ypos, line)
            ypos -= 20
            # y_position -= 20
            if y_position < 50 and ypos < 50:
                c.showPage()
                c.setFillColor(font_color)
                c.setFont(font, font_size)
                y_position = 750
                if al == "center":
                    c.drawCentredString(100, ypos, line)
                else:
                    c.drawString(100, y_position, line)
            y_position -= 20
    
    
    # Добавляем информацию о тестируемом, лечащем враче и клинике
    add_info(f"{test_name}", 350, y_position, "helvetica-Neue", 17, black, "center")
    y_position -=50
    add_info(f"Имя тестируемого:", 45, y_position, "helvetica-Neue", 10, black)
    y_position += 20
    add_info(f"{user_name}", 180, y_position, "helvetica-AG", 9, black)
    c.rect(170, y_position + 15, 250, 18)  # Координаты и размеры рамки
    
    # Добавление линий для разделения блоков информации
    # c.line(45, y_position - 40, 550, y_position - 40)
    # c.line(45, y_position - 70, 550, y_position - 70)

    add_info(f"Лечащий врач:", 45, y_position, "helvetica-Neue", 10, black)  # Поле для заполнения
    y_position += 20
    add_info(f"{doc_name}", 180, y_position, "helvetica-AG", 9, black)
    c.rect(170, y_position + 15, 250, 18)  # Координаты и размеры рамки
    # Добавляем информацию о тесте и результатах
    add_info(f"Дата прохождения:", 45, y_position, "helvetica-Neue", 10, black)
    y_position += 20
    add_info(f"{current_date}", 180, y_position, "helvetica-AG", 9, black)
    # add_info(f"Название теста:", 45, y_position, "DejaVu-Bold", 10, black)
    
  
    # Добавляем логотип клиники
    c.drawImage('MentalHelp.jpg', 45, 690, width=100, height=100)
    y_position -= 20   
    add_info("Результаты теста:", 290, y_position, "helvetica-Neue", 12, black, "center")
    
    for scale, score in result_test.items():
        add_info(f"{scale}:", 45, y_position, "helvetica-Neue", 10, black)
        y_position += 20
        add_info(f"{score}", 180, y_position, "helvetica-AG", 9, blue)
        
    # Добавление линий для разделения результатов
    # c.line(45, y_position - 5, 550, y_position - 5)
    y_position -= 10        
    # Добавление вопросов и ответов из answersArray    
    print(answers_array)
    for i, answer_dict in enumerate(answers_array, start=1):
        print(f'i={i} : answer_dict={answer_dict}')
        question_number = int(answer_dict['question'].split()[1]) - 1
        
        print(f"answer_dict = {answer_dict}")
        if test_name == 'Опросник гипомании HCL 32':
            sections_number = int(answer_dict['section'])
            section = test_data["sections"][sections_number]
            print(f'sec= {section}')
            question = section["questions"][question_number]
            question_text = question["question"]
            if question["type"] == "text":
                answer_text = answer_dict['answer']
            else:
                answer_index = int(answer_dict['answer'])
                for ans in question["answers"]:
                    print(f"ans = {ans}")
                    # print(f"ans['text'] = {ans.text}")
                    if ans["value"] == answer_index:
                        answer_text = ans["text"]
                        print(f"answer_text = {answer_text}")
                    # answer_text = question["answers"][answer_index]["text"]
            if question_number + 1 == 1:
                add_info(f"{section['section']}", 70, y_position, "helvetica-Neue", 11, black)
            add_info(f"Вопрос {question_number + 1}: {question_text}", 70, y_position, "helvetica-Neue", 10, blue)
            add_info(f"Ответ: {answer_text}", 100, y_position, "helvetica-AG", 10, black)
        else:
            question = test_data["questions"][question_number]
            
            question_text = question["question"]
            answer_index = int(answer_dict['answer'])
            for ans in question["answers"]:
                print(f"ans = {ans}")
                # print(f"ans['text'] = {ans.text}")
                if ans["value"] == answer_index:
                    answer_text = ans["text"]
                    print(f"answer_text = {answer_text}")
                # answer_text = question["answers"][answer_index]["text"]
            add_info(f"Вопрос {i}: {question_text}", 70, y_position, "helvetica-Neue", 10, blue)
            add_info(f"Ответ: {answer_text}", 100, y_position, "helvetica-AG", 10, black)
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

def get_total_scores(answersArray, test_data):
    
    result_test = {}
    total_score = 0
    
    for answer_dict in answersArray:
        question_number = int(answer_dict['answer']) 
        total_score += question_number
    
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

def main():
    data_test_str = '[{"question":"Вопрос 1","answer":"3"},{"question":"Вопрос 2","answer":"1"},{"question":"Вопрос 3","answer":"2"},{"question":"Вопрос 4","answer":"1"},{"question":"Вопрос 5","answer":"1"},{"question":"Вопрос 6","answer":"1"},{"question":"Вопрос 7","answer":"1"},{"question":"Вопрос 8","answer":"1"},{"question":"Вопрос 9","answer":"1"},{"question":"Вопрос 10","answer":"1"},{"question":"Вопрос 11","answer":"1"},{"question":"Вопрос 12","answer":"0"},{"question":"Вопрос 13","answer":"2"},{"question":"Вопрос 14","answer":"1"},{"question":"Вопрос 15","answer":"1"},{"question":"Вопрос 16","answer":"2"},{"question":"Вопрос 17","answer":"2"},{"question":"Вопрос 18","answer":"2"},{"question":"Вопрос 19","answer":"0"},{"question":"Вопрос 20","answer":"2"},{"question":"Вопрос 21","answer":"1"},{"test_name":"test_BDI","name":"Jfj","doc":"Jdjdj"}]'
    data_test = json.loads(data_test_str)
    # Получаем информацию о тесте
    test_info = data_test[-1]
    print(f'data_test: {data_test}')
    print(f'test_info: {test_info}')
    test_name = test_info.get('test_name', 'Название теста не указано')
    user_name = test_info.get('name', 'Имя не указано')
    doc_name = test_info.get('doc', 'Имя врача не указано')
    
    file_data = get_test_data(test_name)
    full_test_name = file_data['testName']

    # Получаем информацию о вопросах и ответах
    answers_array = data_test[:-1]
    
    result_test = {}
    result_string = ''
    
    result_test, result_string = get_total_scores(answers_array, file_data)
    
    pdf_file = create_pdf_2(file_data, answers_array, result_test, 'from_user_username', 'from_user_id', 'Опросник выраженности психопатологической симптоматики', user_name, doc_name)

if __name__ == "__main__":
    main()