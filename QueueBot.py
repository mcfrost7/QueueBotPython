import telebot
import re
import sys


from StudentClass import Students as Stud


fileToken = open('token.txt','r')
token = fileToken.read()
fileAdmin = open('admin.txt','r')
admin_list = fileAdmin.read().split()

print(admin_list)

db_path = 'D:\Tg_Bots\QueueBot\data'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['description'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот, который отслеживает очередь. \n'
                                      'Чтобы добавить новую пару, напиши мне сообщение в формате ->  \n'
                                      '{Фамилия}  {Имя}  {Название предмета}  {Номер подгруппы}\n'
                                      'Чтобы посмотреть все добавленные пары, напиши мне /show')


@bot.message_handler(commands=['show'])
def show(message):
    try:
        stud = Stud('D:\Tg_Bots\QueueBot\data\StudentsTest.db')
        bot.send_message(message.chat.id, 'Актуальная очередь на сегодня:')
        student_tuple : tuple = stud.show_all()
        for student_list in student_tuple:
            bufer_str : str = ""
            for student_substr in student_list:
                 bufer_str += student_substr + ' '
            bot.send_message(message.chat.id, f'{bufer_str}')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат сообщения. Пожалуйста, введите данные через пробел, соблюдая рекомендации.')


def string_checker(input : str):        
    return re.match('^[А-яа-я0-9]*$',input)

def id_cheker(input : str):
    return admin_list[0] == input or admin_list[1] == input or admin_list[2] == input

def stop_cheker(input : str):
    return admin_list[0] == input

@bot.message_handler(commands=['turnoff'])
def turnoff(message):
    try:
       if stop_cheker(message.from_user.username):
            bot.send_message(message.chat.id, 'Бот выключен.')
            bot.stop_bot()
            sys.exit(0)
       else:
           bot.send_message(message.chat.id, 'У вас нет прав выключать бота.')
    except ValueError:
        bot.send_message(message.chat.id, 'Что-то пошло не так. Бот не выключен.')


@bot.message_handler(content_types=['text'])
def add(message):
    try:

        subgroup_checker = lambda input_subgroup : ((input_subgroup == '1') or (input_subgroup == '2') or (input_subgroup == '0'))
        surname,name, item, subgroup = message.text.split(' ')
        if id_cheker(message.from_user.username):
            if subgroup_checker(subgroup) and string_checker(surname) and string_checker(name) and string_checker(item):
                stud = Stud('D:\Tg_Bots\QueueBot\data\StudentsTest.db')
                stud.add(surname,name,item,subgroup)
                bot.send_message(message.chat.id, ' Добавлена новая запись:\n'
                                                     f'{surname} {name}   \n'
                                                     f'предмет -> {item}   \n'
                                                     f'Подгруппа -> {subgroup} \n')                                                  
            else:
                bot.send_message(message.chat.id, 'Неверный формат сообщения. Пожалуйста, введите данные через пробел, соблюдая рекомендации.')
        else:
            bot.send_message(message.chat.id, 'У вас нет прав срать в БД!')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат сообщения. Пожалуйста, введите данные через пробел, соблюдая рекомендации.')

if __name__ == '__main__':
    bot.delete_webhook(drop_pending_updates=True)
    bot.infinity_polling()