# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.1


from PyQt5 import QtCore, QtGui, QtWidgets
from sys import exit
import socket
from threading import Thread
from PyQt5.QtWidgets import QMessageBox

class UiClient(object):

    def text_on_textBox(self):
        while True:
            self.textBrowser.append("\n"+self.client.recv(2048).decode("utf-8"))


    def send_server(self):
        listen_thread = Thread(target=self.text_on_textBox)
        listen_thread.start()

        self.client.send(self.plainTextEdit.toPlainText().encode("utf-8"))
        self.plainTextEdit.clear()

    def setupUi(self, MainWindow):
        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        try:
            self.client.connect(
                ("127.0.0.1", 1234)
            )
        except:
            alert = QMessageBox()
            alert.setText('Ошибка подключения к серверу!')
            alert.exec_()
            exit()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 500)
        MainWindow.setMinimumSize(QtCore.QSize(630, 500))
        MainWindow.setMaximumSize(QtCore.QSize(630, 500))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(34, 34, 34);")
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 460, 131, 31))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(exit)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(70, 290, 411, 161))
        self.plainTextEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.plainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(70, 50, 411, 192))
        self.textBrowser.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.textBrowser.setObjectName("textBrowser")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 350, 75, 51))
        self.pushButton_2.setStyleSheet("background-color: rgb(0, 0, 127);\n"
"font: 87 16pt \"Segoe UI Black\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.send_server)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 270, 141, 16))
        self.label.setStyleSheet("font: 87 12pt \"Segoe UI Black\";\n"
"color: rgb(255, 255, 255);\n"
"background-color:rgb(33, 33, 33);\n"
"")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 30, 141, 21))
        self.label_2.setStyleSheet("font: 87 12pt \"Segoe UI Black\";\n"
"color: rgb(164, 164, 246);\n"
"background-color: rgb(34, 34, 34);")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Exit"))
        self.pushButton_2.setText(_translate("MainWindow", "SEND"))
        self.label.setText(_translate("MainWindow", "Консоль команд"))
        self.label_2.setText(_translate("MainWindow", "Вывод сервера"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiClient()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
