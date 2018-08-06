import telebot
from telebot import types
import time

API_TOKEN = '655665228:AAGfa7LvWw46UzckGEMbyG3HZ4-XTo3nQ0E'
bot = telebot.TeleBot(API_TOKEN)


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.city = None
        self.movie_name = None
        self.cinema_name = None

user_dict = {}


#TODO
#city_list = get_city_list_from

@bot.message_handler(commands=['movie'])
def show_city_name(message):
    msg = bot.reply_to(message, "Select your city, or enter it")
    bot.register_next_step_handler(msg, process_city_name)

def process_city_name(message):
    try:
        chat_id = message.chat.id
        user = User(chat_id)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, "Tell me movie name")
        bot.register_next_step_handler(msg, process_movie_name)
    except Exception as e:
        bot.reply_to(message, 'please start over')


def process_movie_name(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.movie = message.text
        msg = bot.reply_to(message, "Tell me cinema name")        )
        bot.register_next_step_handler(msg, process_cinema_name)
    except Exception as e:
        pass

def process_cinema_name(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.cinema_name = message.text
        msg = bot.reply_to(message, "select session")
        bot.register_next_step_handler(msg, process_seasions)
    except Exception as e:
        pass

bot.enable_save_next_step_handlers(delay = 2)

bot.load_next_step_handlers()

bot.polling()

