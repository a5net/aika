import telebot
from telebot import types
import time
from movie import *

API_TOKEN = '184429324:AAG4AbqtubyehDiFqgKItv4JE_bG0Dz5FTc'
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
    raw_city_text = message.text
    city_id = extract_city_id(raw_city_text)
    if city_id == 0:
        user = User(message.chat.id)
        user_dict[message.chat.id] = user
        markup = types.ReplyKeyboardMarkup(resize_keyboard=true)
        city_list_name_movie = get_city_dict()
        city_names_movie = city_list_name_movie.keys()
        for x in city_names_movie:
            b = types.KeyboardButton(x)
            markup.add(b)
        msg = bot.send_message(message.chat.id, 'Пожалуйста, выберите название города из списка', reply_markup=markup)
        bot.register_next_step_handler(msg, process_city_name)
    else:
        user = User(message.chat.id)
        user.city = city_id
        user_dict[message.chat.id] = user
        markup = types.ReplyKeyboardMarkup(resize_keyboard=true)
        movie_list = get_movie_list(city_id)
        for x in movie_list:
            markup.add(types.KeyboardButton(x))        
        msg = bot.send_message(message.chat.id, 'Выберите название фильма', reply_markup=markup)
        bot.register_next_step_handler(msg, process_movie_name)

def process_city_name(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        city_dict = get_city_dict()
        city_id = city_dict[message.text]
        user.city = city_id
        user_dict[chat_id] = user
        markup = types.InlineKeyboardMarkup()
        movie_list = get_movie_list(city_id)
        for x in movie_list:
            markup.add(types.InlineKeyboardButton(x))        
        msg = bot.send_message(message.chat.id, 'Выберите название фильма', reply_markup=markup)
        bot.register_next_step_handler(msg, process_movie_name)
    except Exception as e:
        bot.reply_to(message, 'Error in process_city_name')


def process_movie_name(message):
    try:
        chat_id =message.chat.id
        user = user_dict[chat_id]
        user.movie_name = get_movie_id(user.city, message.text)
        user_dict[chat_id] = user

        cinema_list = get_cinema_list(user.city)
        markup = types.InlineKeyboardMarkup()
        for x in cinema_list:
            markup.add(types.InlineKeyboardButton(x))
        msg = bot.send_message(chat_id, 'Выберите название кинотеатра', reply_markup=markup)
        bot.register_next_step_handler(msg, process_cinema_name)
    except Exception as e:
        bot.reply_to(message, 'Error in process_movie_name')

def process_cinema_name(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.cinema_name = get_cinema_id(user.city, message.text)
        user[chat_id] = user

        sessions_list = get_session_list(user.city, user.movie_name, user.cinema_name)
        markup = types.InlineKeyboardMarkup()
        for x in sessions_list:
            markup.add(types.InlineKeyboardButton(x))
        markup.add(types.InlineKeyboardButton('Купить билеты', url=get_ticket_url(message.text, user.city)))
        if(len(sessions_list) != 0):
            bot.send_message(chat_id, movie_description(user.city, user.movie_name))
            msg = bot.send_message(chat_id, 'Выберите сеанс', reply_markup=markup)
            # bot.register_next_step_handler(msg, get_link)
        else:
            msg = bot.send_message(chat_id, 'К сожелению в данном кинотеатре не показывают ваш фильм, выберите другой')
        
    except Exception as e:
        pass    

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()
