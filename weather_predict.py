import pandas as pd
import datetime
import urllib.request
import urllib.parse
import json
from googletrans import Translator
from nltk.stem.snowball import RussianStemmer
import re
from cachetools import cached, TTLCache
import calendar
from nltk.corpus import stopwords
import emoji

stemmer = RussianStemmer()
cache = TTLCache(maxsize=500, ttl=1800)

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time

def url_builder_geocoding(city):
    user_api = 'AIzaSyB43dwBw0qIRcKVoMvCYuCh4bHEZjS0bG0'
    full_api_url = 'https://maps.googleapis.com/maps/api/geocode/json?&address=' + urllib.parse.quote_plus(city) +'&components=administrative_area:1&key=' + user_api
    return full_api_url

def url_builder(city_name, state):
    user_api = '89f22ce44fe09b07e925aa6420546626'
    unit = 'metric'
    api = 'http://api.openweathermap.org/data/2.5/' + state + '?q='
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
            evening_humidity = raw_api_dict.get('list')[27].get('main').get('humidity')
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
            evening_humidity = raw_api_dict.get('list')[35].get('main').get('humidity')
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

def replace_dates(command):
    dates = {
        'первое' : 1,
        'второе' : 2,
        'третье' : 3,
        'четвертое' : 4,
        'пятое' : 5,
        'шестое' : 6,
        'седьмое' : 7,
        'восьмое' : 8,
        'девятое' : 9,
        'десятое' : 10,
        'одиннадцатое' : 11,
        'двеннадцатое' : 12,
        'тринадцатое' : 13,
        'четырнадцатое' : 14,
        'пятнадцатое' : 15,
        'шестнадцатое' : 16,
        'семнадцатое' : 17,
        'восемнадцатое' : 18,
        'девятнадцатое' : 19,
        'двадцатое' : 20,
        'двадцать первое' : 21,
        'двадцать второе' : 22,
        'двадцать третье' : 23,
        'двадцать четвертое' : 24,
        'двадцать пятое' : 25,
        'двадцать шестое' : 26,
        'двадцать седьмое' : 27,
        'двадцать восьмое' : 28,
        'двадцать девятое' : 29,
        'тридцатое' : 30,
        'тридцать первое' : 31
        }

    word_list = command.split()
    word_list = [stemmer.stem(a).lower() for a in word_list]
    for i in dates:
        if(stemmer.stem(i) in word_list):
            command = re.sub(i, str(dates[i]), command)
    return command

def extract_feature_list(command):
    features = []
    feature_list = ['погода','температура','влажность','скорость','ветер']
    command = re.sub(r'[^\w\s]', ' ', command)
    word_list = command.split()
    word_list = [stemmer.stem(a).lower() for a in word_list]
    for i in feature_list:
        if stemmer.stem(i) in word_list:
            features.append(i)
    return features

def extract_city(command):
    fname = 'regex.txt'
    out = []
    city = ''
    with open(fname, encoding='cp1251') as f:
        regex = f.readlines()
    regex = [line.rstrip('\n') for line in regex]
    match_list = []
    for i in regex:
        result = re.findall(i, command)
        if(result):
            match_list.append(result[0])
    match_list = [word for word in match_list if word.strip() not in stopwords.words('russian')]
    for i in match_list:
        data = data_fetch(url_builder_geocoding(i))
        if(data.get('status') != 'ZERO_RESULTS'):
            out.append(data.get('results')[0].get('address_components')[0].get('long_name'))
    if(out):
        city = out[0]
    return city

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
                forecast_day = int(word_list[word_list.index(stemmer.stem(word).lower()) + 1])
                if(forecast_day > current_day):
                    days_ahead = forecast_day - current_day
                else:
                    number_of_days = int(calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])
                    days_ahead = (number_of_days - current_day) + forecast_day
        except:
            pass

    for word in date_words_after:
        try:    
            if(stemmer.stem(word).lower() in word_list):
                current_day = datetime.date.today().timetuple().tm_mday
                forecast_day = int(word_list[word_list.index(stemmer.stem(word).lower()) - 1])
                if(forecast_day > current_day):
                    days_ahead = forecast_day - current_day
                else:
                    number_of_days = int(calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])
                    days_ahead = (number_of_days - current_day) + forecast_day
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

    for nearday in nearest_days:
        if(stemmer.stem(nearday).lower() in word_list):
            days_ahead = nearest_days[nearday]

    for day_hour in daytime:
        if(stemmer.stem(day_hour) in word_list):
            time_of_the_day = daytime[day_hour]        

    return_array = [days_ahead, time_of_the_day]
    return return_array

