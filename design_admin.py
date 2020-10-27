# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_admin.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_interface_admin(object):
    def setupUi(self, interface_admin):
        interface_admin.setObjectName("interface_admin")
        interface_admin.resize(800, 600)
        interface_admin.setMinimumSize(QtCore.QSize(800, 600))
        interface_admin.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(interface_admin)
        self.centralwidget.setObjectName("centralwidget")
        self.add_computer_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_computer_btn.setGeometry(QtCore.QRect(0, 80, 41, 31))
        self.add_computer_btn.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.add_computer_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Models/Computer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_computer_btn.setIcon(icon)
        self.add_computer_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_computer_btn.setObjectName("add_computer_btn")
        self.send_btn = QtWidgets.QPushButton(self.centralwidget)
        self.send_btn.setGeometry(QtCore.QRect(0, 370, 71, 51))
        self.send_btn.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.send_btn.setObjectName("send_btn")
        self.download_btn = QtWidgets.QPushButton(self.centralwidget)
        self.download_btn.setGeometry(QtCore.QRect(0, 430, 71, 51))
        self.download_btn.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.download_btn.setObjectName("download_btn")
        self.add_router_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_router_btn.setGeometry(QtCore.QRect(0, 110, 41, 31))
        self.add_router_btn.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.add_router_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Models/Router.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_router_btn.setIcon(icon1)
        self.add_router_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_router_btn.setObjectName("add_router_btn")
        self.add_commutator_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_commutator_btn.setGeometry(QtCore.QRect(0, 140, 41, 31))
        self.add_commutator_btn.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.add_commutator_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Models/Commutator.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_commutator_btn.setIcon(icon2)
        self.add_commutator_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_commutator_btn.setObjectName("add_commutator_btn")
        self.add_arc_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_arc_btn.setGeometry(QtCore.QRect(0, 170, 41, 31))
        self.add_arc_btn.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.add_arc_btn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../Models/Arc.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_arc_btn.setIcon(icon3)
        self.add_arc_btn.setIconSize(QtCore.QSize(32, 32))
        self.add_arc_btn.setObjectName("add_arc_btn")
        interface_admin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(interface_admin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        interface_admin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(interface_admin)
        self.statusbar.setObjectName("statusbar")
        interface_admin.setStatusBar(self.statusbar)

        self.retranslateUi(interface_admin)
        QtCore.QMetaObject.connectSlotsByName(interface_admin)

    def retranslateUi(self, interface_admin):
        _translate = QtCore.QCoreApplication.translate
        interface_admin.setWindowTitle(_translate("interface_admin", "Project"))
        self.send_btn.setText(_translate("interface_admin", "Отправить"))
        self.download_btn.setText(_translate("interface_admin", "Загрузить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    interface_admin = QtWidgets.QMainWindow()
    ui = Ui_interface_admin()
    ui.setupUi(interface_admin)
    interface_admin.show()
    sys.exit(app.exec_())
