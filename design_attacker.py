# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_attacker.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_interface_attacker(object):
    def setupUi(self, interface_attacker):
        interface_attacker.setObjectName("interface_attacker")
        interface_attacker.resize(800, 600)
        interface_attacker.setMinimumSize(QtCore.QSize(800, 600))
        interface_attacker.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(interface_attacker)
        self.centralwidget.setObjectName("centralwidget")
        self.download_btn = QtWidgets.QPushButton(self.centralwidget)
        self.download_btn.setGeometry(QtCore.QRect(0, 330, 71, 51))
        self.download_btn.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.download_btn.setObjectName("download_btn")
        interface_attacker.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(interface_attacker)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        interface_attacker.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(interface_attacker)
        self.statusbar.setObjectName("statusbar")
        interface_attacker.setStatusBar(self.statusbar)

        self.retranslateUi(interface_attacker)
        QtCore.QMetaObject.connectSlotsByName(interface_attacker)

    def retranslateUi(self, interface_attacker):
        _translate = QtCore.QCoreApplication.translate
        interface_attacker.setWindowTitle(_translate("interface_attacker", "Project"))
        self.download_btn.setText(_translate("interface_attacker", "Загрузить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    interface_attacker = QtWidgets.QMainWindow()
    ui = Ui_interface_attacker()
    ui.setupUi(interface_attacker)
    interface_attacker.show()
    sys.exit(app.exec_())