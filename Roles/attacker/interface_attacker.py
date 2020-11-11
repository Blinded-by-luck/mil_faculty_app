from PyQt5 import QtWidgets
import pickle

from Roles.attacker import design_attacker
from gui_lib.Arc import Arc
from gui_lib.Canvas import Custom_line, Custom_label
from gui_lib.Nodes import Node


class Interface_attacker(QtWidgets.QMainWindow, design_attacker.Ui_interface_attacker):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()



