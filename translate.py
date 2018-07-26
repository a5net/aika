from googletrans import Translator
import re
import pandas as pd
from nltk.stem.snowball import RussianStemmer

stemmer = RussianStemmer()

lang_frame = pd.read_csv("languages.csv", encoding='utf-8')
lang_dict = dict()
for index, row in lang_frame.iterrows():
    lang = row["language_name"]
    code = row["code"]
    lang_dict[stemmer.stem(lang)] = code


# def source_language(command):
#     code = 'ru'
#     source_regex = 'с ([а-яА-ЯёЁ]+)'
#     data = re.search(source_regex, command)
#     if data != None:    
#         language = stemmer.stem(data.group(1))
#         code = lang_dict[language]

#     return code

def destination_language(command):
    code = 'ru'
    destination_regex = ['на ([а-яА-ЯёЁ]+)', 'по-([а-яА-ЯёЁ]+)']
    for regex in destination_regex:
        data = re.search(regex, command)
        if data != None:
            language = stemmer.stem(data.group(1))
            code = lang_dict[language]

    return code

def translate(command):
    dest = destination_language(command)
    phrase = input('Какую фразу или слово вам надо перевести? \n')
    translator = Translator()
    translation = translator.translate(phrase, dest = dest).text

    return translation

print(translate('переведи'))