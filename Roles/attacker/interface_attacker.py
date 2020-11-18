import sys

from PyQt5 import QtWidgets, QtCore
import pickle

from PyQt5.QtWidgets import QFileDialog

from Roles.attacker import design_attacker
from gui_lib.Arc import Arc
from gui_lib.Canvas import Custom_line, Custom_label, Canvas, CANVAS_WORKING_MODE
from gui_lib.Net import Net
from gui_lib.Nodes import Node


class Attacker(QtWidgets.QMainWindow, design_attacker.Ui_interface_attacker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 450)
        self.canvas = Canvas(self.centralwidget, self, CANVAS_WORKING_MODE.GAME)
        # ???
        self.canvas.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.canvas.net = Net({}, {}, {}, {}, {})

        # Сделать не через абсолютные координаты
        self.canvas.setGeometry(QtCore.QRect(180, 70, 600, 450))
        self.canvas.setScene(self.scene)

        # Привязка событий нажатия
        self.download_btn.clicked.connect(self.download_btn_click)


    def download_btn_click(self):
        # отлов исключений
        self.canvas.reset_temp_data()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Special Files (*.mlbin)", options=options)
        if file_name:
            with open(file_name, 'rb') as file:
                Node.reset_counter()
                Arc.reset_counter()
                self.canvas.net = pickle.load(file)
                self.scene.clear()
                for key_node in self.canvas.net.nodes:
                    node = self.canvas.net.nodes[key_node]
                    pixmap = self.canvas.get_appropriate_pixmap(node)
                    custom_label = Custom_label(pixmap=pixmap, canvas=self.canvas, model_item=node)
                    self.canvas.scene().addWidget(custom_label)

                for key_arc in self.canvas.net.arcs:
                    arc = self.canvas.net.arcs[key_arc]
                    custom_line = Custom_line(canvas=self.canvas, model_item=arc,
                                              x1=arc.node_from.x, y1=arc.node_from.y,
                                              x2=arc.node_to.x, y2=arc.node_to.y)
                    self.canvas.scene().addItem(custom_line)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Attacker()
    application.show()
    sys.exit(app.exec())
