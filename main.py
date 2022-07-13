import os
import logging
import telebot
from telebot import types
import psycopg2
from config import *
from datetime import datetime
from flask import Flask, request

bot = telebot.TeleBot(BOT_TOKEN) #тестовый бот
server = Flask(__name__)
logger=telebot.logger
logger.setLevel(logging.DEBUG)

#bot = telebot.TeleBot('5594004962:AAE9esiDOQxn2YM8t-2oVakoVeY8SKb3Psk')

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

@bot.message_handler(commands=["start"])
def start(message):
    iduser = message.from_user.id
    f_name = message.from_user.first_name
    s_name = message.from_user.last_name
    dt = datetime.now()
    mess = f'Приветствую, <b>{message.from_user.first_name} <u>{message.from_user.last_name},</u></b> Я - бот приемной комисии СПБГЭТУ "ЛЭТИ" и надеюсь смогу помочь тебе с поиском ответов на твои вопросы!'
    bot.send_message(message.chat.id, mess , parse_mode='html')
    db_object.execute (f"SELECT iduser FROM users WHERE iduser = {iduser}")
    result= db_object.fetchone()
   # db_object.execute("INSERT INTO users (dt) VALEUES (%s)", (dt))
    #db_connection.commit()
    if not result:
         db_object.execute("INSERT INTO users (iduser ,f_name,s_name,dt) VAlUES(%s,%s,%s,%s)", (iduser,f_name,s_name,dt)
         db_connection.commit()
 #bot.delete_message(message.chat.id, message.message_id)

@server.route (f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message ():
    json_string = request.get_data().decode ("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!",200
@bot.message_handler(commands=['menu'])
def menu(message):
     murkup = types.InlineKeyboardMarkup(row_width=1)
     btn1 = types.InlineKeyboardButton("Бюджет", callback_data='first')
     btn2 = types.InlineKeyboardButton('Контракт', callback_data='second')
     btn3 = types.InlineKeyboardButton('Правила приема', url='https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/')
     btn4 = types.InlineKeyboardButton('F A Q',
                                     url='https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/chasto-zadavaemye-voprosy')
     btn5 = types.InlineKeyboardButton('Другое', callback_data='fifth')
     btn6 = types.InlineKeyboardButton('Не знаю куда поступить', callback_data='third')
     murkup.add(btn1, btn2, btn3, btn4, btn5, btn6)
     bot.send_message(message.chat.id, 'Выберете, что вас интересует', reply_markup=murkup)
     bot.delete_message(message.chat.id, message.message_id)
    # bot.delete_message(message.chat.id, message.message_id-1)


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.delete_message(message.chat.id, message.message_id)

@bot.callback_query_handler(func=lambda call: True)
def answer(c):
    if c.data == 'first':
        murkup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Какое колличество мест для приема на 1 курс?', url='https://etu.ru/assets/files/ru/postupaushim/priyom-na-1-y-kurs/2022/kolichestvo-mest-dlya-priema-na-obuchenie.pdf')
        btn2 = types.InlineKeyboardButton('Сроки подачи документов', url='https://etu.ru/assets/files/ru/postupaushim/priyom-na-1-y-kurs/2022/sroki-priema.pdf')
        btn3 = types.InlineKeyboardButton('Сроки приема документов', url='https://etu.ru/assets/files/ru/postupaushim/priyom-na-1-y-kurs/2022/sroki-priema.pdf')
        btn4 = types.InlineKeyboardButton('Общежитие', callback_data='ninth')
        btn5 = types.InlineKeyboardButton('Информация о грантах', callback_data='tenth')
        btn6 = types.InlineKeyboardButton('Назад',callback_data='back')
        murkup.add(btn1, btn2, btn3, btn4, btn5,btn6)
        bot.send_message(c.message.chat.id,
                         'Важно понимать, что в конкурсе на бюджет участвуют только люди, подавшие оригинал аттестата/диплома. И конечно же заявление о согласии на зачисление. А ниже есть полезные документы :)',
                         reply_markup=murkup)

    elif c.data == 'back':
        bot.delete_message(c.message.chat.id, c.message.message_id)
    # return help(c.message) #(Рабочий вернутся назад)#

           #  bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id-1 , reply_markup=None)

    if c.data == 'second':
        murkup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Стоимость обучения',
                                          url='https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/platnoe-obuchenie')
        btn2 = types.InlineKeyboardButton('Минимальные баллы',
                                          url='https://etu.ru/assets/files/ru/postupaushim/priyom-na-1-y-kurs/2022/minimalnoe-kolichestvo-ballov_byudzhet_kontrakt.pdf')
        btn3 = types.InlineKeyboardButton('Скидки для поступающих',
                                          url='https://etu.ru/ru/abiturientam/preimushestva-spbgetu/granty-podderzhki/skidki-dlya-postupayushhih')
        btn4 = types.InlineKeyboardButton('Назад',callback_data='back')

        murkup.add(btn1, btn2, btn3,btn4)
        bot.send_message(c.message.chat.id,
                         'На платное обучение в ЛЭТИ не проводится конкурс, требуется лишь набрать минимальные баллы и успеть оплатить обучение (пока места на желаемом направлении не закончились). Кто оплатил - будет зачислен ближайшим приказом, которые будут выпускаться каждую неделю.',
                         reply_markup=murkup)
    if c.data == 'third':
        murkup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Наши направления подготовки',
                                          url='https://etu.ru/ru/abiturientam/napravleniya-podgotovki/bakalavriat/')
        btn2 = types.InlineKeyboardButton('Количество мест для приема',
                                          url='https://etu.ru/assets/files/ru/postupaushim/priyom-na-1-y-kurs/2022/kcp.pdf')
        btn3 = types.InlineKeyboardButton('Проходные баллы',
                                          url='https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/prohodnye-bally')
        btn4 = types.InlineKeyboardButton('Минимальные баллы', url='https://etu.ru/assets/files/ru/postupaushim/priyom-na-1-y-kurs/2022/minimalnoe-kolichestvo-ballov_byudzhet_kontrakt.pdf')
        btn5 = types.InlineKeyboardButton('Какие ЕГЭ (ВИ) нужны для поступления',url='https://etu.ru/assets/files/ru/postupaushim/priyom-na-1-y-kurs/2022/perechen-vstupitelnyh-ispytanij.pdf')
        btn6 = types.InlineKeyboardButton('Назад',callback_data='back' )
        murkup.add(btn1, btn2, btn3, btn4, btn5,btn6)
        bot.send_message(c.message.chat.id,
                         'Важно понимать, что в конкурсе на бюджет участвуют только люди, подавшие оригинал аттестата/диплома. И конечно же заявление о согласии на зачисление. А ниже есть полезные документы :)',
                         reply_markup=murkup)
    if c.data == 'fourth':
        bot.send_message(c.message.chat.id,
                         'Часто задаваемые вопросы в полном объеме представлены у нас на сайте')
    elif c.data == 'fifth':
        murkup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Документы по приему на 1 курс',
                                          url='https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/')
        btn2 = types.InlineKeyboardButton('Часто задаваемые вопросы по приему',
                                          url='https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/chasto-zadavaemye-voprosy')
        btn3 = types.InlineKeyboardButton('Целевое обучение', url='https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/celevoy-priem')
        btn4 = types.InlineKeyboardButton( 'Все об Индивидуальных достижениях', url='https://etu.ru/assets/files/ru/postupaushim/priyom-na-1-y-kurs/2022/information2.pdf')
        btn5 = types.InlineKeyboardButton ('Назад', callback_data='back1')
        murkup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(c.message.chat.id, 'Хм...сложно угадать какие вопросы у тебя в голове! Но я попробую. Если ответ не найден - напиши вопрос текстом, мои более умные коллеги обязательно помогут!', reply_markup=murkup)
    if c.data == 'ninth':
        murkup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('F.A.Q.',
                                          url='https://etu.ru/ru/vospitatelnaya-i-socialnaya/obshezhitiya/raspredelenie-studentov/chasto-zadavaemye-voprosy')
        btn2 = types.InlineKeyboardButton('Официальная страница по расселению',
                                          url='https://etu.ru/ru/vospitatelnaya-i-socialnaya/obshezhitiya/raspredelenie-studentov/')
        btn3 = types.InlineKeyboardButton('Назад',callback_data='back1')
        murkup.add(btn1, btn2, btn3)
        bot.send_message(c.message.chat.id,
                         'У нас в университете 9 общежитий 5 из которых в пешей доступности. Некоторые блочного типа, некоторые коридорного. '
                         'К сожалению выбирать общежитие на 1 курсе нельзя  ', reply_markup=murkup)
        #bot.delete_message(c.message.chat.id, c.message.message_id)
        #bot.delete_message(c.message.chat.id, c.message.message_id - 1)


    elif c.data == 'back1':
        bot.delete_message(c.message.chat.id, c.message.message_id)
       # bot.delete_message(c.message.chat.id, c.message.message_id - 1)
        #bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id, reply_markup=None)
     #return c.data == 'ninth'
    if c.data == 'tenth':
        murkup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Подробная информация о грантах',
                                          url='https://etu.ru/ru/abiturientam/preimushestva-spbgetu/granty-podderzhki/granty-podderzhki-pervokursnikov-v-spbgetu-leti')
        btn2 = types.InlineKeyboardButton('Назад', callback_data='back1')
        murkup.add(btn1,btn2)
        bot.send_message(c.message.chat.id,
                         'Если твой балл ЕГЭ 260 и выше - можно получить дополнительное финансирование от ЛЭТИ. Тем более, если поступаешь как БВИ! ',
                         reply_markup=murkup)
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port = int(os.environ.get("PORT",5000)))


bot.polling(none_stop=True)
