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
        self.centralwidget = QtWidgets.QWidget(interface_admin)
        self.centralwidget.setObjectName("centralwidget")
        self.add_node_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_node_btn.setGeometry(QtCore.QRect(10, 50, 61, 51))
        self.add_node_btn.setObjectName("add_node_btn")
        self.send_btn = QtWidgets.QPushButton(self.centralwidget)
        self.send_btn.setGeometry(QtCore.QRect(0, 180, 71, 51))
        self.send_btn.setObjectName("send_btn")
        self.download_btn = QtWidgets.QPushButton(self.centralwidget)
        self.download_btn.setGeometry(QtCore.QRect(0, 290, 71, 31))
        self.download_btn.setObjectName("download_btn")
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
        self.add_node_btn.setText(_translate("interface_admin", "Добавить\n"
"узел"))
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
