import pandas as pd
import datetime
import urllib.request
import json
from googletrans import Translator
from nltk.stem.snowball import RussianStemmer
import re
from cachetools import cached, TTLCache

stemmer = RussianStemmer()
cache = TTLCache(maxsize=500, ttl=1800)

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time

def url_builder(city_name, state):
    user_api = '89f22ce44fe09b07e925aa6420546626'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/' + state + '?q='     # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz

    full_api_url = api + city_name + '&mode=json&units=' + unit +'&lang=ru&APPID=' + user_api
    return full_api_url

@cached(cache)
def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict

def data_organizer_forecast(raw_api_dict):
    data = dict(
        city = raw_api_dict.get('city').get('name'),
        country = raw_api_dict.get('city').get('country'),
        day_0 = dict(
            morning_temp = raw_api_dict.get('list')[0].get('main').get('temp'),
            afternoon_temp = raw_api_dict.get('list')[1].get('main').get('temp'),
            evening_temp = raw_api_dict.get('list')[3].get('main').get('temp'),
            morning_weather = raw_api_dict.get('list')[0].get('weather')[0].get('description'),
            afternoon_weather = raw_api_dict.get('list')[1].get('weather')[0].get('description'),
            evening_weather = raw_api_dict.get('list')[3].get('weather')[0].get('description'),
            morning_windspeed = raw_api_dict.get('list')[0].get('wind').get('speed'),
            afternoon_windspeed = raw_api_dict.get('list')[1].get('wind').get('speed'),
            evening_windspeed = raw_api_dict.get('list')[3].get('wind').get('speed'),
            morning_humidity = raw_api_dict.get('list')[0].get('main').get('humidity'),
            afternoon_humidity = raw_api_dict.get('list')[1].get('main').get('humidity'),
            evening_humidity = raw_api_dict.get('list')[3].get('main').get('humidity'),
            ),
        day_1 = dict(
            night_temp = raw_api_dict.get('list')[5].get('main').get('temp'),
            morning_temp = raw_api_dict.get('list')[8].get('main').get('temp'),
            afternoon_temp = raw_api_dict.get('list')[9].get('main').get('temp'),
            evening_temp = raw_api_dict.get('list')[11].get('main').get('temp'),
            night_weather = raw_api_dict.get('list')[5].get('weather')[0].get('description'),
            morning_weather = raw_api_dict.get('list')[8].get('weather')[0].get('description'),
            afternoon_weather = raw_api_dict.get('list')[9].get('weather')[0].get('description'),
            evening_weather = raw_api_dict.get('list')[11].get('weather')[0].get('description'),
            night_windspeed = raw_api_dict.get('list')[5].get('wind').get('speed'),
            morning_windspeed = raw_api_dict.get('list')[8].get('wind').get('speed'),
            afternoon_windspeed = raw_api_dict.get('list')[9].get('wind').get('speed'),
            evening_windspeed = raw_api_dict.get('list')[11].get('wind').get('speed'),
            night_humidity = raw_api_dict.get('list')[5].get('main').get('humidity'),
            morning_humidity = raw_api_dict.get('list')[8].get('main').get('humidity'),
            afternoon_humidity = raw_api_dict.get('list')[9].get('main').get('humidity'),
            evening_humidity = raw_api_dict.get('list')[11].get('main').get('humidity'),
            ),
        day_2 = dict(
            night_temp = raw_api_dict.get('list')[13].get('main').get('temp'),
            morning_temp = raw_api_dict.get('list')[16].get('main').get('temp'),
            afternoon_temp = raw_api_dict.get('list')[17].get('main').get('temp'),
            evening_temp = raw_api_dict.get('list')[19].get('main').get('temp'),
            night_weather = raw_api_dict.get('list')[13].get('weather')[0].get('description'),
            morning_weather = raw_api_dict.get('list')[16].get('weather')[0].get('description'),
            afternoon_weather = raw_api_dict.get('list')[17].get('weather')[0].get('description'),
            evening_weather = raw_api_dict.get('list')[19].get('weather')[0].get('description'),
            night_windspeed = raw_api_dict.get('list')[13].get('wind').get('speed'),
            morning_windspeed = raw_api_dict.get('list')[16].get('wind').get('speed'),
            afternoon_windspeed = raw_api_dict.get('list')[17].get('wind').get('speed'),
            evening_windspeed = raw_api_dict.get('list')[19].get('wind').get('speed'),
            night_humidity = raw_api_dict.get('list')[13].get('main').get('humidity'),
            morning_humidity = raw_api_dict.get('list')[16].get('main').get('humidity'),
            afternoon_humidity = raw_api_dict.get('list')[17].get('main').get('humidity'),
            evening_humidity = raw_api_dict.get('list')[19].get('main').get('humidity'),
            ),
        day_3 = dict(
            night_temp = raw_api_dict.get('list')[21].get('main').get('temp'),
            morning_temp = raw_api_dict.get('list')[24].get('main').get('temp'),
            afternoon_temp = raw_api_dict.get('list')[25].get('main').get('temp'),
            evening_temp = raw_api_dict.get('list')[27].get('main').get('temp'),
            night_weather = raw_api_dict.get('list')[21].get('weather')[0].get('description'),
            morning_weather = raw_api_dict.get('list')[24].get('weather')[0].get('description'),
            afternoon_weather = raw_api_dict.get('list')[25].get('weather')[0].get('description'),
            evening_weather = raw_api_dict.get('list')[27].get('weather')[0].get('description'),
            night_windspeed = raw_api_dict.get('list')[21].get('wind').get('speed'),
            morning_windspeed = raw_api_dict.get('list')[24].get('wind').get('speed'),
            afternoon_windspeed = raw_api_dict.get('list')[25].get('wind').get('speed'),
            evening_windspeed = raw_api_dict.get('list')[27].get('wind').get('speed'),
            night_humidity = raw_api_dict.get('list')[21].get('main').get('humidity'),
            morning_humidity = raw_api_dict.get('list')[24].get('main').get('humidity'),
            afternoon_humidity = raw_api_dict.get('list')[25].get('main').get('humidity'),
            evening_humidity = raw_api_dict.get('list')[27].get('main').get('humidity'),
            ),
        day_4 = dict(
            night_temp = raw_api_dict.get('list')[29].get('main').get('temp'),
            morning_temp = raw_api_dict.get('list')[32].get('main').get('temp'),
            afternoon_temp = raw_api_dict.get('list')[33].get('main').get('temp'),
            evening_temp = raw_api_dict.get('list')[35].get('main').get('temp'),
            night_weather = raw_api_dict.get('list')[29].get('weather')[0].get('description'),
            morning_weather = raw_api_dict.get('list')[32].get('weather')[0].get('description'),
            afternoon_weather = raw_api_dict.get('list')[33].get('weather')[0].get('description'),
            evening_weather = raw_api_dict.get('list')[35].get('weather')[0].get('description'),
            night_windspeed = raw_api_dict.get('list')[29].get('wind').get('speed'),
            morning_windspeed = raw_api_dict.get('list')[32].get('wind').get('speed'),
            afternoon_windspeed = raw_api_dict.get('list')[33].get('wind').get('speed'),
            evening_windspeed = raw_api_dict.get('list')[35].get('wind').get('speed'),
            night_humidity = raw_api_dict.get('list')[29].get('main').get('humidity'),
            morning_humidity = raw_api_dict.get('list')[32].get('main').get('humidity'),
            afternoon_humidity = raw_api_dict.get('list')[33].get('main').get('humidity'),
            evening_humidity = raw_api_dict.get('list')[35].get('main').get('humidity'),
            )
        )
    return data

