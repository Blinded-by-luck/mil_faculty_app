import os


from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPen, QColor, QFont
from PyQt5.QtWidgets import QGraphicsView, QLabel, QGraphicsLineItem
from enum import Enum

from gui_lib.Arc import Arc
from gui_lib.Net import Net
from gui_lib.Nodes import Computer
from gui_lib.Nodes import Router
from gui_lib.Nodes import Commutator
from gui_lib.Nodes import Node


# По мере разработки сюда надо добавлять состояния
class MOUSE_BTN_MODE(Enum):
    CHOOSE = 0
    ADD_COMPUTER = 1
    ADD_ROUTER = 2
    ADD_COMMUTATOR = 3
    ADD_ARC = 4


class CANVAS_WORKING_MODE(Enum):
    EDIT = 0
    GAME = 1


"""Класс для фронтенд представления ребер"""
class Custom_line(QGraphicsLineItem):
    dark_pen = QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
    orange = QColor(0xff, 0xa5, 0x00)
    orange_pen = QPen(orange, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    def __init__(self, canvas=None, model_item=None, x1=0, y1=0, x2=0, y2=0):
        super().__init__(x1, y1, x2, y2)
        self.canvas = canvas
        self.setPen(Custom_line.dark_pen)
        # Обратная ссылка на бекенд ребра
        self.model_item = model_item
        self.is_select = False
        # Расположение ребер позади узлов
        self.setZValue(-2)
        if self.model_item is not None:
            # Ссылка на себя для бекенда
            self.model_item.custom_line = self

    def mousePressEvent(self, event):
        if self.canvas.working_mode == CANVAS_WORKING_MODE.EDIT:
            super().mousePressEvent(event)
            print("event from custom_line")
            if event.button() == Qt.LeftButton:
                if self.canvas.mouse_btn_mode == MOUSE_BTN_MODE.CHOOSE:
                    if not self.is_select:
                        self.canvas.make_selected(self)
                        print("Custom_line selected")
                    event.accept()
            if event.button() == Qt.RightButton:
                if self.canvas.mouse_btn_mode == MOUSE_BTN_MODE.CHOOSE:
                    if self.is_select:
                        self.canvas.unselect_and_remove_figure(self)
                        print("Custom_line unselected")
                    event.accept()


"""Класс для фронтенд представления узлов"""
class Custom_label(QLabel):

    def __init__(self, pixmap=None, canvas=None, model_item=None):
        super().__init__()
        self.setPixmap(pixmap)
        self.canvas = canvas
        # Обратная ссылка на бекенд узла
        self.model_item = model_item
        self.is_select = False
        self.setStyleSheet("background:transparent")
        if self.model_item is not None:
            # Ссылка на себя для бекенда
            self.model_item.custom_widget = self
            # Отрисовка номера
            if pixmap is not None:
                self.setGeometry(self.model_item.x, self.model_item.y, pixmap.width(), pixmap.height())
                self.title = QLabel()
                self.title.setText(str(self.model_item.id))
                self.title.setGeometry(self.model_item.x + pixmap.width() / 2,
                                       self.model_item.y + pixmap.height() / 3.8, pixmap.width(), 10)
                self.title.setStyleSheet("background:transparent")
                self.title.setFont(QFont('Times New Roman', 10))

    def mousePressEvent(self, event):
        if self.canvas.working_mode == CANVAS_WORKING_MODE.EDIT:
            super().mousePressEvent(event)
            if event.button() == Qt.LeftButton:
                if self.canvas.mouse_btn_mode == MOUSE_BTN_MODE.CHOOSE:
                    if not self.is_select:
                        self.canvas.make_selected(self)
                        print("Custom_label selected")
                    event.accept()
                if self.canvas.mouse_btn_mode == MOUSE_BTN_MODE.ADD_ARC:
                    if self.canvas.node_from is None:
                        self.canvas.node_from = self.model_item
                        self.canvas.make_selected(self)
                    else:
                        self.canvas.node_to = self.model_item
                        self.canvas.make_selected(self)
                        arc = self.canvas.add_arc_to_model(self.canvas.node_from, self.canvas.node_to,
                                                           self.canvas.interface_window.current_room)
                        visual_arc = self.canvas.create_visual_arc(arc, False)
                        self.scene().addItem(visual_arc)
                        self.canvas.reset_temp_data()
            if event.button() == Qt.RightButton:
                if self.canvas.mouse_btn_mode == MOUSE_BTN_MODE.CHOOSE:
                    if self.is_select:
                        self.canvas.unselect_and_remove_figure(self)
                        print("Custom_label unselected")
                    event.accept()
        # Логика во время игры
        # if self.canvas.working_mode == CANVAS_WORKING_MODE.GAME:
        #     super().mousePressEvent(event)
        #     if event.button() == Qt.LeftButton:
        #         if not self.is_select:
        #             self.canvas.make_selected(self)
        #             print("Custom_label selected")
        #         event.accept()


"""Фронтенд сети"""
class Canvas(QGraphicsView):

    def __init__(self, parent=None, root=None, nets=None, canvas_working_mode=0):
        QGraphicsView.__init__(self, parent=parent)
        # Обратная ссылка на главное окно
        self.interface_window = root
        # TODO Массив сетей
        self.nets = nets
        self.mouse_btn_mode = MOUSE_BTN_MODE.CHOOSE
        self.working_mode = canvas_working_mode
        path = '..' + os.sep + '..' + os.sep + 'Models' + os.sep
        self.computer_pixmap = QPixmap(path + 'Computer.png')
        self.router_pixmap = QPixmap(path + 'Router.png')
        self.commutator_pixmap = QPixmap(path + 'Commutator.png')
        self.selected_computer_pixmap = QPixmap(path + 'Selected_computer.png')
        self.selected_router_pixmap = QPixmap(path + 'Selected_router.png')
        self.selected_commutator_pixmap = QPixmap(path + 'Selected_commutator.png')
        self.fired_computer_pixmap = QPixmap(path + 'Fired_computer.png')
        self.fired_router_pixmap = QPixmap(path + 'Fired_router.png')
        self.fired_commutator_pixmap = QPixmap(path + 'Fired_commutator.png')
        self.arc_pixmap = QPixmap(path + 'Arc.png')
        # Бросать ошибку, если нет файлов
        if self.computer_pixmap.isNull():
            print('computer_pixmap is null')
        self.selected_figures = {}
        # Переменные для вставки ребер
        self.node_from = None
        self.node_to = None

    def keyPressEvent(self, event):
        # super().keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            for key_figure in self.selected_figures:
                self.selected_figures[key_figure].model_item.delete()
                self.unselect_figure(self.selected_figures[key_figure])
            self.selected_figures.clear()
            self.reset_temp_data()
            print("Delete event")
            return

    def add_arc_to_model(self, node_from, node_to, net_idx=0):
        arc = Arc(node_from, node_to)
        self.nets[net_idx].arcs[arc.id] = arc
        return arc

    def create_visual_arc(self, arc, is_download):
        if is_download:
            x1 = arc.node_from.x
            y1 = arc.node_from.y
            x2 = arc.node_to.x
            y2 = arc.node_to.y
        else:
            x1 = self.node_from.x
            y1 = self.node_from.y
            x2 = self.node_to.x
            y2 = self.node_to.y
        return Custom_line(canvas=self, model_item=arc,
                           x1=x1 + self.computer_pixmap.width() / 2,
                           y1=y1 + self.computer_pixmap.height() / 2,
                           x2=x2 + self.computer_pixmap.width() / 2,
                           y2=y2 + self.computer_pixmap.height() / 2)

    def make_selected(self, figure):
        figure.is_select = True
        # Если узел
        if isinstance(figure, Custom_label):
            if isinstance(figure.model_item, Computer):
                if self.working_mode == CANVAS_WORKING_MODE.EDIT:
                    figure.setPixmap(self.selected_computer_pixmap)
                else:
                    figure.setPixmap(self.fired_computer_pixmap)
            elif isinstance(figure.model_item, Router):
                if self.working_mode == CANVAS_WORKING_MODE.EDIT:
                    figure.setPixmap(self.selected_router_pixmap)
                else:
                    figure.setPixmap(self.fired_router_pixmap)
            elif isinstance(figure.model_item, Commutator):
                if self.working_mode == CANVAS_WORKING_MODE.EDIT:
                    figure.setPixmap(self.selected_commutator_pixmap)
                else:
                    figure.setPixmap(self.fired_commutator_pixmap)
            else:
                print("Error in nested if make_selected")
        # Если ребро
        else:
            figure.setPen(Custom_line.orange_pen)
        self.selected_figures[figure.model_item.id] = figure

    def unselect_figure(self, figure):
        figure.is_select = False
        if isinstance(figure, Custom_label):
            pixmap = self.get_appropriate_pixmap(figure.model_item.__class__)
            figure.setPixmap(pixmap)
        else:
            figure.setPen(Custom_line.dark_pen)

    def unselect_and_remove_figure(self, figure):
        self.unselect_figure(figure)
        self.selected_figures.pop(figure.model_item.id)

    def unselect_all_figures(self):
        for key_figure in self.selected_figures:
            self.unselect_figure(self.selected_figures[key_figure])
        self.selected_figures.clear()

    def reset_temp_data(self):
        self.node_from = None
        self.node_to = None
        self.unselect_all_figures()

    def get_appropriate_pixmap(self, class_node):
        if class_node is Computer:
            return self.computer_pixmap
        elif class_node is Router:
            return self.router_pixmap
        elif class_node is Commutator:
            return self.commutator_pixmap
        return ValueError("Unrecognized class")

    def get_appropriate_fired_pixmap(self, class_node):
        if class_node is Computer:
            return self.fired_computer_pixmap
        elif class_node is Router:
            return self.fired_router_pixmap
        elif class_node is Commutator:
            return self.fired_commutator_pixmap
        return ValueError("Unrecognized class")

    @QtCore.pyqtSlot(int)
    def display_net(self, net_idx=0):
        self.reset_temp_data()
        Node.reset_counter()
        Arc.reset_counter()
        self.scene().clear()
        for key_node in self.nets[net_idx].nodes:
            node = self.nets[net_idx].nodes[key_node]
            pixmap = self.get_appropriate_pixmap(node.__class__)
            custom_label = Custom_label(pixmap=pixmap, canvas=self, model_item=node)
            self.scene().addWidget(custom_label)
            self.scene().addWidget(custom_label.title)

        for key_arc in self.nets[net_idx].arcs:
            arc = self.nets[net_idx].arcs[key_arc]
            custom_line = self.create_visual_arc(arc, True)
            self.scene().addItem(custom_line)

    @QtCore.pyqtSlot(Net, int)
    def download_net(self, net, net_idx=0):
        self.nets[net_idx] = net

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.working_mode == CANVAS_WORKING_MODE.EDIT:
            if event.button() == Qt.LeftButton:
                if (self.mouse_btn_mode == MOUSE_BTN_MODE.CHOOSE) & (not event.isAccepted()):
                    print("Event from canvas")
                    return
                point = self.mapToScene(event.pos())
                if self.mouse_btn_mode == MOUSE_BTN_MODE.ADD_COMPUTER:
                    node = Computer(point.x() - self.computer_pixmap.width() / 2,
                                    point.y() - self.computer_pixmap.height() / 2, ingoing_arcs=[], outgoing_arcs=[])
                    custom_label = Custom_label(pixmap=self.computer_pixmap, canvas=self, model_item=node)
                    self.nets[self.interface_window.current_room].add_node(node)
                    self.scene().addWidget(custom_label)
                    self.scene().addWidget(custom_label.title)
                    return

                if self.mouse_btn_mode == MOUSE_BTN_MODE.ADD_ROUTER:
                    node = Router(point.x() - self.router_pixmap.width() / 2,
                                  point.y() - self.router_pixmap.height() / 2, ingoing_arcs=[], outgoing_arcs=[])
                    custom_label = Custom_label(pixmap=self.router_pixmap, canvas=self, model_item=node)
                    self.nets[self.interface_window.current_room].add_node(node)
                    self.scene().addWidget(custom_label)
                    self.scene().addWidget(custom_label.title)
                    return

                if self.mouse_btn_mode == MOUSE_BTN_MODE.ADD_COMMUTATOR:
                    node = Commutator(point.x() - self.commutator_pixmap.width() / 2,
                                      point.y() - self.commutator_pixmap.height() / 2, ingoing_arcs=[],
                                      outgoing_arcs=[])
                    custom_label = Custom_label(pixmap=self.commutator_pixmap, canvas=self, model_item=node)
                    self.nets[self.interface_window.current_room].add_node(node)
                    self.scene().addWidget(custom_label)
                    self.scene().addWidget(custom_label.title)
                    return
            if event.button() == Qt.RightButton:
                # Отмена выбора фигур
                if (self.mouse_btn_mode == MOUSE_BTN_MODE.CHOOSE) & (not event.isAccepted()):
                    self.reset_temp_data()
                    return
                if (self.mouse_btn_mode == MOUSE_BTN_MODE.ADD_ARC) & (self.node_from is not None):
                    self.reset_temp_data()
                    return
                # Отмена выбора фигур и переход в режим выбора
                if self.mouse_btn_mode != MOUSE_BTN_MODE.CHOOSE:
                    self.interface_window.enable_buttons()
                    self.mouse_btn_mode = MOUSE_BTN_MODE.CHOOSE
                    self.reset_temp_data()
                    return
