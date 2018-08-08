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
        self.city_id = None
        self.movie_id = None
        self.movie_name = None
        self.cinema_name = None
        self.cinema_id = None

user_dict = {}
city_list_for_movie = get_city_dict().keys()


def draw_city_list():
    markup = types.InlineKeyboardMarkup()
    for x in city_list_for_movie:
        markup.add(types.InlineKeyboardButton(x, callback_data="movie"))
    return markup

def draw_movie_list(city_id):
    markup = types.InlineKeyboardMarkup()
    movie_list = get_movie_list(city_id)
    markup.add(types.InlineKeyboardButton("Выберите название фильма", callback_data="ignore"))
    for x in movie_list:
        markup.add(types.InlineKeyboardButton(x, callback_data="cinema"))
    markup.add(types.InlineKeyboardButton("Назад к выбору города", callback_data="back_to_city"))
    return markup

def draw_cinema_list(city_id):
    cinema_list = get_cinema_list(city_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Выберите название кинотеатра", callback_data="ignore"))
    for x in cinema_list:
        markup.add(types.InlineKeyboardButton(x, callback_data="sessions"))
    markup.add(types.InlineKeyboardButton("Назад к выбору фильма", callback_data="back_to_movie"))
    return markup

def draw_seesions_list(city_id, movie_id, cinema_id, cinema_name):
    markup = types.InlineKeyboardMarkup()
    sessions_list = get_session_list(city_id, movie_id, cinema_id)
    for x in sessions_list:
        markup.add(types.InlineKeyboardButton(x, callback_data="ignore"))
    markup.add(types.InlineKeyboardButton(text="Купить билеты", url=get_ticket_url(cinema_name, city_id)))
    markup.add(types.InlineKeyboardButton("Назад к выбору кинотеатра", callback_data="back_to_cinema"))
    return markup

@bot.message_handler(commands=['movie'])
def start_movie_helper(message):
    chat_id = message.chat.id
    text = message.text
    city_id = extract_city_id(text)
    
    if(city_id == 0):
        markup = draw_city_list()
        bot.send_message(chat_id, "Movie Bot", reply_markup=markup)
    else:
        markup = draw_movie_list(city_id)
        bot.send_message(chat_id, "Movie Bot", reply_markup=markup)
        user = User(chat_id)
        user_dict[chat_id] = user
    
@bot.callback_query_handler(func=lambda call: True)
def message_query_handler(call):
    message_type = call.data
    message = call.message.text
    chat_id = call.message.chat.id
    user = User(chat_id)

    if(message_type == 'city' or message_type == 'back_to_city'):
        markup = draw_city_list()
        bot.edit_message_text('Movie Bot', call.from_user.id, call.message.message_id, reply_markup=markup)
    if(message_type == 'movie' or message_type == 'back_to_movie'):
        user.city = message
        city_dict = get_city_dict()
        user.city_id = city_dict[message]
        user_dict[user.chat_id] = user
        markup = draw_movie_list(user.city_id)
        bot.edit_message_text('Movie Bot', call.from_user.id, call.message.message_id, reply_markup=markup)
    if(message_type == 'cinema' or message_type == 'back_to_cinema'):
        user.movie_name = message
        user.movie_id = get_movie_id(user.city_id, message)
        markup = draw_cinema_list(user.city_id)
        bot.edit_message_text('Movie Bot', call.from_user.id, call.message.message_id, reply_markup=markup)
    if(message_type == 'sessions'):
        user.cinema_name = message
        user.Cinema_id = get_cinema_id(user.city_id, user.cinema_name)
        markup = draw_seesions_list(user.city_id, user.movie_id, user.cinema_id, user.cinema_name)
        bot.edit_message_text('Movie Bot', call.from_user.id, call.message.message_id, reply_markup=markup)

bot.polling(none_stop=True)