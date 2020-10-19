from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QBrush
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QLabel
from enum import Enum

from gui_lib.Nodes import Computer
from gui_lib.Nodes import Router
from gui_lib.Nodes import Commutator
from gui_lib.Nodes import Node

# По мере разработки сюда надо добавлять состояния
class LEFT_MOUSE_BTN_MODE(Enum):
    CHOOSE = 0
    ADD_COMPUTER = 1
    ADD_ROUTER = 2
    ADD_COMMUTATOR = 3


left_mouse_btn_mode = LEFT_MOUSE_BTN_MODE.CHOOSE


def get_left_mouse_btn_mode():
    return left_mouse_btn_mode


def set_left_mouse_btn_mode(value):
    global left_mouse_btn_mode
    left_mouse_btn_mode = value

class Custom_label(QLabel):

    def __init__(self, pixmap, canvas):
        super().__init__()
        self.setPixmap(pixmap)
        self.canvas = canvas
        self.node = None
        self.is_select = False
        self.setStyleSheet("background:transparent")

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.CHOOSE:
                if not self.is_select:
                    self.canvas.make_selected(self)
                    print("Custom_label selected")
                event.accept()
        if event.button() == Qt.RightButton:
            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.CHOOSE:
                if self.is_select:
                    self.canvas.unselect_and_remove_figure(self)
                    print("Custom_label unselected")
                event.accept()


class Canvas(QGraphicsView):

    def make_selected(self, figure):
        figure.is_select = True
        if isinstance(figure, Custom_label):
            if isinstance(figure.node, Computer):
                figure.setPixmap(self.selected_computer_pixmap)
            else:
                if isinstance(figure.node, Router):
                    figure.setPixmap(self.selected_router_pixmap)
                else:
                    if isinstance(figure.node, Commutator):
                        figure.setPixmap(self.selected_commutator_pixmap)
                    else:
                        print("Error in nested if make_selected")
            self.selected_figures[figure.node.id] = figure
        else:
            # обработка ребер, -id ребра
            pass

    def unselect_figure(self, figure):
        figure.is_select = False
        if isinstance(figure, Custom_label):
            if isinstance(figure.node, Computer):
                figure.setPixmap(self.computer_pixmap)
            else:
                if isinstance(figure.node, Router):
                    figure.setPixmap(self.router_pixmap)
                else:
                    if isinstance(figure.node, Commutator):
                        figure.setPixmap(self.commutator_pixmap)
                    else:
                        print("Error in nested if unselect_figure")
        else:
            # обработка ребер, -id ребра
            pass

    def unselect_and_remove_figure(self, figure):
        self.unselect_figure(figure)
        self.selected_figures.pop(figure.node.id)

    def unselect_all_figures(self):
        for key_figure in self.selected_figures:
            self.unselect_figure(self.selected_figures[key_figure])
        self.selected_figures.clear()

    def __init__(self, parent=None, root=None):
        QGraphicsView.__init__(self, parent=parent)
        self.interface_admin = root
        # Бросать ошибку, если нет файлов
        self.computer_pixmap = QPixmap('Models\\Computer.png')
        self.router_pixmap = QPixmap('Models\\Router.png')
        self.commutator_pixmap = QPixmap('Models\\Commutator.png')
        self.selected_computer_pixmap = QPixmap('Models\\Selected_computer.png')
        self.selected_router_pixmap = QPixmap('Models\\Selected_router.png')
        self.selected_commutator_pixmap = QPixmap('Models\\Selected_commutator.png')
        if self.computer_pixmap.isNull():
            print('computer_pixmap is null')
        self.selected_figures = {}

    def place_node(self, pixmap, x, y):
        custom_label = Custom_label(pixmap, self)
        self.scene().addWidget(custom_label)
        size = custom_label.pixmap().size()
        custom_label.setGeometry(x - size.width() / 2, y - size.height() / 2, size.width(), size.height())
        return custom_label

    def place_computer(self, pixmap, x, y):
        custom_label = self.place_node(pixmap, x, y)
        # custom_pixmap_item = Custom_pixmap_item(pixmap_item)
        # custom_pixmap_item.setBrush(Qt.yellow)
        # pixmap_item.mousePressEvent(self.mouse_press_computer)
        return custom_label

    def place_router(self, pixmap, x, y):
        custom_label = self.place_node(pixmap, x, y)
        #pixmap_item.mousePressEvent()
        return custom_label

    def place_commutator(self, pixmap, x, y):
        custom_label = self.place_node(pixmap, x, y)
        #pixmap_item.mousePressEvent()
        return custom_label

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            if (get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.CHOOSE) & (not event.isAccepted()):
                print("Event from canvas")
                return
            # print('count nodes before =', len(self.interface_admin.net.nodes))
            # print('Node.Counter before =', Node.Counter)
            point = self.mapToScene(event.pos())
            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_COMPUTER:
                pixmap = self.computer_pixmap
                custom_label = self.place_computer(pixmap, point.x(), point.y())
                node = Computer(custom_label.x(), custom_label.y(), [], [], custom_label)
                self.interface_admin.net.add_node(node)
                return

            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_ROUTER:
                pixmap = self.router_pixmap
                pixmap_item = self.place_router(pixmap, point.x(), point.y())
                node = Router(pixmap_item.x(), pixmap_item.y(), [], [], pixmap_item)
                self.interface_admin.net.add_node(node)
                return

            if get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.ADD_COMMUTATOR:
                pixmap = self.commutator_pixmap
                pixmap_item = self.place_commutator(pixmap, point.x(), point.y())
                node = Commutator(pixmap_item.x(), pixmap_item.y(), [], [], pixmap_item)
                self.interface_admin.net.add_node(node)
                return
        if event.button() == Qt.RightButton:
            # если что расписать подробнее
            if get_left_mouse_btn_mode() != LEFT_MOUSE_BTN_MODE.CHOOSE:
                self.interface_admin.enable_buttons()
                set_left_mouse_btn_mode(LEFT_MOUSE_BTN_MODE.CHOOSE)
                return
            if (get_left_mouse_btn_mode() == LEFT_MOUSE_BTN_MODE.CHOOSE) & (not event.isAccepted()):
                self.unselect_all_figures()
