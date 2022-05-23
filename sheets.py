import pprint
from google_sheet_client import client
from teamleaders import get_team_leaders, DEFAULT_TEAMLEADER

# Открываем табличку
spreadsheet_id = '1q6hf-FfKLB1seAguqS4SDTuMZnLVFLMKssVPIqPh-XA'
sheet = client.open_by_key(spreadsheet_id).worksheet('Заявки')

# Функция для форматирования сообщений
def formatMessage(record):
    text = str(record['Выберите ответственного ТЛ']) + '\n\n' + \
        '‼️Заявка № ' + str(record['Номер заявки']) + '\n' + \
        'Для преподавателя: ' + str(record['Укажите ФИО преподавателя']) + '\n' + \
        '🎓 На ученика ' + str(record['Укажите ФИО ученика ']) + ' из группы ' + str(record['Группа ученика (формат цифры, например, Онлайн120_В-10)']) + '\n' + \
        '📱 Контакты: ' + str(record['Контакты ученика, часовой пояс, если не мск. Если нужно имя родителя + контакты. Есть ли мессенджер, какой?']) + '\n' + \
        '📚 Модуль и урок: ' + str(record['На каком модуле и прошедший урок у ученика (формат М5У3)']) + '\n' + \
        '📝 Комментарий КМа: ' + str(record['Причина назначения дополнительного урока']) + '\n'

    if record['От кого заявка, укажите должность'] == 'Кризис-менеджер':
        text = '❗❗❗ КРИТИЧЕСКАЯ ЗАЯВКА ❗❗❗'+'\n\n' + text
        text = text + '❗Что нужно проработать: ' + record['Что мы пообещали (поле для кризис-менеджеров, какие негативные впечатления обещали проработать)'] + '\n'
    if str(record['До какого числа нужно провести доп?']) != '':
        text = text + '🕐Урок нужно провести до: ' + str(record['До какого числа нужно провести доп?'])
    return text

def getMessages():
    # Забираем все записи их таблицы
    work = sheet.get_all_records()
    # print(work)
    # Найти конец таблицы и обрезать пустые строки
    endIndex = 0
    for i in range(len(work)):
        # Добавим поле 'Номер заявки'
        work[i]['Номер заявки'] = str(endIndex + 2)
        endIndex += 1
        if work[i]['Укажите ФИО ученика '] == '':
            break
    work = work[:endIndex - 1]

    # Создадим переменную для рассылки
    recordForSending = []
    # Создадим список с номерами заявок
    ticketsNumber = []
    # Добавим в эту таблицу все не отправленные записи
    for i in work:
        if i['Да'] != 'Да':
            recordForSending.append(i)
            ticketsNumber.append(i['Номер заявки'])
    # Вывод записей для отправки
    # pp = pprint.PrettyPrinter()
    # pp.pprint(recordForSending)

    # Создадим словарь для отправки
    messages = {}
    # Добавим в него всех ТЛов
    for i in get_team_leaders():
        messages[i[0]] = []

    # Обрабатываем все записи для отправки и добавляем их в словарь
    for record in recordForSending:
        try:
            messages[record['Выберите ответственного ТЛ']].append(formatMessage(record))
        except KeyError:
            messages[DEFAULT_TEAMLEADER[0]].append(formatMessage(record))
    return messages, ticketsNumber

def updateTableSendedTickets(tickets):
    for ticket in tickets:
        sheet.update('N' + str(ticket), 'Да')

def updateTableCell(cell, number, value):
    sheet.update(str(cell) + str(number), value)
