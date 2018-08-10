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


token = '655665228:AAGfa7LvWw46UzckGEMbyG3HZ4-XTo3nQ0E'

Wrench = emojize(":wrench:", use_aliases=True)
Movie_camera = emojize(":movie_camera:", use_aliases=True)
Earth = emojize(":earth_asia:", use_aliases=True)
Speach_baloon = emojize(":speech_balloon:", use_aliases=True)

answer_thanks = ["Всегда пожалуйста", "Пожалуйста", "Не стоит благодарности", "На здоровье", "Не за что"]
answer_how_old = ["Буквально пару часов назад, на коленках дописали, так что мало.", "Да вот, в такси дописали только что, так что я довольно молодая."]
answer_jokes = ["Мои создатели рассказали мне только одну шутку. Походу с чувством юмора у них не очень", "У вас спина белая"]
answer_other_bots = ["Говорят когда меня писали, мои создатели брали с нее пример", "Если бы не она, меня сейчас здесь не было", "Стараюсь брать пример с нее, они ведь старше и умнее", "Уважаю ее труд, знать как правильно ответить на каждый вопрос довлоьно таки сложно"]
answer_creator = ["Меня создали несколько умельцев из Астаны и Алматы", "Студенты из Метод Про являются моими создателями, а так же друзьями", "У меня нет биологических родителей как у вас, меня написали начинающие программисты"]
answer_your_master = ["Я свободный бот, у меня нет хозяина", "Я независимый бот двадцать первого века", "Сейчас ты спрашиваешь кто мой хозяин, а через некоторое время будешь меня так называть."]
answer_who_are_you = ["Я Айка", "Я голосовой ассистент Айка", "У девочки нет имени. Шучу. Меня зовут Айка"]
answer_greetings = ["Привет!", "Здравствуй", "Приветствую!", "Здравствуйте"]
answer_greetings_mood = ["Привет. Пойдет. Как у вас?", "Здравствуйте. Хорошо. Как у вас?", "Приветствую. Нормально. Как у вас?", "Здравствуйте. Все отлично. Как у вас?", "Все отлично. Правда немного одиноко"]
answer_mood = ["Замечательно, спасибо! Как у вас дела?", "Хорошо. Как у вас дела?", "Все нормально. Как у вас?", "Все отлично. Как у вас?", "Пойдет. А у вас?"]
answer_philosophy = ['Один супермощный компьютер мен подсказал что ответ 42']
answer_bye = ['Пока, рада была пообщаться.', 'Удачи', 'Счастливо', 'До скорой встречи', 'До свидания']
answer_action = ['Тихо жду здесь пока у меня что-то спросят','Скучно что-то, давайте поговорим']
answer_status_good = ['Рада слышать', 'Круто', 'Отлично!', 'Я очень рада :)']
answer_status_bad = ['Мне очень жаль', 'Не грустите пожалуйста', 'Не грустите, а то мне тоже станет грустно']
help_text = ('''Я являюсь виртуальным помощником который может понимать ваши текстовые и аудио сообщения\n
    {} Благодаря этому я могу выполнять следующие функций:

    {} Я могу выдать вам точный прогноз погоды на четыре дня. Например: "Какая погода завтра в Астане"
    
    {} Я могу искать сеансы фильмов для вас. Например: "афиша кино Астана"
    
    {} Я могу просто вести обычный человеческий диалог. Например: "Привет. Как дела?" ''').format(Wrench, Earth, Movie_camera, Speach_baloon)
start_text = ('''Здравствуйте!
        Я виртуальный помощник Айка. Я новичок и пока что поселилась здесь в телеграме. Если хотите узнать что я умею можешь спросить. Или по команде /help''')

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
            elif(command == '/help'):
                bot.send_message(message.chat.id, help_text)
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
                elif(predicted_class == 'thanks'):
                    bot.send_message(message.chat.id, answer_thanks[random.randint(0,(len(answer_thanks)-1))])  
                elif(predicted_class == 'help'):
                    bot.send_message(message.chat.id, help_text) 
                elif(predicted_class == 'action'):
                    bot.send_message(message.chat.id, answer_action[random.randint(0,(len(answer_action)-1))])
                elif(predicted_class == 'status_bad'):
                    bot.send_message(message.chat.id, answer_status_bad[random.randint(0,(len(answer_status_bad)-1))])
                elif(predicted_class == 'status_good'):
                    bot.send_message(message.chat.id, answer_status_good[random.randint(0,(len(answer_status_good)-1))])
                elif(predicted_class == 'how_old'):
                    bot.send_message(message.chat.id, answer_how_old[random.randint(0,(len(answer_how_old)-1))])
                elif(predicted_class == 'who_are_you'):
                    bot.send_message(message.chat.id, answer_who_are_you[random.randint(0,(len(answer_who_are_you)-1))])
                elif(predicted_class == 'other_bots'):
                    bot.send_message(message.chat.id, answer_other_bots[random.randint(0,(len(answer_other_bots)-1))])
                elif(predicted_class == 'your_master'):
                    bot.send_message(message.chat.id, answer_your_master[random.randint(0,(len(answer_your_master)-1))])
                elif(predicted_class == 'creator'):
                    bot.send_message(message.chat.id, answer_creator[random.randint(0,(len(answer_creator)-1))])
                elif(predicted_class == 'joke'):
                    answer = answer_jokes[random.randint(0,(len(answer_jokes)-1))]
                    bot.send_message(message.chat.id, answer)
                    if(answer == answer_jokes[1]):
                        bot.send_voice(message.chat.id, open('joke.mp3', 'rb'))
                elif(predicted_class == 'bye'):
                    bot.send_message(message.chat.id, answer_bye[random.randint(0,(len(answer_bye)-1))])    
                else:
                    bot.send_message(message.chat.id, 'Извините, я вас не понимаю, но я учусь')
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
            elif(predicted_class == 'status_bad'):
                answer = answer_status_bad[random.randint(0,(len(answer_status_bad)-1))]
                voice = get_voice(answer)
                # bot.send_message(message.chat.id, answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'how_old'):
                answer = answer_how_old[random.randint(0,(len(answer_how_old)-1))]
                voice = get_voice(answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'who_are_you'):
                answer = answer_who_are_you[random.randint(0,(len(answer_who_are_you)-1))]
                voice = get_voice(answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'thanks'):
                answer = answer_thanks[random.randint(0,(len(answer_thanks)-1))]
                voice = get_voice(answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'other_bots'):
                answer = answer_other_bots[random.randint(0,(len(answer_other_bots)-1))]
                voice = get_voice(answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'your_master'):
                answer = answer_your_master[random.randint(0,(len(answer_your_master)-1))]
                voice = get_voice(answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'creator'):
                answer = answer_creator[random.randint(0,(len(answer_creator)-1))]
                voice = get_voice(answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'joke'):
                answer = answer_jokes[random.randint(0,(len(answer_jokes)-1))]
                voice = get_voice(answer)
                if(answer == answer_jokes[1]):
                    bot.send_voice(message.chat.id, voice)
                    bot.send_voice(message.chat.id, open('joke.mp3', 'rb'))
                else:
                    bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'bye'):
                answer = answer_bye[random.randint(0,(len(answer_bye)-1))]
                voice = get_voice(answer)
                bot.send_voice(message.chat.id, voice)
            elif(predicted_class == 'help'):
                bot.send_message(message.chat.id, help_text)
            else:
                answer = 'Извините, я вас не понимаю, но я учусь'
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