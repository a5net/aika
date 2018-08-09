import telebot
from telebot import types
import time
from movie import *

API_TOKEN = '184429324:AAG4AbqtubyehDiFqgKItv4JE_bG0Dz5FTc'# это @GinetBot
# API_TOKEN = "695195394:AAEsxvvCgKTClHNKL2ElIYbN_iBZYhHki-U"
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

city_dict_names_as_key = get_city_dict()
city_list_for_movie = city_dict_names_as_key.keys()
city_dict_id_as_key = {}


for x in city_list_for_movie:
    city_dict_id_as_key[city_dict_names_as_key[x]] = x



def draw_city_list():
    markup = types.InlineKeyboardMarkup()
    for x in city_list_for_movie:
        markup.add(types.InlineKeyboardButton(x, callback_data="movie " + str(city_dict_names_as_key[x])))
    return markup

def draw_movie_list(city_id):
    markup = types.InlineKeyboardMarkup()
    movie_list = get_movie_list(city_id)
    for x in movie_list:
        markup.add(types.InlineKeyboardButton(text=x, callback_data="cinema " + str(get_movie_id(city_id, x))))
    markup.add(types.InlineKeyboardButton("Назад к выбору города", callback_data="back_to_city"))
    return markup

def draw_cinema_list(city_id):
    cinema_list = get_cinema_list(city_id)
    markup = types.InlineKeyboardMarkup()
    for x in cinema_list:
        markup.add(types.InlineKeyboardButton(text=x, callback_data="sessions " + x))
    markup.add(types.InlineKeyboardButton("Назад к выбору фильма", callback_data="back_to_movie"))
    return markup

def draw_seesions_list(city_id, movie_id, cinema_id, cinema_name):
    markup = types.InlineKeyboardMarkup()
    sessions_list = get_session_list(city_id, movie_id, cinema_id)
    print(sessions_list)
    for x in sessions_list:
        markup.add(types.InlineKeyboardButton(text=x, callback_data="ignore"))
    markup.add(types.InlineKeyboardButton(text="Купить билеты в " + cinema_name, url=get_ticket_url(cinema_name, city_id)))
    markup.add(types.InlineKeyboardButton(text="Назад к выбору кинотеатра", callback_data="back_to_cinema"))
    return markup



@bot.message_handler(commands=['movie'])
def start_movie_helper(message):
    chat_id = message.chat.id
    text = message.text
    city_id = extract_city_id(text)
    user = User(chat_id)
    if(city_id == 0):
        markup = draw_city_list()
        bot.send_message(chat_id, "Movie Bot", reply_markup=markup)
    else:
        markup = draw_movie_list(city_id)
        bot.send_message(chat_id, "Movie Bot", reply_markup=markup)
        user = User(chat_id)
        user.city_id = city_id
        user.cinema_name = city_dict_id_as_key[city_id]        
        user_dict[chat_id] = user
    
@bot.callback_query_handler(func=lambda call: True)
def message_query_handler(call):
    print(call.data)
    raw_message = call.data.split()
    message_type = raw_message[0]
    message = ' '.join(raw_message[1:])
    
    chat_id = call.message.chat.id
    try:
        user = user_dict[chat_id]
    except:
        user = User(chat_id)
        user_dict[chat_id] = user
    if(message_type == 'city' or message_type == 'back_to_city'):
        markup = draw_city_list()
        bot.edit_message_text(text='Выберите город из списка ниже: ', chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=markup)
    if(message_type == 'movie' or message_type == 'back_to_movie'):
        if(message_type == 'movie'):
            user.city = city_dict_id_as_key[int(message)]
            user.city_id = int(message)
            user_dict[chat_id] = user
        markup = draw_movie_list(user.city_id)
        bot.edit_message_text(text='Какой фильм хотите посмотреть?', chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=markup)
    if(message_type == 'cinema' or message_type == 'back_to_cinema'):
        if(message_type == 'cinema'):
            movie_list = get_movie_list(user.city_id)
            for x in movie_list:
                if(get_cinema_id(user.city_id, x) == int(message)):
                    user._movie_name = x
            user.movie_id = int(message)
            user_dict[chat_id] = user
        markup = draw_cinema_list(user.city_id)
        bot.edit_message_text(text='Выберите кинотеатр из списка ниже', chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=markup)
    if(message_type == 'sessions'):
        user.cinema_name = message
        user.cinema_id = get_cinema_id(user.city_id, user.cinema_name)
        markup = draw_seesions_list(user.city_id, user.movie_id, user.cinema_id, user.cinema_name)
        user_dict[chat_id] = user
        bot.edit_message_text(text='А вот и сеансы', chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=markup)
    if(message_type == 'ignore'):
        bot.answer_callback_query(call.id, text="")

@bot.message_handler(commands=['astana'])
def start(message , text):
    city_id = extract_city_id(text)
    print(city_id)
    markup = draw_movie_list(city_id)
    chat_id = message.chat.id
    bot.send_message(chat_id, "Какой фильм хотите посмотреть?", reply_markup=markup)
    user = User(chat_id)
    user.city_id = city_id
    user.city_name = city_dict_id_as_key[city_id]        
    user_dict[chat_id] = user

bot.polling(none_stop=True)