def data_organizer_current(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        humidity=raw_api_dict.get('main').get('humidity'),
        weather=raw_api_dict['weather'][0]['description'],
        wind=raw_api_dict.get('wind').get('speed'),
        dt=time_converter(raw_api_dict.get('dt'))
    )
    return data

def extract_feature_list(command):
    features = []
    feature_list = ['погода','температура','влажность','скорость']
    command = re.sub(r'[^\w\s]', ' ', command)
    word_list = command.split()
    word_list = [stemmer.stem(a).lower() for a in word_list]
    for i in feature_list:
        if stemmer.stem(i) in word_list:
            features.append(i)
    return features

def extract_city(command):
    city_frame = pd.read_csv("city.csv", encoding='cp1251')
    city_list = city_frame["name"].tolist()
    city_dict = dict()
    for i in city_list:
        city_dict[stemmer.stem(i).lower()] = i
    city_dict['астан'] = 'Астана'
    city_name = ""
    print('на' in city_dict.keys())
    command = re.sub(r'[^\w\s]', ' ', command)
    word_list = command.split()
    word_list = [stemmer.stem(a).lower() for a in word_list]
    for word in word_list:
        if(word in city_dict.keys()):
            translator = Translator()
            city_name = translator.translate(city_dict[word]).text
    return city_name

