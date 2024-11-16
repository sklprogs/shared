#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import PyQt6
import PyQt6.QtWidgets
from skl_shared_qt.localize import _


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
