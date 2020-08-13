'''
локализация кибаны с использованием  Google translator на примере русского языка - ru
нужный для вас можно посмотреть в файле language.txt
'''

import json
import time
import re
from googletrans import Translator # Google translator - спасибо Google за переводчик

with open('/your_path/zh-CN.json', 'r', encoding='utf-8') as fh: # /your_path/ - ваша папка с файлом китайской локализации
    data = json.load(fh) #загружаем из файла китайской локализации данные в словарь data

ch = data["messages"] # словарь "messages" с китайскими словами
n_val = 10**9 # индексы для замены переменных
message_n = {} # словарь "messages" со списком переменных и их заменой на индексы
message_ch = {} # словарь "messages"  с индексами вместо переменных, китайский
message_ru = {} # словарь "messages"  с индексами вместо переменных, русский
ru = {} # словарь "messages" с русскими словами
data_ru = {} #

# замена переменных на индексы
for key in ch:
    n = ch[key].count("{") # подсчет фигурных скобок - переменные заключены в {}
    variable_end = 0 # задаем начало поиска переменной
    ch_int = [] #  список для переменных в строке
    stroka = ch[key] #  присвоение значения ключа

    if n > 0: # проверка на наличие пременных
        for i in range(n):
            variable_start = ch[key].find("{", variable_end) #  значение начала переменной
            variable_end = ch[key].find("}", variable_end) #  значение окончания переменной
            variable = ch[key][variable_start:variable_end + 1] # значание переменной
            result = re.findall(r'[A-z]', variable) # поиск в переменной латиницы
            if len(result) > 0: # наличие в переменной латиницы
                ch_int.append(["{" + str(n_val) + "}", variable]) # добавление в список индекса и переменной
                stroka = stroka.replace(variable, "{" + str(n_val) + "}",1) # замена переменной на значение индекса
                message_n[key] = ch_int # формирование словаря "messages" со списком переменных и их заменой на индексы
                n_val += 1 # инкремент индекса
                variable_end += 1 # изменение начала поиска переменной
    message_ch[key] = stroka # формирование словаря "messages"  с индексами вместо переменных, китайский

# перевод с китайского
translator = Translator()
for key, value in message_ch.items(): # просмотр словаря "messages"  с индексами вместо переменных, китайский
    if value != " ": # проверка пустого значения (пустое не переводится!!!)
        result = translator.translate(value, src='zh-CN', dest='ru') # результат перевода
        time.sleep(1) # таймаут для успеха перевода
        message_ru[key] = result.text # формирование словаря "messages"  с индексами вместо переменных, русский
    else:
        message_ru[key] = message_ch[key] #

# замена кавычки " на апостроф `
for key, value in message_ru.items(): # просмотр словаря "messages"  с индексами вместо переменных, русский
    if '"' in value: # проверка наличия кавычек
        value_new = value.replace('"','`') # замена кавычки " на апостроф `
        message_ru[key] = value_new # изменение словаря "messages"  с индексами вместо переменных, русский

ru = message_ru # присвоение данных словарю "messages" с русскими словами

# замена индексов на переменные
for key, value in message_n.items(): # просмотр словаря "messages" со списком переменных и их заменой на индексы
    stroka = ru[key] # присвоение значения ключа словаря "messages" с русскими словами
    for i in  value:
        stroka = stroka.replace(i[0],i[1]) # замена индексов на переменные
    ru[key] = stroka # формирование словаря "messages" с русскими словами

data_ru = data # присвоение данных файла китайской локализации
data_ru["messages"] = ru # изменение словаря "messages" с русскими словами

# формирование файла русской локализации
with open('/your_path/ru-RU.json', 'w', encoding='utf-8') as file:
    json.dump(data_ru, file, indent=4, ensure_ascii=False) # сохраняем данные в файл русской локализации