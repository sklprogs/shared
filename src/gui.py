#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import PyQt6
import PyQt6.QtWidgets
from skl_shared_qt.localize import _


class Top(PyQt6.QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def add_widget(self, widget):
        self.layout.addWidget(widget)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_gui(self):
        self.widget = self
        self.layout = PyQt6.QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)



class Objects:

    def __init__(self):
        self.icon = self.screen = None
    
    def get_screen(self):
        if self.screen is None:
            self.screen = Screen()
        return self.screen
    
    def get_icon(self):
        if self.icon is None:
            self.icon = PyQt6.QtGui.QIcon(ICON)
        return self.icon



''' If there are issues with import or tkinter's wait_variable, put this
    beneath 'if __name__'.
'''
objs = Objects()


if __name__ == '__main__':
    objs.start()
    objs.end()
