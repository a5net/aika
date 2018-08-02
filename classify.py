import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json
import re
import os
from pathlib import Path

#print(os.listdir("../input"))

import nltk
nltk.download('punkt')
from nltk.stem.snowball import RussianStemmer


stemmer = RussianStemmer()


def get_class_examples(name):
    train = pd.read_json("input/" + name + '.json', orient = 'columns')
    return train.to_dict('records')

def get_class_name_list():
    path = "input"
    list_names = os.listdir(path)
    res = []
    for i in range(0, len(list_names)):
        candidate = Path(list_names[i]).suffix
        if(candidate == ".json"):
            res.append(list_names[i].replace('.json', ''))
    return set(res)
    
class_name_list = get_class_name_list()

def get_all_class():
    train_data = []
    for x in class_name_list:
        train_data += get_class_examples(x) 
    return train_data



def get_city_names():
    city_frame = pd.read_csv("city.csv", encoding='cp1251')
    city_list = city_frame["name"].tolist()
    res = {''}
    for j in city_list:
        #if j != "Дели":
        res.add(stemmer.stem(j).lower())
        
    return res


def get_stopwords():
#     from nltk.corpus import stopwords
#     stop_words_list = stopwords.words('russian')
    stop_words = get_city_names()

    
    #stop_words.add('как')
    stop_words.add('в')
    return stop_words

    
def get_length(text, stop_words):
    count = 0
    for i in text:
            count += 1
    return count

def get_average_of_class(class_name, stop_words):
    data = get_class_examples(class_name)
    size = len(data)
    count = 0
    for i in range(0, size):
        count += get_length(data[i]['text'].split(), stop_words)
    return count / size


corpus_words = {}
class_words = {}
training_data = get_all_class()
classes = list(set([a['class'] for a in training_data]))

stop_words = get_stopwords()
city_names = get_city_names()
for c in classes:
    class_words[c] = []

for data in training_data:
    for word in nltk.word_tokenize(data['text']):
        if word not in ["?", "!"]:
            stemmed_word = stemmer.stem(word.lower())
            if stemmed_word not in stop_words:
                if stemmed_word not in corpus_words:
                    corpus_words[stemmed_word] = 1
                else:
                    corpus_words[stemmed_word] += 1

                class_words[data['class']].extend([stemmed_word])



def calculate_class_score(text, class_name):
    count = 0
    for word in nltk.word_tokenize(text):
        if stemmer.stem(word.lower()) in class_words[class_name]:
            count += (1 / corpus_words[stemmer.stem(word.lower())])
    return count


def cleaner(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    temp = ""
    arr = text.split()
    for i in arr:
        i = stemmer.stem(i).lower()
        if i  not in stop_words:
            temp += i + " "
    return temp



def classify(sentence):
    sentence = cleaner(sentence)
    high_class = None
    high_score = 0
    average = get_length(sentence.split(), city_names)
    high_average = 0    
    for c in class_words.keys():
        score = calculate_class_score(sentence, c)
        if score > high_score and score != 0:
            high_class = c
            high_score = score
            high_average = get_average_of_class(c, city_names)
        elif score == high_score and score != 0:
            new_class_average = get_average_of_class(c, city_names)
            related_to_origin_class = (average - high_average) * (average - high_average)
            related_to_new_class = (average - new_class_average) * (average - new_class_average)
            if related_to_new_class < related_to_origin_class:
                high_class = c
                high_score = score
                high_average = related_to_new_class            
    if(high_class == None): high_class = "unknown_command"
    return high_class
 