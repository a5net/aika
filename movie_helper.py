import telebot
from telebot import types
import time
from user_class import * 


# class User:
#     def __init__(self, chat_id):
#         self.chat_id = chat_id
#         self.city = None
#         self.movie_name = None
#         self.cinema_name = None

user_dict = {}


#TODO
#city_list = get_city_list_from

@bot.message_handler(commands=['movie'])
def show_city_list(message):
    chat_id = message.chat.id
    user = User(chat_id)
    user_dict[chat_id] = user
    msg = bot.reply_to(message, 
    "")
    bot.register_next_step_handler(msg, show_movie_name)

def show_movie_name(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = bot.reply_to(message,
        " "
        )
        bot.register_next_step_handler(msg, show_cinema_name)
    except Exception as e:
        pass

def show_cinema_name(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = bot.reply_to(message, 
        " ")
        bot.register_next_step_handler(msg, show_seasions)
    except Exception as e:
        pass

def show_sessions(message):
    try:
        chat_id = message.chat.id
        user =  user_dict[chat_id]
        msg = bot.reply_to(message, 
        "")
        bot.send_message(chat_id, )
    except Exception as e:
        pass