def extract_date_and_time(command):
    time_of_the_day = ''
    days_ahead = ''
    command = re.sub(r'[^\w\s]', ' ', command)
    word_list = command.split()
    word_list = [stemmer.stem(a).lower() for a in word_list]
    day_of_the_week = dict(
        понедельник = 0,
        вторник = 1,
        среда = 2,
        четверг = 3,
        пятница = 4,
        суббота = 5,
        воскресенье = 6
        )
    nearest_days = dict(
        сегодня = 0,
        завтра = 1,
        послезавтра = 2
        )
    daytime = dict(
        днем = 2,
        дня = 2,
        полдень = 2,
        полночь = 0,
        ночь = 0,
        утро = 1,
        обед = 2,
        вечер = 3
        )
    
    date_words_before = ['на','за']
    date_words_after = ['число']
    for word in date_words_before:
        try:    
            if(stemmer.stem(word).lower() in word_list):
                current_day = datetime.date.today().timetuple().tm_mday
                days_ahead = int(word_list[word_list.index(stemmer.stem(word).lower()) + 1]) - current_day
                if(days_ahead > 4):
                    inp = input("У нас имеется прогноз погоды на ближайшие 4 дня, введите другую дату: ")
                    days_ahead = int(inp) - current_day
        except:
            pass

    for word in date_words_after:
        try:
            if(stemmer.stem(word).lower() in word_list):
                current_day = datetime.date.today().timetuple().tm_mday
                days_ahead = int(word_list[word_list.index(stemmer.stem(word).lower()) - 1]) - current_day
                if(days_ahead > 4):
                    inp = input("У нас имеется прогноз погоды на ближайшие 4 дня, введите другую дату: ")
                    days_ahead = int(inp) - current_day
        except:
            pass

    for weekday in day_of_the_week:
        if(stemmer.stem(weekday).lower() in word_list):
            current_day_of_the_week = datetime.datetime.today().weekday()
            difference = day_of_the_week[weekday] - current_day_of_the_week
            if(difference >= 0):
                days_ahead = difference
            else:
                days_ahead = 7 + difference
            if(days_ahead > 4):
                inp = input("У нас имеется погода на ближайшие 4 дня, введите другой день недели: ")
                difference = day_of_the_week[inp] - current_day_of_the_week
                if(difference >= 0):
                    days_ahead = difference
                else:
                    days_ahead = 7 + difference

    for nearday in nearest_days:
        if(stemmer.stem(nearday).lower() in word_list):
            days_ahead = nearest_days[nearday]

    for day_hour in daytime:
        if(stemmer.stem(day_hour) in word_list):
            time_of_the_day = daytime[day_hour]        

    return_array = [days_ahead, time_of_the_day]
    return return_array

def get_weather(command):
    days_ahead = 0
    time_of_the_day = 2
    m_symbol = '\xb0' + 'C'
    translator = Translator()
    feature_list = extract_feature_list(command)
    city = extract_city(command)
    if not city:
            city = input("Введите название города: ")
            city = translator.translate(city).text
    date_and_time_array = extract_date_and_time(command)
    # try:
    if((not date_and_time_array[0]) and (not date_and_time_array[1])):
        data = data_organizer_current(data_fetch(url_builder(city, 'weather')))
        if('погода' in feature_list or not feature_list):
            print('Погода в: {}, {}:'.format(data['city'], data['country']))
            print(data['temp'], m_symbol, data['weather'])
            print('Влажность воздуха: {} %'.format(data['humidity']))
            print('Скорость ветра: {} м/сек'.format(data['wind']))
            print('-----------------------------------------------')
            print('Последние обновления были получены с сервера: {}'.format(data['dt']))
        elif('температура' in feature_list):
            print('Температура воздуха: {}'.format(data['temp']), m_symbol)
        elif('влажность' in feature_list):
            print('Влажность воздуха: {} %'.format(data['humidity']))
        elif('скорость' in feature_list):
            print('Скорость ветра: {} м/сек'.format(data['wind']))
    else:
        data = data_organizer_forecast(data_fetch(url_builder(city, 'forecast')))
        if date_and_time_array[0]:
            days_ahead = date_and_time_array[0]
        if date_and_time_array[1]:
            time_of_the_day = date_and_time_array[1]
        day_dict = 'day_' + str(days_ahead)
        time_of_the_day_array = ['night', 'morning', 'afternoon', 'evening']

        if('погода' in feature_list or not feature_list):
            print('Погода в: {}, {}:'.format(data['city'], data['country']))
            print(data[day_dict][time_of_the_day_array[time_of_the_day] + '_temp'], m_symbol, data[day_dict][time_of_the_day_array[time_of_the_day] + '_weather'])
            print('Влажность воздуха: {} %'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_humidity']))
            print('Скорость ветра: {} м/сек'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_windspeed']))
        elif('температура' in feature_list):
            print('Температура воздуха: {}'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_temp']), m_symbol)
        elif('влажность' in feature_list):
            print('Влажность воздуха: {} %'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_humidity']))
        elif('скорость' in feature_list):
            print('Скорость ветра: {} м/сек'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_windspeed']))
    # except:
    #     print('В работе программы возникли неполадки, введите запрос еще раз.')