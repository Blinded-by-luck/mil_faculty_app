import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
import design_menu  # Это наш конвертированный файл дизайна
from gui_lib.Net import Net
from interface_admin import Interface_admin
from gui_lib.Canvas import Canvas, CANVAS_WORKING_MODE
from interface_attacker import Interface_attacker


class Interface_menu(QtWidgets.QMainWindow, design_menu.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.enter_admin_btn.clicked.connect(self.enter_admin_btn_click)
        self.enter_attacker_btn.clicked.connect(self.enter_attacker_btn_click)

    def enter_admin_btn_click(self):
        self.admin_window = QtWidgets.QMainWindow()
        self.interface_attacker = Interface_admin()
        self.interface_attacker.setupUi(self.admin_window)

        # Продолжение конструктора Interface_admin
        self.interface_attacker.scene = QtWidgets.QGraphicsScene()
        self.interface_attacker.scene.setSceneRect(0, 0, 600, 450)
        self.interface_attacker.canvas = Canvas(self.interface_attacker.centralwidget, self.interface_attacker, CANVAS_WORKING_MODE.EDIT)
        self.interface_attacker.canvas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.interface_attacker.canvas.net = Net({}, {}, {}, {}, {})

        # Сделать не через абсолютные координаты
        self.interface_attacker.canvas.setGeometry(QtCore.QRect(180, 70, 600, 450))
        self.interface_attacker.canvas.setScene(self.interface_attacker.scene)

        # Привязка событий нажатия
        self.interface_attacker.add_computer_btn.clicked.connect(self.interface_attacker.add_computer_btn_click)
        self.interface_attacker.add_router_btn.clicked.connect(self.interface_attacker.add_router_btn_click)
        self.interface_attacker.add_commutator_btn.clicked.connect(self.interface_attacker.add_commutator_btn_click)
        self.interface_attacker.send_btn.clicked.connect(self.interface_attacker.send_btn_click)
        self.interface_attacker.download_btn.clicked.connect(self.interface_attacker.download_btn_click)
        self.interface_attacker.add_arc_btn.clicked.connect(self.interface_attacker.add_arc_btn_click)
        # конец

        #
        self.admin_window.show()
        print('Admin_click')
        self.close()

    def enter_attacker_btn_click(self):
        self.admin_window = QtWidgets.QMainWindow()
        self.interface_attacker = Interface_attacker()
        self.interface_attacker.setupUi(self.admin_window)

        # Продолжение конструктора Interface_attacker
        self.interface_attacker.scene = QtWidgets.QGraphicsScene()
        self.interface_attacker.scene.setSceneRect(0, 0, 600, 450)
        self.interface_attacker.canvas = Canvas(self.interface_attacker.centralwidget, self.interface_attacker, CANVAS_WORKING_MODE.GAME)
        # переопределить методы нажатия
        self.interface_attacker.canvas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.interface_attacker.canvas.net = Net({}, {}, {}, {}, {})

        # Сделать не через абсолютные координаты
        self.interface_attacker.canvas.setGeometry(QtCore.QRect(180, 70, 600, 450))
        self.interface_attacker.canvas.setScene(self.interface_attacker.scene)

        # Привязка событий нажатия
        self.interface_attacker.download_btn.clicked.connect(self.interface_attacker.download_btn_click)
        # конец

        #
        self.admin_window.show()
        print('Attacker_click')
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Interface_menu()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
