from PyQt5 import QtCore, QtGui, QtWidgets
from NotPasswordUi import Ui_MainWindow
import sys


class NotPassword(QtWidgets.QMainWindow):

    def __init__(self, points):
        super(NotPassword, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.points = points

        self.ui.label_4.setText(str(self.points) + self.word())

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
    application = NotPassword(3)
    application.show()
    app.exec_()
