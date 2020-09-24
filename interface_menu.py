import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
import design_menu  # Это наш конвертированный файл дизайна
from interface_admin import Interface_admin
from gui_lib import Canvas

class Interface_menu(QtWidgets.QMainWindow, design_menu.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.enter_admin_btn.clicked.connect(self.enter_admin_btn_click)

    def enter_admin_btn_click(self):
        self.admin_window = QtWidgets.QMainWindow()
        self.interface_admin = Interface_admin()
        self.interface_admin.setupUi(self.admin_window)

        # Продолжение конструктора Interface_admin
        self.interface_admin.scene = QtWidgets.QGraphicsScene()
        self.interface_admin.scene.setSceneRect(0, 0, 600, 450)
        self.interface_admin.canvas = Canvas(self.interface_admin.centralwidget, self.interface_admin)
        # Сделать не через абсолютные координаты
        self.interface_admin.canvas.setGeometry(QtCore.QRect(180, 70, 600, 450))
        self.interface_admin.canvas.setScene(self.interface_admin.scene)

        # Обработчики нажатия
        self.interface_admin.add_node_btn.clicked.connect(self.interface_admin.add_node_btn_click)
        # конец обработчиков события

        #
        self.admin_window.show()
        print('Admin_click')
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Interface_menu()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':
    main()
