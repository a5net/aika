from weather_predict import *
import random
from classify import *

answer = ["Привет!", "Здравствуй", "Приветствую!", "Здарова", "Здравствуйте"]
answer_greetings_mood = ["Привет. Пойдет. Как у тебя?", "Здравствуй. Хорошо. Как у тебя?", "Приветствую. Нормально. Как у тебя?", "Здарова. Неплохо. Как у тебя?", "Здравствуйте. Все отлично. Как у вас?"]
answer_mood = ["Замечательно, спасибо!!", "Хорошо как у тебя дела?", "Все нормально как у вас?", "Все отлично как у тебя?", "Пойдет а у тебя?"]
answer_philosophy = ['42']

command = '1'

while command != '-1':
	command = input('Введите команду: ')
	predicted_class = classify(command)
	if(predicted_class == 'weather'):
		get_weather(command)
	elif(predicted_class == 'greetings'):
		print(answer[random.randint(0,(len(answer)-1))])
	elif(predicted_class == 'greetings_mood'):
		print(answer_greetings_mood[random.randint(0,(len(answer_greetings_mood)-1))])
	elif(predicted_class == 'mood'):
		print (answer_mood[random.randint(0,(len(answer_mood)-1))])
	elif(predicted_class == 'philosophy'):
		print(answer_philosophy[0])
	else:
		print('Извините, я вас не понимаю, но я учусь :3')