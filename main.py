import bot
from bot.bot import Bot
from bot.handler import MessageHandler, CommandHandler, HelpCommandHandler
import schedule
import time
import threading
import sheets
import cancellationSheet
#import feedback
from teamleaders import get_team_leaders_dict
import gspread

CHAT = "???"
LOG_CHAT = "???"
TOKEN = "???"
NAME = "KodlandNotificationBot"
bot = Bot(token=TOKEN, name=NAME, is_myteam=True)

def notification():
    teamleaders = get_team_leaders_dict()
    messages, ticketsNumber = sheets.getMessages()
    for i in messages.keys():
        for j in messages[i]:
            print(j)
            bot.send_text(chat_id=teamleaders[i], text=j)
            # Отправка сообщения в общий чат
            bot.send_text(chat_id=CHAT, text=j)
    sheets.updateTableSendedTickets(ticketsNumber)

def cancellationNotification():
    messages, ticketsNumber = cancellationSheet.getMessages()
    teamleaders = get_team_leaders_dict()
    for i in messages.keys():
        for j in messages[i]:
            print(j)
            bot.send_text(chat_id=teamleaders[i], text=j)
            # Отправка сообщения в общий чат
            # bot.send_text(chat_id=CHAT, text=j)
    cancellationSheet.updateTableSendedTickets(ticketsNumber)

# def feedbackNotification():
#     messages, ticketsNumber = feedback.getMessages()
#     for i in messages.keys():
#         for j in messages[i]:
#             print(j)
#             bot.send_text(chat_id=TEAMLEADERS[i], text=j)
#             # Отправка сообщения в общий чат
#             # bot.send_text(chat_id=CHAT, text=j)
#     feedback.updateTableSendedTickets(ticketsNumber)


schedule.every(5 * 60).seconds.do(notification)
#schedule.every(200).seconds.do(cancellationNotification)
#schedule.every(300).seconds.do(feedbackNotification)

def go():
    while 1:
        try:
            schedule.run_pending()
            time.sleep(1)
        except gspread.exceptions.APIError as exc:
            print("Google sheet error", str(exc))
            pass

t = threading.Thread(target=go, name="тест")
t.start()

def message_cb(bot, event):
    bot.send_text(chat_id=event.from_chat, text=event.text)

def help_cb(bot, event):
    text = event.from_chat + '\n\n' + event.data['text']
    bot.send_text(chat_id=LOG_CHAT, text=text)
    text = 'Доступные команды: \n' + \
        '/setstat - позволяет установить статус "Передано" одной заявке в таблице с допами \n' + \
        'Пример использования: /setstat 1234 \n' + \
        '/setdate - позволяет установить Дату и Время в ячейке "F" \n' + \
        'Пример использования: /setdate 1234 29.09 17:40 \n'
    bot.send_text(chat_id=event.from_chat, text=text)

def setStatusFirst_cb(bot, event):
    text = event.from_chat + '\n\n' + event.data['text']
    bot.send_text(chat_id=LOG_CHAT, text=text)
    ticketNumber = event.data['text'].split()
    sheets.updateTableCell('G', ticketNumber[1], 'Передано')
    bot.send_text(chat_id=event.from_chat, text="Изменение статуса в заявку №" + ticketNumber[1] + " внесено")

def setDate_cb(bot, event):
    text = event.from_chat + '\n\n' + event.data['text']
    bot.send_text(chat_id=LOG_CHAT, text=text)
    ticketNumber = event.data['text'].split()
    sheets.updateTableCell('F', ticketNumber[1], ticketNumber[2] + ' ' + ticketNumber[3])
    sheets.updateTableCell('G', ticketNumber[1], 'Назначен')
    bot.send_text(chat_id=event.from_chat, text="Дата и статус в заявке №" + ticketNumber[1] + " изменены")

if __name__ == '__main__':
    # bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
    bot.dispatcher.add_handler(CommandHandler(command="setdate", callback=setDate_cb))
    bot.dispatcher.add_handler(CommandHandler(command="setstat", callback=setStatusFirst_cb))
    bot.dispatcher.add_handler(HelpCommandHandler(callback=help_cb))
    bot.start_polling()
    bot.idle()
