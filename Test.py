from PyQt5 import QtCore, QtGui, QtWidgets
from Multiple import MultipleAnswer
from One import OneAnswer
from String import StringAnswer
from RegistrationClass import Registration
from Dictionary import Questions
import numpy as np
import sys
import re


class Test:
    def __init__(self, password_len=8, questions_len=12):
        self.password_len = password_len
        self.questions_len = questions_len
        self.surname_name = ''
        self.group = ''
        self.password = ''
        self.questions = Questions().get_dictionary()
        self.MultipleAnswer = MultipleAnswer
        self.OneAnswer = OneAnswer
        self.StringAnswer = StringAnswer
        self.application = []
        self.app = []
        self.user_points = 0
        self.true_points = 0

    def show_questions(self, dict, key, quest_number):
        if key[0] == 1:
            self.application.append(self.OneAnswer(dict, key, quest_number))   # Один вариант ответа
        elif key[0] == 2:
            self.application.append(self.MultipleAnswer(dict, key, quest_number))  # Несколько вариантов ответа
        elif key[0] == 3:
            self.application.append(self.StringAnswer(dict, key, quest_number))  # Символьный ответ
        self.app.append(QtWidgets.QApplication([]))
        self.application[quest_number - 1].show()
        self.app[quest_number - 1].exec_()
        self.user_points += self.application[quest_number - 1].get_points()

    def password_create(self):
        vocabulary = list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*()_+-=,./;{}[]|"')

        flag = True
        while flag:  # Генерация пароля до тех пор, пока rules не равно 4
            self.password = ''
            password = np.random.choice(vocabulary, self.password_len)
            for letter in password:
                self.password += letter

            rules = 0
            if re.compile(r'[a-z]').findall(self.password):  # Проверка на присутствие нижнего регистра
                rules += 1
            if re.compile(r'[A-Z]').findall(self.password):  # Проверка на присутствие верхнего регистра
                rules += 1
            if re.compile(r'\d').findall(self.password):  # Проверка на присутствие цифр
                rules += 1
            if re.compile(r'\D\W').findall(self.password):  # Проверка на присутствие специальных символов
                rules += 1
            if rules == 4:
                flag = False

    def run(self):
        # Приветственное окно
        app = QtWidgets.QApplication([])
        application = Registration()
        application.show()
        app.exec_()
        self.surname_name, self.group = application.get_data()

        # Генерация пароля
        self.password_create()

        # Вопросы
        quest_ind = range(len(list(self.questions.keys())))
        list_of_questions = np.random.choice(quest_ind, self.questions_len, replace=False)
        i = 1
        for quest in list_of_questions:
            self.show_questions(self.questions, list(self.questions.keys())[quest], i)
            i += 1

        print(self.surname_name)
        print(self.group)
        print(self.user_points, '/', self.questions_len, sep='')

        # Проверка на зачет/незачет
        if self.user_points >= self.password_len:
            print('Ваш пароль:', self.password)
        else:
            print('Вы не набрали достаточное количество баллов')

        sys.exit()


test = Test()
test.run()


