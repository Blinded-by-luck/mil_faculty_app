# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.enter_defender_btn = QtWidgets.QPushButton(self.centralwidget)
        self.enter_defender_btn.setGeometry(QtCore.QRect(350, 260, 101, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enter_defender_btn.sizePolicy().hasHeightForWidth())
        self.enter_defender_btn.setSizePolicy(sizePolicy)
        self.enter_defender_btn.setObjectName("enter_defender_btn")
        self.enter_attacker_btn = QtWidgets.QPushButton(self.centralwidget)
        self.enter_attacker_btn.setGeometry(QtCore.QRect(350, 200, 101, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enter_attacker_btn.sizePolicy().hasHeightForWidth())
        self.enter_attacker_btn.setSizePolicy(sizePolicy)
        self.enter_attacker_btn.setObjectName("enter_attacker_btn")
        self.enter_lbl = QtWidgets.QLabel(self.centralwidget)
        self.enter_lbl.setGeometry(QtCore.QRect(370, 110, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enter_lbl.sizePolicy().hasHeightForWidth())
        self.enter_lbl.setSizePolicy(sizePolicy)
        self.enter_lbl.setObjectName("enter_lbl")
        self.enter_admin_btn = QtWidgets.QPushButton(self.centralwidget)
        self.enter_admin_btn.setGeometry(QtCore.QRect(350, 140, 101, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enter_admin_btn.sizePolicy().hasHeightForWidth())
        self.enter_admin_btn.setSizePolicy(sizePolicy)
        self.enter_admin_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.enter_admin_btn.setObjectName("enter_admin_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Project"))
        self.enter_defender_btn.setText(_translate("MainWindow", "Защитник"))
        self.enter_attacker_btn.setText(_translate("MainWindow", "Нападающий"))
        self.enter_lbl.setText(_translate("MainWindow", "Войти как:"))
        self.enter_admin_btn.setText(_translate("MainWindow", "Администратор"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
