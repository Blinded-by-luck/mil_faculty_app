from PyQt5 import QtCore, QtGui, QtWidgets
from RegistrationUi import Ui_MainWindow
import sys


class Registration(QtWidgets.QMainWindow):

    def __init__(self):
        super(Registration, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.surname_name = ''
        self.group = ''

        self.ui.pushButton.clicked.connect(lambda: self.pb_clicked())

    def pb_clicked(self):
        text = self.ui.lineEdit.text()
        text = text.lower().split(' ')
        self.surname_name = ''
        for word in text:
            self.surname_name += word

        text = self.ui.lineEdit_2.text()
        text = text.lower().split(' ')
        self.group = ''
        for word in text:
            self.group += word

        self.close()

    def get_data(self):
        return self.surname_name, self.group


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Registration()
    application.show()
    app.exec_()
    #sys.exit(app.exec())