def get_weather(command):
    command = replace_dates(command)
    output = ''
    speech = ''
    days_ahead = 0
    time_of_the_day = 2
    m_symbol = '\xb0' + 'C'
    translator = Translator()
    feature_list = extract_feature_list(command)
    city = extract_city(command)
    if(city == ''):
        return('Не указано название города')
    date_and_time_array = extract_date_and_time(command)
    try:
        if((not date_and_time_array[0]) and (not date_and_time_array[1])):
            data = data_organizer_current(data_fetch(url_builder(city, 'weather')))
            if('погода' in feature_list or not feature_list):
                output = output + ':earth_asia: Погода в: {}, {}: \n'.format(data['city'], data['country'])
                output = output + str(':thermometer: ' + data['temp']) + m_symbol + ' ' + data['weather'] + '\n'
                output = output + 'Влажность воздуха: {} %\n'.format(data['humidity']) 
                output = output + ':fog: Скорость ветра: {} м/сек\n'.format(data['wind'])
                output = output + '-----------------------------------------------\n'
                output = output + 'Последние обновления были получены с сервера: {}\n'.format(data['dt'])
                speech = 'В городе {} {}, {} градусов по цельсию'.format(city, data['weather'], str(int(data['temp']))) 
                return output, speech
            elif('температура' in feature_list):
                output = output + ':thermometer: Температура воздуха: {}'.format(data['temp']) + m_symbol
                speech = 'Температура воздуха в городе {} {} градусов по цельсию'.format(city, int(data['temp']))
                return output, speech
            elif('влажность' in feature_list):
                output = output + 'Влажность воздуха: {} %'.format(data['humidity'])
                speech = 'Влажность водуха в городе {} {} процентов'.format(city, int(data['humidity']))
                return output, speech
            elif('скорость' in feature_list or 'ветер' in feature_list):
                output = output + ':fog: Скорость ветра: {} м/сек'.format(data['wind'])
                speech = 'Скорость ветра в городе {} {} метров в секунду'.format(city, data['wind'])
                return output, speech
        else:
            data = data_organizer_forecast(data_fetch(url_builder(city, 'forecast')))
            if date_and_time_array[0]:
                days_ahead = date_and_time_array[0]
                if(days_ahead > 4):
                    return('У нас имеется прогноз погоды на ближайшие четыре дня')
            if date_and_time_array[1]:
                time_of_the_day = date_and_time_array[1]
            day_dict = 'day_' + str(days_ahead)
            time_of_the_day_array = ['night', 'morning', 'afternoon', 'evening']

            if('погода' in feature_list or not feature_list):
                output = output + ':earth_asia: Погода в: {}, {}:\n'.format(data['city'], data['country'])
                output = output + str(':thermometer: ' + data[day_dict][time_of_the_day_array[time_of_the_day] + '_temp']) + m_symbol + ' ' + data[day_dict][time_of_the_day_array[time_of_the_day] + '_weather'] + '\n'
                output = output + 'Влажность воздуха: {} %\n'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_humidity'])
                output = output + ':fog: Скорость ветра: {} м/сек'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_windspeed'])
                speech = 'В городе {} {}, {} градусов по цельсию'.format(city, data[day_dict][time_of_the_day_array[time_of_the_day] + '_weather'], str(int(data[day_dict][time_of_the_day_array[time_of_the_day] + '_temp'])))
                return output, speech
            elif('температура' in feature_list):
                output = output + ':thermometer: Температура воздуха: {}'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_temp']) + m_symbol
                speech = 'Температура воздуха в городе {} {} градусов по цельсию'.format(city, str(int(data[day_dict][time_of_the_day_array[time_of_the_day] + '_temp'])))
                return output, speech
            elif('влажность' in feature_list):
                output = output + 'Влажность воздуха: {} %'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_humidity'])
                speech = 'Влажность водуха в городе {} {} процентов'.format(city, int(data[day_dict][time_of_the_day_array[time_of_the_day] + '_humidity']))
                return output, speech
            elif('скорость' in feature_list or 'ветер' in feature_list):
                output = output + ':fog: Скорость ветра: {} м/сек'.format(data[day_dict][time_of_the_day_array[time_of_the_day] + '_windspeed'])
                speech = 'Скорость ветра в городе {} {} метров в секунду'.format(city, data[day_dict][time_of_the_day_array[time_of_the_day] + '_windspeed'])
                return output, speech
    except:
        print('В работе программы возникли неполадки, введите запрос еще раз.')