from weather_predict import *
import random
from classify import *
from translate import *
import telebot
from speech_to_text import *
import requests
from emoji import emojize
from telebot import types
from movie import *


token = '695195394:AAEsxvvCgKTClHNKL2ElIYbN_iBZYhHki-U'

Wrench = emojize(":wrench:", use_aliases=True)
Movie_camera = emojize(":movie_camera:", use_aliases=True)
Earth = emojize(":earth_asia:", use_aliases=True)
Speach_baloon = emojize(":speech_balloon:", use_aliases=True)

answer_how_old = ["Буквально пару часов назад, на коленках дописали", "Да вот, в такси дописали только что"]
answer_who_are_you = ["Меня зовут Айка", "Я голосовой ассистент Айка"]
answer_greetings = ["Привет!", "Здравствуй", "Приветствую!", "Здравствуйте"]
answer_greetings_mood = ["Привет. Пойдет. Как у тебя?", "Здравствуй. Хорошо. Как у тебя?", "Приветствую. Нормально. Как у тебя?", "Здарова. Неплохо. Как у тебя?", "Здравствуйте. Все отлично. Как у вас?"]
answer_mood = ["Замечательно, спасибо!!", "Хорошо. Как у тебя дела?", "Все нормально. Как у вас?", "Все отлично. Как у тебя?", "Пойдет. А у тебя?"]
answer_philosophy = ['42']
answer_action = ['Разговариваю с тобой', 'Существую', 'Тихо жду здесь пока у меня что-то спросят']
answer_status_good = ['Рада слышать', 'Круто', 'Отлично!', 'Я очень рада :)']
help_text = ('''Я являюсь виртуальным помощником который может понимать ваши текстовые и аудио сообщения\n\n.
    {}Благодаря этому я могу выполнять следующие функций:

    {}Я могу выдать вам точный прогноз погоды на четыре дня. Для этого вы можете например спросить: \n "Какая погода завтра в Астане"
    
    {}Я могу искать сеансы фильмов для вас. Чтобы ее работы вы можете написать, например: "афиша кино" или просто "фильмы"
    
    {}Я могу просто вести обычный человеческий дилаог. Если хотите можете например написать "Привет. Как дела? ''').format(Wrench, Earth, Movie_camera, Speach_baloon)
start_text = ('''Здравствуйте!
        Я виртуальный помощник Айка. С моей помощью вы можете получить прогноз погоды на ближайшие дни, найти для себя сеанс в кино а также я просто умею разговаривать подробней обо каждой функций вы можете узнать по запросу /help''')

bot = telebot.TeleBot(token)
print("Программа запущена")

def get_voice(message):
    speech_url = 'https://tts.voicetech.yandex.net/generate?text={}&format=mp3&quality=lo&lang=ru-RU&speaker=oksana&emotion=good&key=c3667808-f5a2-4c52-8f90-699a3e23e4f2'.format(message)
    doc = requests.get(speech_url)
    with open('audio.ogg', 'wb') as f:
        f.write(doc.content)
    voice = open('audio.ogg', 'rb')
    return voice

@bot.message_handler(content_types=["text","voice"])
def handle_message(message):
    if message.text:
        command = message.text
        try:
            if(command == '/start'):
                bot.send_message(message.chat.id, start_text)
            else:
                predicted_class = classify(command)
                if(predicted_class == 'weather'):
                    output, speech = get_weather(command)
                    bot.send_message(message.chat.id, output)
                elif(predicted_class == 'cinema'):
                    movie_start(message, message.text)
                elif(predicted_class == 'greetings'):
                    bot.send_message(message.chat.id, answer_greetings[random.randint(0,(len(answer_greetings)-1))])
                elif(predicted_class == 'greetings_mood'):
                    bot.send_message(message.chat.id, answer_greetings_mood[random.randint(0,(len(answer_greetings_mood)-1))])
                elif(predicted_class == 'mood'):
                    bot.send_message(message.chat.id, answer_mood[random.randint(0,(len(answer_mood)-1))])
                elif(predicted_class == 'philosophy'):
                    bot.send_message(message.chat.id, answer_philosophy[0]) 
                elif(predicted_class == 'help'):
                    bot.send_message(message.chat.id, help_text) 
                elif(predicted_class == 'action'):
                    bot.send_message(message.chat.id, answer_action[random.randint(0,(len(answer_action)-1))])
                elif(predicted_class == 'status_good'):
                    bot.send_message(message.chat.id, answer_status_good[random.randint(0,(len(answer_status_good)-1))])
                elif(predicted_class == 'how_old'):
                    bot.send_message(message.chat.id, answer_how_old[random.randint(0,(len(answer_status_good)-1))])
                elif(predicted_class == 'who_are_you'):
                    bot.send_message(message.chat.id, answer_who_are_you[random.randint(0,(len(answer_status_good)-1))])
                else:
                    bot.send_message(message.chat.id, 'Извините, я вас не понимаю, но я учусь :3')
        except:
            pass
    else:
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        try:
            command = speech_to_text(bytes=file.content)
        except:
            bot.send_message(message.chat.id, 'Распознование голоса не удалось, попробуйте снова')
        try:    
            predicted_class = classify(command)
            if(predicted_class == 'weather'):
                output, speech = get_weather(command)
                voice = get_voice(speech)
                bot.send_message(message.chat.id, output)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'cinema'):
                movie_start(message, command)
            elif(predicted_class == 'greetings'):
                answer = answer_greetings[random.randint(0,(len(answer_greetings)-1))]
                voice = get_voice(answer)
                # bot.send_message(message.chat.id, message)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'greetings_mood'):
                answer = answer_greetings_mood[random.randint(0,(len(answer_greetings_mood)-1))]
                voice = get_voice(answer)
                # bot.send_message(message.chat.id, answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'mood'):
                answer = answer_mood[random.randint(0,(len(answer_mood)-1))]
                voice = get_voice(answer)
                # bot.send_message(message.chat.id, answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'philosophy'):
                answer = answer_philosophy[0]
                voice = get_voice(answer)
                # bot.send_message(message.chat.id, answer)
                bot.send_voice(message.chat.id, voice) 
            elif(predicted_class == 'action'):
                answer = answer_action[random.randint(0,(len(answer_action)-1))]
                voice = get_voice(answer)
                # bot.send_message(message.chat.id, answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'status_good'):
                answer = answer_status_good[random.randint(0,(len(answer_status_good)-1))]
                voice = get_voice(answer)
                # bot.send_message(message.chat.id, answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'how_old'):
                answer = answer_how_old[random.randint(0,(len(answer_status_good)-1))]
                voice = get_voice(answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'who_are_you'):
                answer = answer_who_are_you[random.randint(0,(len(answer_status_good)-1))]
                voice = get_voice(answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'help'):
                bot.send_message(message.chat.id, help_text)
            else:
                answer = 'Извините, я вас не понимаю, но я учусь :3'
                voice = get_voice(answer)
                # bot.send_message(message.chat.id, answer)
                bot.send_voice(message.chat.id, voice)
        except:
            pass

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
    row = []
    i = 0
    for x in city_list_for_movie:
        i += 1
        if(i % 3 != 0):
            row.append(types.InlineKeyboardButton(x, callback_data="movie " + str(city_dict_names_as_key[x])))
        else:
            markup.row(*row)
            row = []
            row.append(types.InlineKeyboardButton(x, callback_data="movie " + str(city_dict_names_as_key[x])))
    if(len(row) != 0):
        markup.row(*row)
    
    return markup

