from weather_predict import *
import random
from classify import *
from translate import *

answer = ["Привет!", "Здравствуй", "Приветствую!", "Здравствуйте"]
answer_greetings_mood = ["Привет. Пойдет. Как у тебя?", "Здравствуй. Хорошо. Как у тебя?", "Приветствую. Нормально. Как у тебя?", "Здарова. Неплохо. Как у тебя?", "Здравствуйте. Все отлично. Как у вас?"]
answer_mood = ["Замечательно, спасибо!!", "Хорошо. Как у тебя дела?", "Все нормально. Как у вас?", "Все отлично. Как у тебя?", "Пойдет. А у тебя?"]
answer_philosophy = ['42']
answer_action = ['Разговариваю с тобой', 'Существую', 'Тихо жду здесь пока у меня что-то спросят']
answer_status_good = ['Рада слышать', 'Круто', 'Отлично!', 'Я очень рада :)']
command = '1'

while True:
	command = input('Введите команду(-1 чтобы закончить разговор): ')
	if command == '-1':
		break
	predicted_class = classify(command)
	if(predicted_class == 'weather'):
		print(get_weather(command))
	elif(predicted_class == 'greetings'):
		print(answer[random.randint(0,(len(answer)-1))])
	elif(predicted_class == 'greetings_mood'):
		print(answer_greetings_mood[random.randint(0,(len(answer_greetings_mood)-1))])
	elif(predicted_class == 'mood'):
		print (answer_mood[random.randint(0,(len(answer_mood)-1))])
	elif(predicted_class == 'philosophy'):
		print(answer_philosophy[0])
	elif(predicted_class == 'action'):
		print (answer_action[random.randint(0,(len(answer_action)-1))])
	elif(predicted_class == 'status_good'):
		print (answer_status_good[random.randint(0,(len(answer_status_good)-1))])
	elif(predicted_class == 'translate'):
		print(translate(command))
	else:
		print('Извините, я вас не понимаю, но я учусь :3')
