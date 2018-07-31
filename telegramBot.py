from weather_predict import *
import random
from classify import *
from translate import *
import telebot



token = '519406193:AAFBzLaoLqvt81lG1A6hpTWBoJQVCWrMo9M'
answer = ["Привет!", "Здравствуй", "Приветствую!", "Здравствуйте"]
answer_greetings_mood = ["Привет. Пойдет. Как у тебя?", "Здравствуй. Хорошо. Как у тебя?", "Приветствую. Нормально. Как у тебя?", "Здарова. Неплохо. Как у тебя?", "Здравствуйте. Все отлично. Как у вас?"]
answer_mood = ["Замечательно, спасибо!!", "Хорошо. Как у тебя дела?", "Все нормально. Как у вас?", "Все отлично. Как у тебя?", "Пойдет. А у тебя?"]
answer_philosophy = ['42']
answer_action = ['Разговариваю с тобой', 'Существую', 'Тихо жду здесь пока у меня что-то спросят']
answer_status_good = ['Рада слышать', 'Круто', 'Отлично!', 'Я очень рада :)']
command = '1'
bot = telebot.TeleBot(token)
@bot.message_handler(content_types=["text"])
def bot0(message):
    # while True:
        command = message.text
        # if command == '-1':
        #     break
        predicted_class = classify(command)
        if(predicted_class == 'weather'):
                get_weather(command)
                bot.send_message(message.chat.id, output)
        elif(predicted_class == 'greetings'):
                bot.send_message(message.chat.id, answer[random.randint(0,(len(answer)-1))])
        elif(predicted_class == 'greetings_mood'):
                bot.send_message(message.chat.id, answer_greetings_mood[random.randint(0,(len(answer_greetings_mood)-1))])
        elif(predicted_class == 'mood'):
                bot.send_message(message.chat.id, answer_mood[random.randint(0,(len(answer_mood)-1))])
        elif(predicted_class == 'philosophy'):
                bot.send_message(message.chat.id, answer_philosophy[0]) 
        elif(predicted_class == 'action'):
                bot.send_message(message.chat.id, answer_action[random.randint(0,(len(answer_action)-1))])
        elif(predicted_class == 'status_good'):
                bot.send_message(message.chat.id, answer_status_good[random.randint(0,(len(answer_status_good)-1))])
        # elif(predicted_class == 'translate'):
        #         bot.send_message(message.chat.id, print(translate(command)))
        else:
                bot.send_message(message.chat.id, 'Извините, я вас не понимаю, но я учусь :3')

if __name__ == '__main__':
    bot.polling(none_stop=True)

print('The bot has started')