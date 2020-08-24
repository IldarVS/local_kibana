'''
локализация кибаны с использованием  Google translator на примере русского языка - ru
нужный для вас можно посмотреть в файле language.txt
'''

import json
import time
import re
from googletrans import Translator # Google translator - спасибо Google за переводчик


class Local_Kibana_settings():
    def __init__(self, language, openfile, savefile):
        self.dest = language
        self.openfile = openfile
        self.savefile = savefile
        self.translator = Translator()
        self.message_n = {}  # словарь "messages" со списком переменных и их заменой на индексы
        self.message_ch = {}  # словарь "messages"  с индексами вместо переменных, китайский
        self.message_ru = {}  # словарь "messages"  с индексами вместо переменных, русский
        self.ru = {}  # словарь "messages" с русскими словами
        self.data_ru = {}  #
        self.ch_word = {}
        self.open_json()
        self.index_var()
        self.translate()
        self.replace_apostrof()
        self.replace_var()
        self.form_word()
        self.translate_word()
        self.replace_word()
        self.save_json()

    def open_json(self):
        with open(self.openfile, 'r', encoding='utf-8') as fh: # /your_path/ - ваша папка с файлом китайской локализации
            self.data = json.load(fh) #загружаем из файла китайской локализации данные в словарь data


    def index_var(self): # индексация пременных
        self.ch = self.data["messages"]  # словарь "messages" с китайскими словами
        n_val = 10 ** 9  # индексы для замены переменных
        for key in self.ch:
            n = self.ch[key].count("{") # подсчет фигурных скобок - переменные заключены в {}
            variable_end = 0 # задаем начало поиска переменной
            ch_int = [] #  список для переменных в строке
            stroka = self.ch[key] #  присвоение значения ключа
            if n > 0: # проверка на наличие пременных
                for i in range(n):
                    variable_start = self.ch[key].find("{", variable_end)
                    variable_end = self.ch[key].find("}", variable_end) #  значение окончания переменной
                    if variable_start > variable_end:
                        variable_start = variable_end
                        variable_end = self.ch[key].find("}", variable_start + 1)
                    variable_end2 = self.ch[key].find("{", variable_start + 1)
                    if variable_end > variable_end2:
                        variable_end = variable_end2
                    if variable_end == -1: variable_end = len(self.ch[key])
                    variable = self.ch[key][variable_start:variable_end + 1] # значание переменной
                    result = re.findall(r'[A-z]', variable) # поиск в переменной латиницы
                    if len(result) > 0 : # наличие в переменной латиницы
                        ch_int.append(["{"+ str(n_val) + "}", variable]) # добавление в список индекса и переменной
                        stroka = stroka.replace(variable, "{"+ str(n_val) + "}") # замена переменной на значение индекса
                        self.message_n[key] = ch_int # формирование словаря "messages" со списком переменных и их заменой на индексы
                        n_val += 1 # инкремент индекса
                    variable_end += 1 # изменение начала поиска переменной
            self.message_ch[key] = stroka # формирование словаря "messages"  с индексами вместо переменных, китайский

    # перевод с китайского - долго более 5 часов
    def translate(self):
        n = 0
        for key, value in self.message_ch.items(): # просмотр словаря "messages"  с индексами вместо переменных, китайский
            if value != " ": # проверка пустого значения (пустое не переводится!!!)
                result = self.translator.translate(value, src='zh-CN', dest=self.dest) # результат перевода
                time.sleep(1) # таймаут для успеха перевода
                self.message_ru[key] = result.text # формирование словаря "messages"  с индексами вместо переменных, русский
            else:
                self.message_ru[key] = self.message_ch[key] #
            n += 1
            print(n)
    # замена кавычки " на апостроф `
    def replace_apostrof(self):
        for key, value in self.message_ru.items(): # просмотр словаря "messages"  с индексами вместо переменных, русский
            if '"' in value: # проверка наличия кавычек
                value_new = value.replace('"','`') # замена кавычки " на апостроф `
                self.message_ru[key] = value_new # изменение словаря "messages"  с индексами вместо переменных, русский
        self.ru = self.message_ru # присвоение данных словарю "messages" с русскими словами

    # замена индексов на переменные
    def replace_var(self):
        for key, value in self.message_n.items(): # просмотр словаря "messages" со списком переменных и их заменой на индексы
            stroka = self.ru[key] # присвоение значения ключа словаря "messages" с русскими словами
            for i in  value:
                stroka = stroka.replace(i[0],i[1]) # замена индексов на переменные
            self.ru[key] = stroka # формирование словаря "messages" с русскими словами

    # перевод отдельных слов, оставшихся без перевода

    def form_word(self):
        rus = self.ru
        for key in rus:
            rus[key] = rus[key] + " " # добавление технического пробела
            letters_china = re.findall(u'[\u4e00-\u9fff]', rus[key]) # список китайских букв в строке
            words = [] # список китайских слов в строке
            if letters_china != []:
                n = 0
                word = ""
                for letter in rus[key]:
                    try:
                        if letter == letters_china[n]:
                            word += letters_china[n]
                            n += 1
                        elif word != "":
                                words.append(word)
                                word = ""
                    except:
                        pass
                self.ch_word[key] = words

    def translate_word(self):
        n = 0
        for key in self.ch_word:
            if self.ch_word[key] != []:
                ch_rus = []
                for value in self.ch[key]:
                    result = self.translator.translate(value, src='zh-CN', dest=self.dest)  # результат перевода
                    time.sleep(1)  # таймаут для успеха перевода
                    ch_rus.append([value,result.text])
                    n += 1
                    print(n)
                self.ch_word[key] = ch_rus  # формирование списка  китайских слов ,и их перевода на русский

    # Замена китайских слов на русские в словаре ru
    def replace_word(self):
        for key in self.ru:
            if self.ch_word[key] != []:
                for value in self.ch_word[key]:
                    self.ru[key] = self.ru[key].replace(value[0], value[1])
        self.data_ru = self.data  # присвоение данных файла китайской локализации
        self.data_ru["messages"] = self.ru  # изменение словаря "messages" с русскими словами

# формирование файла русской локализации
    def save_json(self):
        with open(self.savefile, 'w', encoding='utf-8') as file:
            json.dump(self.data_ru, file, indent=4, ensure_ascii=False) # сохраняем данные в файл русской локализации


if __name__ == "__main__":
    language = 'ru' # можно выбрать любой другой язык локализации
    openfile = 'zh-CN.json' # исходный файл китайской локализации
    savefile = 'ru-RU.json' # получаемый файл русской локализации
    localize = Local_Kibana_settings(language, openfile, savefile)
