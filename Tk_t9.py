# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
Плагин - приложение по исправлению орфографической ошибкой
"""

import json
import tkinter
import tkinter.scrolledtext
from functools import partial
import requests
from Check_class import Check_class
import pyperclip

class Text_T9:
    """""
    import Tk_t9
    T9 = Tk_t9.Text_T9(tkinter.Tk, tkinter.Text,'ru')
    T9.Start()
    """
    @Check_class(0)
    def __init__(self: None, master: tkinter.Tk, Text_it: None, Lang: str):

        self.button = [[], []]
        self.Lang = Lang
        self.Индекс_неправильных_слов = []
        self.Right_words = self.Save_load_Right('r')

        """ Tkinter """
        self.Windows = master
        self.frame0 = tkinter.Frame(self.Windows)
        self.frame1 = tkinter.Frame(self.Windows)
        self.Text_set = Text_it
        self.Оffer_Lab = tkinter.Button(
            self.Windows, bg='#9AB85A', text='?', relief=tkinter.RIDGE, command=self.Getting_text)  # Текст с ошибкой
        for x in range(6):  # Cвертка Button
            if x < 3:
                self.button[0].append(tkinter.Button(
                    self.frame0, bg='#74A889', width=1, height=1, text='-',
                    command=partial(self.Set_Text, x)))
            else:
                self.button[1].append(tkinter.Button(
                    self.frame1, bg='#74A889', width=1, height=1, text='-',
                    command=partial(self.Set_Text, x)))
        self.Windows.bind("<Key>", self.Key_invent)

        """
        # partial для того чтобы в цикле давать разные значения функции
        #self.Text_set.bind('<KeyRelease>', lambda *args: self.Getting_text())
        """

    @Check_class(0)
    def Start(self: None):
        """
        Делает:
        1) Расположение кнопок в окне
        2) Список упакованных кнопок по три в каждой ячейке [[],[]]

        Нужно:
        1) self.Text_set
        2) self.Оffer_Lab
        3) self.button
        4) self.frame0,self.frame
        5) self.Getting_text()
        """
        self.Оffer_Lab.pack(fill=tkinter.BOTH)
        for x in self.button:
            self.frame0.pack(fill=tkinter.BOTH)
            self.frame1.pack(fill=tkinter.BOTH)
            for y in x:
                y.pack(side='left', fill=tkinter.BOTH, expand=True)
        self.Getting_text()

    @Check_class(0)
    def Key_invent(self: None, event: tkinter.Event):
        """
        Делает:
        1) Работа с буфером памяти

        Нужно:
        0) pyperclip
        1) self.Text_set
        2) event:tkinter.Event
        3) Getting_text - удобство
        """

        Key = bytes(event.char, encoding='utf-8')

        if Key == b'\x16':  # 'Ctr+v'
            self.Text_set.insert(tkinter.INSERT, str(pyperclip.paste()))
            self.Getting_text()

        elif Key == b'\x03':  # 'Ctr+c'
            pyperclip.copy(self.Text_set.get(1.0, 'end-1c'))

        elif Key == b'\x18':  # 'Ctr+x'
            self.Text_set.delete(1.0, tkinter.END)

    @Check_class(0)
    def Save_load_Right(self: None, reg: str, Right_words: dict = {}):
        """
        Делает:
        1) Кэширует в self.Right_words

        Нужно:
        0) json
        1) self.Right_words
        """
        if reg == 'r':
            try:
                with open('Right_words.json', 'r', encoding='utf-8') as JSR:
                    Right = json.load(JSR)
            except FileNotFoundError:
                with open('Right_words.json', 'w', encoding='utf-8') as JSW:
                    json.dump({}, JSW, sort_keys=False,
                              ensure_ascii=False)
                with open('Right_words.json', 'r', encoding='utf-8') as JSR:
                    Right = json.load(JSR)
            return Right

        with open('Right_words.json', 'r', encoding='utf-8') as JSR:
            Right = json.load(JSR)
            Right.update(Right_words)
        with open('Right_words.json', 'w', encoding='utf-8') as JSW:
            json.dump(Right, JSW, sort_keys=False, ensure_ascii=False)

    @Check_class(0)
    def Spelling(self: None, Text: list, lang: str):
        """
        Привязанная переменная:
        1) self.Right_wordsв -  кеш слов

        Делает:
        1) Проверяет орфографию
        2) Формируют ответ с ошибками - "Error_word"

        Нужно:
        0) requests
        1) Text list
        2) Язык в котором искать
        3) Помощник self.Right_words
        4) Визуал - self.Оffer_Lab
        5) self.Windows.update() - для оптимизации
        """

        Error_word = {}
        for text in Text:

            if text in self.Right_words:
                if self.Right_words[text][0]:
                    continue

                elif not self.Right_words[text][0]:
                    Error_word.update(self.Right_words[text][1])
                    continue

            else:
                try:
                    self.Оffer_Lab['bg'] = '#ABE7EC'
                    url = 'https://speller.yandex.net/services/spellservice.json/checkText?'
                    respons = requests.get(
                        url, params={'text': text, 'lang': lang}).json()
                    self.Windows.update()
                except requests.exceptions.ConnectionError:
                    raise Exception("NO INTERNET")

                if respons:
                    respons_Spelling = {}
                    for x in respons:
                        respons_Spelling[x['word']] = x['s']
                        self.Right_words[text] = (0, respons_Spelling)
                    Error_word.update(respons_Spelling)
                    continue

                elif not respons:
                    self.Right_words[text] = (1,)
                    self.Оffer_Lab['bg'] = '#9AB85A'
                    continue

        return Error_word

    @Check_class(0)
    def Auxiliary(self: None, text: list):
        """
        Привязанная переменная:
        1) self.Индекс_неправильных_слов -  для записи ответа

        Делает:
        1) Принимает текст в виде list
        2) отправляет его в self.Spelling
        3) Получает dict с неправильными словами
        4) Формирует ответ - "Индекс_неправильных_слов"
        4.1) Выделяет их | |
        4.2) Указывайте индекс расположения текста
        4.3) Приписывает вариант замены
        5) Заменяет в тексте слова на выделенные 

        Нужно:
        1) Полынй текст в list
        2) self.Spelling
        3) self.Индекс_неправильных_слов
        4) self.Text_set
        """

        sp_test = self.Spelling(text, self.Lang)

        for x in enumerate(text):
            if sp_test.get(x[1]):
                t = f'|{text[x[0]]}|'
                text[x[0]] = t
                self.Индекс_неправильных_слов.append((x[0], t, sp_test[x[1]]))

        self.Text_set.delete(1.0, tkinter.END)
        self.Text_set.insert(tkinter.INSERT, ' '.join(text))

    @Check_class(0)
    def Getting_text(self: None):
        """
        Нужно:
        1) self.Text_set - текстовое поле
        2) self.Auxiliary 
        3) self.Оffer_Lab 
        4) self.Индекс_неправильных_слов
        5) self.button
        6) self.Set_Text

        Делает:
        1) Получает слова из текстового поля
        2) Получает ответ от self.Auxiliary
        3) Берет первый элемент из self.Индекс_неправильных_слов
        4) Назначает self.Оffer_Lab неправильное слово
        5) Назначает кнопкам вариант замены слово если 
        нехватает слов то заменяет их на '-'
        5.1) Назначает кнопкам функции и атрибуты к ним
        5.1.1) Правильный вариант текста - Индекс этого текста

        6) Оптимезация: если ошибок нет то лишний раз при нажатие кнопки не
        переконфигурируются        
        """

        Text = self.Text_set.get(1.0, 'end-1c').split(' ')

        if Text != ['']:
            self.Auxiliary(Text)

        if self.Индекс_неправильных_слов:
            Spelling_Text = self.Индекс_неправильных_слов[0]
            if not self.Оffer_Lab['text'] == Spelling_Text[1]:
                self.Оffer_Lab['text'] = Spelling_Text[1]
                for x in enumerate(self.button[0]+self.button[1]):
                    try:
                        text = Spelling_Text[2][x[0]]
                        x[1]['text'] = text
                        x[1]['command'] = partial(
                            self.Set_Text, Spelling_Text[0], text)
                    except IndexError:
                        x[1]['text'] = '-'
                        x[1]['command'] = partial(self.Set_Text, '-')

        else: 
            if not self.button[0][0]['text'] == '-':
                self.Оffer_Lab['text'] = '-'
                for x in enumerate(self.button[0]+self.button[1]):
                    x[1]['text'] = '-'

    @Check_class(0)
    def Set_Text(self: None, Cord: int, text: str):
        """
        Делает:
        1) Непосредственная замена слов с ошибками
        2) Оптимизация - если этого слова больше нет то его пропускам
        чтобы небыло личшний раз не вставлять текст

        Нужно:
        1) self.Text_set
        1) Cord - Индекс неправильный слов
        2) text - Правильное слово
        3) self.Getting_text()
        4) self.Индекс_неправильных_слов
        5) self.Save_load_Right - Для оптимизации 

        """
        self.Save_load_Right('w', self.Right_words)

        All_text = self.Text_set.get(1.0, 'end-1c').split(' ')

        if All_text[Cord] == self.Оffer_Lab['text']:
            All_text[Cord] = text
            self.Text_set.delete(1.0, tkinter.END)
            self.Text_set.insert(tkinter.INSERT, ' '.join(All_text))
            self.Индекс_неправильных_слов.pop(0)
            self.Getting_text()

        else:
            self.Индекс_неправильных_слов.pop(0)
            self.Getting_text()


if __name__ == '__main__':
    Windows = tkinter.Tk()
    Windows.title('T-9')
    Windows.geometry('450x250')
    Text = tkinter.scrolledtext.ScrolledText(Windows, width=1, height=7)
    Text.pack(fill=tkinter.BOTH, expand=True)
    T9 = Text_T9(Windows, Text, 'ru')
    T9.Start()
    Windows.mainloop()
