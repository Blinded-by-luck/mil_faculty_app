from PyQt5 import QtCore, QtGui, QtWidgets
from PasswordUi import Ui_MainWindow
import sys


class Password(QtWidgets.QMainWindow):

    def __init__(self, points, password):
        super(Password, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.points = points
        self.password = password

        self.ui.label_4.setText(str(self.points) + self.word())
        self.ui.label_2.setText(self.password)

        self.ui.pushButton.clicked.connect(lambda: self.pb_clicked())

    def word(self):
        if self.points == 1:
            return ' балл'
        elif self.points in [2, 3, 4]:
            return ' балла'
        else:
            return ' баллов'

    def pb_clicked(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Password(11, '2edvas')
    application.show()
    app.exec_()
