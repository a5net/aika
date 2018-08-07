import urllib.request
import urllib.parse
import json
import re
from cachetools import cached, TTLCache
import nltk
from nltk.corpus import stopwords
from num2words import num2words
from transliterate import translit, get_available_language_codes


url_api = 'http://localhost:3000/api/v1/cities/'
def url_builder_geocoding(city):
    user_api = 'AIzaSyB43dwBw0qIRcKVoMvCYuCh4bHEZjS0bG0'
    full_api_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.parse.quote_plus(city) +'&language=ru&components=administrative_area:1&key=' + user_api
    return full_api_url

def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict

def extract_city_id(command):
    fname = 'regex_cinema.txt'
    out = []
    city = ''
    city_id = 0
    with open(fname, encoding='cp1251') as f:
        regex = f.readlines()
    regex = [line.rstrip('\n') for line in regex]
    match_list = []
    for i in regex:
        result = re.findall(i, command)
        if(result):
            match_list.append(result[0])
    match_list = [word for word in match_list if word.strip() not in stopwords.words('russian')]
    match_list = [x for x in match_list if x]
    for i in match_list:
        data = data_fetch(url_builder_geocoding(i))
        if(data.get('status') != 'ZERO_RESULTS'):
            print(data)
            out.append(data.get('results')[0].get('address_components')[0].get('long_name'))
    if(out):
        city = out[0]
    data = data_fetch(url_api)
    for i in data:
        if(i.get('name') == city):
            city_id = i.get('id')

    return city_id

def get_city_dict():
    city_list = dict()
    data = data_fetch(url_api)
    for i in data:
        city_list[i.get('name')] = i.get('id')
    return city_list

def get_cinema_list(city_id):
    url = url_api + str(city_id)
    data = data_fetch(url)
    cinema_list = []
    for i in data:
        cinema_list.append(i.get('name'))

    return cinema_list

def get_cinema_id(city_id, cinema_name):
    url = url_api + str(city_id)
    data = data_fetch(url)
    cinema_id = 0
    for i in data:
        if(i.get('name') == cinema_name):
            cinema_id = i.get('id')
            break

    return cinema_id

def get_movie_list(city_id):
    url = url_api + str(city_id) + '/movies'
    data = data_fetch(url)
    movie_list = []
    for i in data:
        if(i.get('title') not in movie_list):
            movie_list.append(i.get('title'))

    return movie_list

def get_movie_id(city_id, movie_name):
    url = url_api + str(city_id) + '/movies'
    data = data_fetch(url)
    movie_id = 0
    for i in data:
        if(i.get('title') == movie_name):
            movie_id = i.get('id')
            break
    
    return movie_id

def get_session_list(city_id, movie_id, cinema_id):
    url = url_api + str(city_id) + '/movies/'+ str(movie_id) + '/cinemas/' + str(cinema_id)
    data = data_fetch(url)
    sessions_list = []
    for i in data:
        sessions_list.append(i.get('time'))

    return sessions_list


# def get_ticketon_url(movie_name_russian, session):
#     movie_name_russian = movie_name_russian.split()
#     for i in range(len(movie_name_russian)):
#         if movie_name_russian[i].isdigit():
#             movie_name_russian[i] = num2words(movie_name_russian[i], lang='ru')
#     movie_name_without_numbers = " ".join(movie_name_russian)
#     movie_name_translit = [translit(a, 'ru', reversed=True).strip("'") for a in movie_name_without_numbers.split()]
#     movie_name_translit = "-".join(movie_name_translit)
#     full_url = "https://m.ticketon.kz/event/" + movie_name_translit
#     url = urllib.request.urlopen(full_url)
#     output = url.read().decode('utf-8')

def get_ticket_url(cinema_name, city_id):
    kinopark = {
        'Kinopark 11 (Есентай) IMAX' : 1,
        'Kinopark 6 (Спутник)' : 5,
        'Kinopark 8 Moskva' : 8,
        'Kinopark 7 IMAX Keruen' : 9,
        'Kinopark 8 IMAX Saryarka' : 7,
        'Kinopark 6 Keruencity Astana' : 4,
        'Kinopark 5 Mega Planet Shymkent' : 3,
        'Kinopark 7 Keruencity Aktobe' : 6
        }
    url = ""
    cinema_name_list = cinema_name.split()
    cinema_name_list = [a.lower() for a in cinema_name_list]
    if('kinopark' in cinema_name_list):
        url = 'http://kinopark.kz/ru/shedule?interval=today&cinema=' + kinopark[cinema_name]
    else:
        url = 'http://localhost:3000/api/v1/cities/' + str(city_id)
        data = data_fetch(url)
        for i in data:
            if(i.get('name') == cinema_name):
                cite_id = i.get('cite_index')
                url = 'http://kino.kz/cinema.asp?cinemaid=' + str(cite_id)

    return url

def movie_description(city_id, movie_id):
    url = url_api + str(city_id) + '/movies'
    data = data_fetch(url)
    movie_description = 0
    for i in data:
        if(i.get('id') == movie_id):
            movie_description = i.get('description')
            break
    
    return movie_description