'''
локализация кибаны с использованием  Google translator на примере русского языка - ru
нужный для вас можно посмотреть в файле language.txt
'''

import json
import re
from googletrans import Translator # Google translator - спасибо Google за переводчик
from tqdm import tqdm

class Local_Kibana_settings():
    def __init__(self, language, openfile, savefile):
        self.dest = language
        self.openfile = openfile
        self.savefile = savefile
        self.translator = Translator()
        self.ru = {}  # словарь "messages" с русскими словами
        self.data_ru = {}  #
        self.ch_word = {}
        self.count_pbar = 0
        self.pbar = []
        self.open_json()
        self.form_word()


    def open_json(self):
        with open(self.openfile, 'r', encoding='utf-8') as fh: # /your_path/ - ваша папка с файлом китайской локализации
            self.data = json.load(fh) #загружаем из файла китайской локализации данные в словарь data
            self.ru = self.data["messages"]  # словарь "messages" с китайскими словами

    # формирование отдельных слов для перевода

    def form_word(self):
        self.count_word = 0
        rus = self.ru
        for key in rus:
            rus[key] = rus[key] + " " # добавление технического пробела
            letters_china = re.findall(u'[\u4e00-\u9fff]', rus[key]) # список китайских букв в строке
            words = [] # список китайских слов в строке
            if letters_china != []:
                letters_china.append("")
                n = 0
                word = ""
                for letter in rus[key]:
                    try:
                        if letter == letters_china[n]:
                            word += letters_china[n]
                            n += 1
                        elif word != "":
                            self.count_word += 1
                            words.append(word)
                            word = ""
                    except:
                        pass
            self.ch_word[key] = words
        if self.count_word < 100:
            self.save_json()
        else:
            self.translate_word()

    def translate_word(self):
        self.pbar.append(tqdm(total=self.count_word))
        for key in self.ch_word:
            if self.ch_word[key] != []:
                ch_rus = []
                for value in self.ch_word[key]:
                    result = self.translator.translate(value, src='zh-CN', dest=self.dest)  # результат перевода
                    # time.sleep(1)  # таймаут для успеха перевода
                    ch_rus.append([value,result.text])
                    self.pbar[self.count_pbar].update(1)
                self.ch_word[key] = ch_rus  # формирование списка  китайских слов ,и их перевода на русский
        self.replace_word()
        self.count_pbar += 1

    # Замена китайских слов на русские в словаре ru
    def replace_word(self):
        for key in self.ru:
            if self.ch_word[key] != []:
                for value in self.ch_word[key]:
                    self.ru[key] = self.ru[key].replace(value[0], value[1])

        self.form_word()

# формирование файла русской локализации
    def save_json(self):
        self.data_ru = self.data  # присвоение данных файла китайской локализации
        self.data_ru["messages"] = self.ru  # изменение словаря "messages" с русскими словами
        with open(self.savefile, 'w', encoding='utf-8') as file:
            json.dump(self.data_ru, file, indent=4, ensure_ascii=False) # сохраняем данные в файл русской локализации


if __name__ == "__main__":
    language = 'ru' # можно выбрать любой другой язык локализации
    openfile = 'E:/Disk_C/762/ru-RU5.json' # исходный файл китайской локализации
    # openfile = 'E:/Disk_C/762/ru-RU2.json'  # исходный файл китайской локализации
    savefile = 'E:/Disk_C/762/ru-RU.json' # получаемый файл русской локализации
    localize = Local_Kibana_settings(language, openfile, savefile)
