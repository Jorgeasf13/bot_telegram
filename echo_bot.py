import telebot
import datetime
from telebot import types

import sqlite3

conn = sqlite3.connect('clientes.db', check_same_thread= False)
cursor = conn.cursor()




API_TOKEN = '<930897758:AAFcce3GwyeOEwS7smiZYDlZUUXQgI9C1dk>'

bot = telebot.TeleBot("930897758:AAFcce3GwyeOEwS7smiZYDlZUUXQgI9C1dk")


user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None





# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start', 'Oi', 'Olá'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Olá, qual o seu nome?
""")
    bot.register_next_step_handler(msg, process_name_step)



def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        hora_atual = datetime.datetime.now().hour
        if 6 <= hora_atual and hora_atual < 12:
            msg = bot.reply_to(message, 'Bom dia '+ name + ' ,qual a sua idade?')
        elif 12 <= hora_atual and hora_atual < 18:
            msg = bot.reply_to(message, 'Boa tarde '+ name + ' ,qual a sua idade?')
        else:
            msg = bot.reply_to(message, 'Boa noite '+ name + ' ,qual a sua idade?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, e)
        bot.reply_to(message, 'oooops')



def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Tem que ser um número')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Masculino', 'Feminino')
        msg = bot.reply_to(message, 'Qual o seu sexo?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, e)
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Masculino') or (sex == u'Feminino'):
            user.sex = sex
        else:
            raise Exception()
        bot.send_message(chat_id, f"Prazer em te conhecer {user.name} \nIDADE {user.age} \n SEXO {user.sex}")
        cursor.execute(f"""
            INSERT INTO clientes(nome, idade, sexo)
            VALUES ("{user.name}", {user.age}, "{user.sex}")
        """)
        conn.commit()
        print("Dados inseridos com sucesso.")
        
    except Exception as e:
        bot.reply_to(message, 'oooops')
        print(e)

@bot.message_handler(commands=['data', 'dados'])
def send_data(message):
    try:
        cursor.execute("""
        SELECT * FROM clientes;
        """)
        resultado = ' '
        for linha in cursor.fetchall():
            resultado += f"{linha}"
        bot.send_message(message.chat.id, resultado)
    except Exception as e:
        print(e)
        conn.close()

bot.enable_save_next_step_handlers(delay=2)


bot.load_next_step_handlers()

bot.polling()