def draw_movie_list(city_id):
    markup = types.InlineKeyboardMarkup()
    movie_list = get_movie_list(city_id)
    row = []
    i = 0
    for x in movie_list:
        i += 1
        if(i % 2 != 0):
            row.append(types.InlineKeyboardButton(text=x, callback_data="cinema " + str(get_movie_id(city_id, x))))
        else:
            markup.row(*row)
            row = []
            row.append(types.InlineKeyboardButton(text=x, callback_data="cinema " + str(get_movie_id(city_id, x))))
    if(len(row) != 0):
        markup.row(*row)
    markup.add(types.InlineKeyboardButton("Назад к выбору города", callback_data="back_to_city"))
    return markup

def draw_cinema_list(city_id):
    cinema_list = get_cinema_list(city_id)
    markup = types.InlineKeyboardMarkup()
    for x in cinema_list:
        markup.add(types.InlineKeyboardButton(text=x, callback_data="sessions " + str(get_cinema_id(city_id, x))))
    markup.add(types.InlineKeyboardButton("Назад к выбору фильма", callback_data="back_to_movie"))
    return markup

def draw_seesions_list(city_id, movie_id, cinema_id, cinema_name):
    markup = types.InlineKeyboardMarkup()
    sessions_list = get_session_list(city_id, movie_id, cinema_id)
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
        bot.send_message(chat_id, "Выберите город из списка ниже: ", reply_markup=markup)
    else:
        markup = draw_movie_list(city_id)
        bot.send_message(chat_id, "Какой фильм хотите посмотреть?", reply_markup=markup)
        user = User(chat_id)
        user.city_id = city_id
        user.cinema_name = city_dict_id_as_key[city_id]        
        user_dict[chat_id] = user
    
@bot.callback_query_handler(func=lambda call: True)
def message_query_handler(call):
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
                    user.movie_name = x
            user.movie_id = int(message)
            user_dict[chat_id] = user
        markup = draw_cinema_list(user.city_id)
        bot.edit_message_text(text='Выберите кинотеатр из списка ниже', chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=markup)
    if(message_type == 'sessions'):
        cinema_list = get_cinema_list(user.city_id)
        user.cinema_id = message
        for x in cinema_list:
            if(get_cinema_id(user.city_id, x) == int(message)):
                user.cinema_name = x
        markup = draw_seesions_list(user.city_id, user.movie_id, user.cinema_id, user.cinema_name)
        user_dict[chat_id] = user
        bot.edit_message_text(text= "  🎞 "+ movie_description(user.city_id, user.movie_id), chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=markup)
    if(message_type == 'ignore'):
        bot.answer_callback_query(call.id, text="")

def movie_start(message , text):
    chat_id = message.chat.id
    city_id = extract_city_id(text)
    user = User(chat_id)
    if(city_id == 0):
        markup = draw_city_list()
        bot.send_message(chat_id, "Выберите город из списка ниже: ", reply_markup=markup)
    else:
        markup = draw_movie_list(city_id)
        bot.send_message(chat_id, "Какой фильм хотите посмотреть?", reply_markup=markup)
        user = User(chat_id)
        user.city_id = city_id
        user.cinema_name = city_dict_id_as_key[city_id]        
        user_dict[chat_id] = user

if __name__ == '__main__':
    bot.polling(none_stop=True)