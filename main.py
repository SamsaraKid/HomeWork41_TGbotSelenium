import telebot
import botlib

# читаем токен из файла
file = open('token', 'r')
token = file.readline()
file.close()

# создаём бота
bot = telebot.TeleBot(token)
print('Бот создан')

# создаём кнопки клавиатуры в чате
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.add(telebot.types.InlineKeyboardButton(text='погода', callback_data='weather'))
keyboard.add(telebot.types.InlineKeyboardButton(text='анекдот', callback_data='anekdot'))

# создаём кнопки меню
markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row('/погода', '/анекдот')
markup.row('/start', '/stop')

# старт бота
@bot.message_handler(commands=['start'])
def start_mes(info):
    print(info.from_user.username, 'послал(а) команду /start')
    bot.send_message(info.chat.id, 'Выберите команду', reply_markup=keyboard)  # выводим клавиатуру в чате
    bot.send_message(info.chat.id, 'Или воспользуйтесь меню', reply_markup=markup)  # создаём меню

# скрываем меню
@bot.message_handler(commands=['stop'])
def stop_mes(info):
    print(info.from_user.username, 'послал(а) команду /stop')
    markup_hide = telebot.types.ReplyKeyboardRemove()
    bot.send_message(info.chat.id, '/start для возобновления работы', reply_markup=markup_hide)

# обработка текстовых команд
@bot.message_handler(content_types=['text'])
def message(info):
    print(info.from_user.username, 'послал(а) команду', info.text)
    try:
        if 'привет' in info.text.lower():
            mes = 'hi'
        elif 'пока' in info.text.lower():
            mes = 'by'
        elif 'погода' in info.text.lower():
            bot.send_message(info.chat.id, 'Проверяю погоду...')
            mes = botlib.weather()
        elif 'анекдот' in info.text.lower():
            bot.send_message(info.chat.id, 'Ищу анекдот...')
            mes = botlib.anekdot()
        else:
            mes = 'Неверная команда'
        bot.send_message(info.chat.id, mes)
    except:
        bot.send_message(info.chat.id, 'Произошла ошибка, попробуйте ещё раз')
    bot.send_message(info.chat.id, 'Выберите команду', reply_markup=keyboard)

# обработка команд от кнопок в чате
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    print(call.from_user.username, 'послал(а) команду', call.data)
    try:
        if call.data == 'weather':
            bot.send_message(call.message.chat.id, 'Проверяю погоду...')
            mes = botlib.weather()
        elif call.data == 'anekdot':
            bot.send_message(call.message.chat.id, 'Ищу анекдот...')
            mes = botlib.anekdot()
        else:
            mes = 'Неверная команда'
        bot.send_message(call.message.chat.id, mes)
    except:
        bot.send_message(call.message.chat.id, 'Произошла ошибка, попробуйте ещё раз')
    bot.send_message(call.message.chat.id, 'Выберите команду', reply_markup=keyboard)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)

