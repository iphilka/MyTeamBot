import pprint
import time
from google_sheet_client import client
from teamleaders import DEFAULT_TEAMLEADER, get_team_leaders

# Открываем табличку
spreadsheet_id = '1XG638nHVFz6kXAalMGjrawifVb7e-XpXFNyaX16-G3w'
sheet = client.open_by_key(spreadsheet_id).worksheet('Форма от 06.2021')

def formatMessage(records):
    text = str(records['Тимлид преподавателя']) + '\n\n' +\
           'Сообщение для преподавателя: ' + str(records['ФИО преподавателя']) + '\n' +\
           str(records['Рекомендации']) + '\n' + 'Средняя оценка: ' + str(records['Средняя оценка']) + '\n' + \
           'Сообщение для ТЛ:' + '\n' + \
           str(records['Сообщение для ТЛ (в случае грубых нарушений со стороны П: мат, грубые слова, кушает на уроке, обсуждает с учениками неподходящие темы)'])
    print(records['Средняя оценка'])
    return text

def getMessages():
    # Забираем все записи их таблицы
    work = sheet.get_all_records()
    # print(work)

    endIndex = 0
    for i in range(len(work)):
        endIndex += 1
        # Добавим поле 'Номер заявки'
        if work[i]['Средняя оценка'] == '':
            middleFunc = f'=ОКРУГЛ(ЕСЛИ(F{endIndex + 1}="Первый урок"; СРЗНАЧ(AV{endIndex + 1}:BS{endIndex + 1}); ЕСЛИ(F{endIndex + 1}="Обычный урок"; СРЗНАЧ(I{endIndex + 1}:AC{endIndex + 1}); ЕСЛИ(F{endIndex + 1}="Выпускной"; СРЗНАЧ(BT{endIndex + 1}:CH{endIndex + 1}); ЕСЛИ(F{endIndex + 1}="Индивидуальный урок"; СРЗНАЧ(AD{endIndex + 1}:AU{endIndex + 1});ЕСЛИ(F{endIndex + 1}="IND Kids 6-7"; СРЗНАЧ(CI{endIndex + 1}:CX{endIndex + 1});ЕСЛИ(F{endIndex + 1}="Практический урок (7-8 модуль)"; СРЗНАЧ(CV{endIndex + 1}:DN{endIndex + 1});-1))))));2)'
            sheet.update_acell('DY' + str(endIndex + 1), str(middleFunc))
        if work[i]['Отметка времени'] == '':
            break
    work = sheet.get_all_records()
    # Найти конец таблицы и обрезать пустые строки
    endIndex = 0
    for i in range(len(work)):
        endIndex += 1
        # Добавим поле 'Номер заявки'
        work[i]['Номер строки'] = str(endIndex + 1)
        if work[i]['Отметка времени'] == '':
            break

    work = work[:endIndex]
    time.sleep(10)
    # Создадим переменную для рассылки
    recordForSending = []
    # Создадим список с номерами заявок
    ticketsNumber = []
    # Добавим в эту таблицу все не отправленные записи
    for i in work:
        if i['Отправлено уведомление ТЛ'] != 'Да':
            recordForSending.append(i)
            ticketsNumber.append(i['Номер строки'])
    #print(recordForSending)

    messages = {}
    # Добавим в него всех ТЛов
    for i in get_team_leaders():
        messages[i[0]] = []

    # Обрабатываем все записи для отправки и добавляем их в словарь
    print(recordForSending)
    for record in recordForSending:
        message = formatMessage(record)
        try:
            messages[record['Тимлид преподавателя']].append(message)
        except KeyError:
            messages[DEFAULT_TEAMLEADER[0]].append(message)
    return messages, ticketsNumber

def updateTableSendedTickets(tickets):
    for ticket in tickets:
        sheet.update('DZ' + str(ticket), 'Да')
