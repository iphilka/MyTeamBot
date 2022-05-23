import pprint
from google_sheet_client import client
from teamleaders import DEFAULT_TEAMLEADER, get_team_leaders

# Переменные
TEAMLEADERS = {
    'TEAM_LEAD1': ["Луговой Филипп ТЛ1", "f.lugovoy@kodland.team"],
    'TEAM_LEAD2': ["Логачев Артём ТЛ2", "a.logachev@kodland.team"],
    'TEAM_LEAD3': ["Николаева Анастасия ТЛ3", "n.nikolaeva@kodland.team"],
    'TEAM_LEAD4': ["Шуралева Майя ТЛ4", "m.shuravleva@kodland.team"],
    'TEAM_LEAD5': ["Мужагитова Юлия ТЛ5", "yu.muzhagitova@kodland.team"],
    'TEAM_LEAD6': ["Кирьянов Михаил ТЛ6", "m.kiryanov@kodland.team"],
    'TEAM_LEAD7': ["Кошкин Анатолий ТЛ7", "a.koshkin@kodland.team"],
    'TEAM_LEAD8': ["Дроздов Никита ТЛ8", "n.drozdov@kodland.team"],
    'TEAM_LEAD9': ["Пуртова Милана ТЛ9", "m.purtova@kodland.team"],
    'TEAM_LEAD10': ["Киселев Дмитрий ТЛ10", "d.kiselev@kodland.team"],
    'TEAM_LEAD11': ["Исайко Антон ТЛ11", "a.isayko@kodland.team"],
    'TEAM_LEAD12': ["Никитенко Анна ТЛ12", "a.nikitenko@kodland.team"],
    'TEAM_LEAD13': ["Дернов Самат ТЛ13", "s.dernov.bekkulov@kodland.team"],
    'TEAM_LEAD14': ["Елфимов Иван ТЛ14", "i.elfimov@kodland.team"],
    'TEAM_LEAD15': ["Козьменко Александр ТЛ15", "a.kozmenko@kodland.team"],
    'TEAM_LEAD16': ["Теркунова Светлана ТЛ16", "s.terkunova@kodland.team"],
    'TEAM_LEAD17': ["Кимайкина Екатерина ТЛ17", "e.kimajkina@kodland.team"],
    'TEAM_LEAD18': ["Никитенко Яна ТЛ18", "ya.nikitenko@kodland.team"],
    'TEAM_LEAD19': ["Горохова Милена ТЛ19", "m.gorohova@kodland.team"],
    'TEAM_LEAD20': ["Самкова Елена ТЛ20", "e.samkova@kodland.team"],
    'TEAM_LEAD21': ["Короткова Дарья ТЛ21", "d.korotkova@kodland.team"],
    'TEAM_LEAD_O1': ["Беловолова Ольга ТЛО 1", "ol.belovolova@kodland.team"],
    'TEAM_LEAD_O2': ["Малетина Кристина ТЛО 2", "k.maletina@kodland.team"],
    'TEAM_LEAD_03': ["Хмыров Владимир ТЛО 3", "v.khmyrov@kodland.team"],
    'TEAM_LEAD_04': ["Штефан Михаил ТЛО 4", "m.shtefan@kodland.team"]
}

# Открываем табличку
spreadsheet_id = '1cxtiswV1Y38Ibci3YDdm5oby4tra3YI-ThtEFeS57xk'
sheet = client.open_by_key(spreadsheet_id).worksheet('Ответы на форму (1)')

def formatMessage(records):
    text = '👿 Проблема! 👿' + '\n' + 'Преподаватель ' + str(records['Фамилия и имя преподавателя']) + ' попросил замену' + '\n' + \
        'Дата урока: ' + str(records['Дата урока, на который нужна замена']) + '\n' + \
        'Причина: ' + str(records['Причина отсутствия возможности провести урок (необходим подробный комментарий причины отсутствия. Варианты "По семейным обстоятельствам", "Форс-мажор" и тп не принимаются)']) + '\n'
    if str(records['Укажите кандидата на замену Вашего урока (Фамилия имя)']) == '':
        text = text + '🪓 Замена не указана'
    else:
        text = text +'🎉 Кандидатура на замену ' + str(records['Укажите кандидата на замену Вашего урока (Фамилия имя)'])
    return text

def getMessages():
    # Забираем все записи их таблицы
    work = sheet.get_all_records()
    # print(work)
    # Найти конец таблицы и обрезать пустые строки
    endIndex = 0
    for i in range(len(work)):
        endIndex += 1
        # Добавим поле 'Номер заявки'
        work[i]['Номер строки'] = str(endIndex + 1)

        if work[i]['Отметка времени'] == '':
            break
    work = work[:endIndex]

    # Создадим переменную для рассылки
    recordForSending = []
    # Создадим список с номерами заявок
    ticketsNumber = []
    # Добавим в эту таблицу все не отправленные записи
    for i in work:
        if i['Отправлено уведомление ТЛ'] != 'Да':
            recordForSending.append(i)
            ticketsNumber.append(i['Номер строки'])
    # Добавим в него всех ТЛов
    for i in get_team_leaders():
        messages[i[0]] = []

    # Обрабатываем все записи для отправки и добавляем их в словарь
    print(recordForSending)
    for record in recordForSending:
        message = formatMessage(record)
        try:
            messages[record['Твой тимлид']].append(message)
        except KeyError:
            messages[DEFAULT_TEAMLEADER[0]].append(message)
    return messages, ticketsNumber

def updateTableSendedTickets(tickets):
    for ticket in tickets:
        sheet.update('R' + str(ticket), 'Да')
