from PyQt5 import QtCore, QtGui, QtWidgets
from MultipleUi import Ui_MainWindow
import sys


class MultipleAnswer(QtWidgets.QMainWindow):

    def __init__(self, dict, key, quest_number):
        super(MultipleAnswer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dict = dict
        self.key = key
        self.user_answer = []
        self.points = 0
        self.true_points = 0
        self.result = None
        self.setClose = False

        self.ui.label.setText(self.key[1])
        self.ui.label_2.setText('Вопрос ' + str(quest_number))
        self.ui.label_3.setText(self.dict[self.key][0][1])
        self.ui.label_4.setText(self.dict[self.key][1][1])
        self.ui.label_5.setText(self.dict[self.key][2][1])
        self.ui.label_6.setText(self.dict[self.key][3][1])
        self.ui.label_7.setText(self.dict[self.key][4][1])

        self.ui.checkBox.number = 1
        self.ui.checkBox.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox))

        self.ui.checkBox_2.number = 2
        self.ui.checkBox_2.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_2))

        self.ui.checkBox_3.number = 3
        self.ui.checkBox_3.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_3))

        self.ui.checkBox_4.number = 4
        self.ui.checkBox_4.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_4))

        self.ui.checkBox_5.number = 5
        self.ui.checkBox_5.toggled.connect(lambda: self.cb_clicked(self.ui.checkBox_5))

        self.ui.pushButton.clicked.connect(lambda: self.pb_clicked())

    def cb_clicked(self, checkbox):
        if checkbox.isChecked():
            if checkbox.number not in self.user_answer:
                self.user_answer.append(checkbox.number)
        else:
            if checkbox.number in self.user_answer:
                self.user_answer.remove(checkbox.number)

    def pb_clicked(self):
        self.points = 0
        for i in self.user_answer:
            if self.dict[self.key][i - 1][2] == 1:
                self.points += 1
            else:
                self.points -= 1

        self.true_points = 0
        for j in range(len(self.dict[self.key])):
            self.true_points += self.dict[self.key][j][2]

        if self.points == self.true_points:
            self.points = 1
        else:
            self.points = 0
        self.setClose = True
        self.close()

    def get_points(self):
        return self.points

    def closeEvent(self, e):
        if self.setClose:
            e.accept()
        else:
            self.result = QtWidgets.QMessageBox.question(self, 'Подтверждение', 'Вы действительно хотите прекратить выполнение теста?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

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
    application = MultipleAnswer(dictionary, (2, "Используемыми методами Антивирусного монитора являются:"), 1)
    application.show()
    app.exec_()
    #sys.exit(app.exec())
