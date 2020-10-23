from PyQt5 import QtCore, QtGui, QtWidgets
from OneUi import Ui_MainWindow
import sys


class OneAnswer(QtWidgets.QMainWindow):
    def __init__(self, dict, key, quest_number):
        super(OneAnswer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dict = dict
        self.key = key
        self.user_answer = None
        self.points = 0
        self.result = None
        self.setClose = False

        self.ui.label.setText(key[1])
        self.ui.label.setWordWrap(True)

        self.ui.label_2.setText('Вопрос ' + str(quest_number))
        self.ui.label_3.setText(self.dict[self.key][0][1])
        self.ui.label_4.setText(self.dict[self.key][1][1])
        self.ui.label_5.setText(self.dict[self.key][2][1])

        self.ui.radioButton.number = 1
        self.ui.radioButton.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton))

        self.ui.radioButton_2.number = 2
        self.ui.radioButton_2.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_2))

        self.ui.radioButton_3.number = 3
        self.ui.radioButton_3.toggled.connect(lambda: self.rb_clicked(self.ui.radioButton_3))

        self.ui.pushButton.clicked.connect(lambda: self.pb_clicked())

    def rb_clicked(self, radiobutton):
        self.user_answer = radiobutton.number

    def pb_clicked(self):
        if self.user_answer is None:
            self.points = 0
        else:
            if self.dict[self.key][self.user_answer - 1][2] == 1:
                self.points += 1

        self.setClose = True
        self.close()

    def get_points(self):
        return self.points

    def closeEvent(self, e):
        if self.setClose:
            e.accept()
        else:
            self.result = QtWidgets.QMessageBox.question(self, 'Подтверждение',
                                                         'Вы действительно хотите прекратить выполнение теста?',
                                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                         QtWidgets.QMessageBox.No)

            if self.result == QtWidgets.QMessageBox.Yes:
                e.accept()
                QtWidgets.QWidget.closeEvent(self, e)
            else:
                e.ignore()



dictionary = {
    (1,  "Основной задачей программы-детектора является:"):
	[[1, "Нахождение вирусов в оперативной памяти, на внутренних и(или) внешних носителях", 1],
	 [2, "Выполнение иммунизации системы(файлов, каталогов), блокируя действие вирусов", 0],
	 [3, "Анализировать накопленную информацию на жестком диске, в реальном времени или периодически", 0]],

    (2, "Используемыми методами Антивирусного монитора являются:"):
	[[1, "Эвристический анализ", 1],
	 [2, "Сигнатурный анализ", 0],
	 [3, "Мониторинг и блокировка потенциально опасных действий", 1],
	 [4, "Эмуляция процессора", 1],
	 [5, "Периодическое сканирование дисков", 0]],
    (1,"Как в терминале пользователя предотвратить утечку информации при подключении незарегистрированного терминала в многопользовательском режиме?"):
[[1, "Необходимо перед выдачей запрашиваемых данных осуществить идентификацию терминала, с которого поступил запрос",
  0],
 [2, "Необходимо осуществить аутентификацию пользователя, установить его подлинность и полномочия", 1],
 [3,
  "Необходимо определить ключ незарегистрированного терминала, и проверить его принадлежность к списку возможных авторизованных пользователей",
  0]
 ]
}
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = OneAnswer(dictionary, (1,"Как в терминале пользователя предотвратить утечку информации при подключении незарегистрированного терминала в многопользовательском режиме?"), 1)
    application.show()
    app.exec_()
