from PyQt5 import QtWidgets
from TestAppUi import Ui_Form
from Dictionary import Questions
import sys
import numpy as np
import re


class TestApp(QtWidgets.QMainWindow):

    def __init__(self):
        super(TestApp, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)

        self.username = ''
        self.group = ''
        self.correct_points = 0
        self.user_answers = [None, None, [], None, None, None, [], [], None, []]
        self.Dict = Questions()
        self.list_of_questions_keys = self.generate_questions()
        self.password = self.password_create()

        self.set_questions()
        self.push_buttons()
        self.radio_buttons()
        self.checkboxes()

    def correct_word(self):
        if self.correct_points in [2, 3, 4]:
            return ' балла'
        elif self.correct_points == 1:
            return ' балл'
        else:
            return ' баллов'

    # Создание пароля
    def password_create(self):
        vocabulary = list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*()_+-=,./;{}[]|"')

        flag = True
        while flag:  # Генерация пароля до тех пор, пока rules не равно 4
            password = ''
            word = np.random.choice(vocabulary, 8)
            for letter in word:
                password += letter

            rules = 0
            if re.compile(r'[a-z]').findall(password):  # Проверка на присутствие нижнего регистра
                rules += 1
            if re.compile(r'[A-Z]').findall(password):  # Проверка на присутствие верхнего регистра
                rules += 1
            if re.compile(r'\d').findall(password):  # Проверка на присутствие цифр
                rules += 1
            if re.compile(r'\D\W').findall(password):  # Проверка на присутствие специальных символов
                rules += 1
            if rules == 4:
                flag = False

        return password

    # Случайный выбор вопросов из Dict
    def generate_questions(self):
        test_questions = []
        all_questions_keys = list(self.Dict.quest.keys())
        one_answer = []
        multiple_answer = []
        string_answer = []
        # Поиск всех вопросов всех типов и добавление в соответствующие списки
        for question_key in all_questions_keys:
            if question_key[0] == 1:
                one_answer.append(question_key)
            elif question_key[0] == 2:
                multiple_answer.append(question_key)
            else:
                string_answer.append(question_key)

        # Выбор случайных вопросов по типам
        test_one_answer = np.random.choice(range(len(one_answer)), 4, replace=False)
        test_multiple_answer = np.random.choice(range(len(multiple_answer)), 4, replace=False)
        test_string_answer = np.random.choice(range(len(string_answer)), 2, replace=False)

        # Добавление выбранных вопросов в список со всеми вопросами теста
        test_questions.append(one_answer[test_one_answer[0]])
        test_questions.append(one_answer[test_one_answer[1]])
        test_questions.append(multiple_answer[test_multiple_answer[0]])
        test_questions.append(string_answer[test_string_answer[0]])
        test_questions.append(one_answer[test_one_answer[2]])
        test_questions.append(string_answer[test_string_answer[1]])
        test_questions.append(multiple_answer[test_multiple_answer[1]])
        test_questions.append(multiple_answer[test_multiple_answer[2]])
        test_questions.append(one_answer[test_one_answer[3]])
        test_questions.append(multiple_answer[test_multiple_answer[3]])

        return test_questions

    # Размещение вопросов и вариантов ответа на каждой странице
    def set_questions(self):

        # Вопрос 1
        answer = self.Dict.quest[self.list_of_questions_keys[0]]
        self.ui.label_5.setText(self.list_of_questions_keys[0][1])
        self.ui.label_8.setText(answer[0][1])
        self.ui.label_6.setText(answer[1][1])
        self.ui.label_7.setText(answer[2][1])

        # Вопрос 2
        answer = self.Dict.quest[self.list_of_questions_keys[1]]
        self.ui.label_16.setText(self.list_of_questions_keys[1][1])
        self.ui.label_13.setText(answer[0][1])
        self.ui.label_14.setText(answer[1][1])
        self.ui.label_15.setText(answer[2][1])

        # Вопрос 3
        answer = self.Dict.quest[self.list_of_questions_keys[2]]
        self.ui.label_18.setText(self.list_of_questions_keys[2][1])
        self.ui.label_20.setText(answer[0][1])
        self.ui.label_21.setText(answer[1][1])
        self.ui.label_22.setText(answer[2][1])
        self.ui.label_23.setText(answer[3][1])
        self.ui.label_24.setText(answer[4][1])

        # Вопрос 4
        self.ui.label_26.setText(self.list_of_questions_keys[3][1])

        # Вопрос 5
        answer = self.Dict.quest[self.list_of_questions_keys[4]]
        self.ui.label_30.setText(self.list_of_questions_keys[4][1])
        self.ui.label_27.setText(answer[0][1])
        self.ui.label_28.setText(answer[1][1])
        self.ui.label_29.setText(answer[2][1])

        # Вопрос 6
        self.ui.label_32.setText(self.list_of_questions_keys[5][1])

        # Вопрос 7
        answer = self.Dict.quest[self.list_of_questions_keys[6]]
        self.ui.label_34.setText(self.list_of_questions_keys[6][1])
        self.ui.label_35.setText(answer[0][1])
        self.ui.label_36.setText(answer[1][1])
        self.ui.label_37.setText(answer[2][1])
        self.ui.label_38.setText(answer[3][1])
        self.ui.label_39.setText(answer[4][1])

        # Вопрос 8
        answer = self.Dict.quest[self.list_of_questions_keys[7]]
        self.ui.label_41.setText(self.list_of_questions_keys[7][1])
        self.ui.label_42.setText(answer[0][1])
        self.ui.label_43.setText(answer[1][1])
        self.ui.label_44.setText(answer[2][1])
        self.ui.label_45.setText(answer[3][1])
        self.ui.label_46.setText(answer[4][1])

        # Вопрос 9
        answer = self.Dict.quest[self.list_of_questions_keys[8]]
        self.ui.label_48.setText(self.list_of_questions_keys[8][1])
        self.ui.label_50.setText(answer[0][1])
        self.ui.label_51.setText(answer[1][1])
        self.ui.label_52.setText(answer[2][1])

        # Вопрос 10
        answer = self.Dict.quest[self.list_of_questions_keys[9]]
        self.ui.label_59.setText(self.list_of_questions_keys[9][1])
        self.ui.label_53.setText(answer[0][1])
        self.ui.label_54.setText(answer[1][1])
        self.ui.label_55.setText(answer[2][1])
        self.ui.label_56.setText(answer[3][1])
        self.ui.label_57.setText(answer[4][1])

    # Подключение push buttons
    def push_buttons(self):
        self.ui.pushButton.clicked.connect(lambda: self.pb1_clicked())
        self.ui.pushButton_2.clicked.connect(lambda: self.pb2_clicked('one', self.list_of_questions_keys[0], 0))
        self.ui.pushButton_3.clicked.connect(lambda: self.pb2_clicked('one', self.list_of_questions_keys[1], 1))
        self.ui.pushButton_4.clicked.connect(lambda: self.pb2_clicked('multiple', self.list_of_questions_keys[2], 2))
        self.ui.pushButton_5.clicked.connect(lambda: self.pb2_clicked('string', self.list_of_questions_keys[3], 3))
        self.ui.pushButton_6.clicked.connect(lambda: self.pb2_clicked('one', self.list_of_questions_keys[4], 4))
        self.ui.pushButton_7.clicked.connect(lambda: self.pb2_clicked('string', self.list_of_questions_keys[5], 5))
        self.ui.pushButton_8.clicked.connect(lambda: self.pb2_clicked('multiple', self.list_of_questions_keys[6], 6))
        self.ui.pushButton_9.clicked.connect(lambda: self.pb2_clicked('multiple', self.list_of_questions_keys[7], 7))
        self.ui.pushButton_10.clicked.connect(lambda: self.pb2_clicked('one', self.list_of_questions_keys[8], 8))
        self.ui.pushButton_11.clicked.connect(lambda: self.pb3_clicked('multiple', self.list_of_questions_keys[9], 9))
        self.ui.pushButton_12.clicked.connect(lambda: self.close())
        self.ui.pushButton_13.clicked.connect(lambda: self.close())

    # Подключение radio buttons
    def radio_buttons(self):
        # Вопрос 1
        self.ui.radioButton.ans = 0
        self.ui.radioButton.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton, 0))
        self.ui.radioButton_2.ans = 1
        self.ui.radioButton_2.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_2, 0))
        self.ui.radioButton_3.ans = 2
        self.ui.radioButton_3.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_3, 0))

        # Вопрос 2
        self.ui.radioButton_7.ans = 0
        self.ui.radioButton_7.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_7, 1))
        self.ui.radioButton_8.ans = 1
        self.ui.radioButton_8.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_8, 1))
        self.ui.radioButton_9.ans = 2
        self.ui.radioButton_9.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_9, 1))

        # Вопрос 5
        self.ui.radioButton_10.ans = 0
        self.ui.radioButton_10.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_10, 4))
        self.ui.radioButton_11.ans = 1
        self.ui.radioButton_11.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_11, 4))
        self.ui.radioButton_12.ans = 2
        self.ui.radioButton_12.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_12, 4))

        # Вопрос 9
        self.ui.radioButton_13.ans = 0
        self.ui.radioButton_13.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_13, 8))
        self.ui.radioButton_14.ans = 1
        self.ui.radioButton_14.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_14, 8))
        self.ui.radioButton_15.ans = 2
        self.ui.radioButton_15.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_15, 8))

    # Подключение checkboxes
    def checkboxes(self):
        # Вопрос 3
        self.ui.checkBox.ans = 0
        self.ui.checkBox.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox, 2))
        self.ui.checkBox_2.ans = 1
        self.ui.checkBox_2.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_2, 2))
        self.ui.checkBox_3.ans = 2
        self.ui.checkBox_3.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_3, 2))
        self.ui.checkBox_4.ans = 3
        self.ui.checkBox_4.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_4, 2))
        self.ui.checkBox_5.ans = 4
        self.ui.checkBox_5.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_5, 2))

        # Вопрос 7
        self.ui.checkBox_10.ans = 0
        self.ui.checkBox_10.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_10, 6))
        self.ui.checkBox_6.ans = 1
        self.ui.checkBox_6.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_6, 6))
        self.ui.checkBox_7.ans = 2
        self.ui.checkBox_7.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_7, 6))
        self.ui.checkBox_8.ans = 3
        self.ui.checkBox_8.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_8, 6))
        self.ui.checkBox_9.ans = 4
        self.ui.checkBox_9.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_9, 6))

        # Вопрос 8
        self.ui.checkBox_15.ans = 0
        self.ui.checkBox_15.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_15, 7))
        self.ui.checkBox_11.ans = 1
        self.ui.checkBox_11.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_11, 7))
        self.ui.checkBox_12.ans = 2
        self.ui.checkBox_12.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_12, 7))
        self.ui.checkBox_13.ans = 3
        self.ui.checkBox_13.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_13, 7))
        self.ui.checkBox_14.ans = 4
        self.ui.checkBox_14.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_14, 7))

        # Вопрос 10
        self.ui.checkBox_20.ans = 0
        self.ui.checkBox_20.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_20, 9))
        self.ui.checkBox_16.ans = 1
        self.ui.checkBox_16.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_16, 9))
        self.ui.checkBox_17.ans = 2
        self.ui.checkBox_17.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_17, 9))
        self.ui.checkBox_18.ans = 3
        self.ui.checkBox_18.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_18, 9))
        self.ui.checkBox_19.ans = 4
        self.ui.checkBox_19.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_19, 9))

    def cb_clicked(self, checkbox, number):
        if checkbox.isChecked():
            if checkbox.ans not in self.user_answers[number]:
                self.user_answers[number].append(checkbox.ans)

    def rb_clicked(self, radiobutton, number):
        self.user_answers[number] = radiobutton.ans

    def pb1_clicked(self):
        text1 = self.ui.lineEdit_3.text()
        self.username = text1

        text2 = self.ui.lineEdit_4.text()
        text2 = text2.lower().split(' ')
        for word in text2:
            self.group += word

        if self.username == '' or self.group == '':
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Заполните все поля')
        else:
            self.ui.stackedWidget.setCurrentIndex(1)

    def pb2_clicked(self, question_type, key, number):
        if question_type == 'one':
            self.correct_points += self.check_answer_one(key, self.user_answers[number])
        elif question_type == 'multiple':
            self.correct_points += self.check_answer_multiple(key, self.user_answers[number])
        elif question_type == 'string':
            self.correct_points += self.check_answer_string(key, number)

        self.ui.stackedWidget.setCurrentIndex(number + 2)

    def pb3_clicked(self, question_type, key, number):
        if question_type == 'multiple':
            self.correct_points += self.check_answer_multiple(key, self.user_answers[number])

        if self.correct_points <= 8:
            self.ui.stackedWidget.setCurrentIndex(11)
            self.ui.label_12.setText(str(self.correct_points) + self.correct_word())
            self.ui.label_2.setText(self.password)
        else:
            self.ui.stackedWidget.setCurrentIndex(12)
            self.ui.label_65.setText(str(self.correct_points) + self.correct_word())

    def check_answer_one(self, key, user_answer):
        if user_answer is not None:
            if self.Dict.quest[key][user_answer][2] == 1:
                return 1
            else:
                return 0
        else:
            return 0

    def check_answer_multiple(self, key, user_answer):
        points = 0
        for i in user_answer:
            if self.Dict.quest[key][i][2] == 1:
                points += 1

        true_points = 0
        for j in range(len(self.Dict.quest[key])):
            true_points += self.Dict.quest[key][j][2]

        if points == true_points:
            return 1
        else:
            return 0

    def check_answer_string(self, key, number):
        if number == 3:
            text = self.ui.lineEdit_5.text()
        elif number == 5:
            text = self.ui.lineEdit_6.text()

        text = text.lower().split(' ')
        answer = ''
        for word in text:
            answer += word

        if answer != '':
            self.user_answers[number] = answer
            i = 1
            for correct_answer in self.Dict.quest[key]:
                if answer == correct_answer[1]:
                    return 1
                else:
                    i += 1
            if i >= len(self.Dict.quest[key]):
                return 0
        else:
            return 0

    def get_token(self):
        return self.password

    def get_username(self):
        return self.username


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = TestApp()
    application.show()
    sys.exit(app.exec())
