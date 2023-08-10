import telebot
import botlib

file = open('token', 'r')
token = file.readline()
bot = telebot.TeleBot(token)
# bot.send_message(5787921322, 'Бот запущен')
# если бот получил сообщение типа text
@bot.message_handler(content_types=['text'])
def message(info):
    for key in info.__dict__.keys():
        print(key, info.__dict__[key])
    print(info.chat.id)
    if 'привет' in info.text.lower():
        mes = 'hi'
    elif 'пока' in info.text.lower():
        mes = 'by'
    elif 'погода' in info.text.lower():
        mes = botlib.weather()
    elif 'анекдот' in info.text.lower():
        mes = botlib.anekdot()
    else:
        mes = 'Неверная команда, повторите'
    bot.send_message(info.chat.id, mes)

bot.polling(none_stop=True)

