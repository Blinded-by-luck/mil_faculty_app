import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design_menu  # Это наш конвертированный файл дизайна
from interface_admin import Interface_admin

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
        # Обработчики нажатия надо прикреплять здесь
        self.interface_admin.add_node_btn.clicked.connect(self.interface_admin.add_node_btn_click)
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
