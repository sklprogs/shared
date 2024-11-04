#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QShortcut, QKeySequence


class Entry:
    
    def __init__(self, parent=None):
        self.parent = None
        self.set_gui()
    
    def go_start(self):
        self.widget.setCursorPosition(0)
    
    def select_all(self):
        self.widget.selectAll()
    
    def get_font_size(self):
        size = self.widget.font().pointSize()
        # We will get -1 if the font size was specified in pixels
        if size > 0:
            return size
    
    def set_font_size(self, size):
        qfont = self.widget.font()
        qfont.setPointSize(size)
        self.widget.setFont(qfont)
    
    def disable(self):
        self.widget.setEnabled(False)
    
    def enable(self):
        self.widget.setEnabled(True)
    
    def get_width(self):
        return self.widget.width()
    
    def get_root_y(self):
        return self.widget.frameGeometry().y()
    
    def get_x(self):
        return self.widget.pos().x()
    
    def set_min_width(self, width):
        self.widget.setMinimumWidth(width)
    
    def set_max_width(self, width):
        self.widget.setMaximumWidth(width)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self.widget).activated.connect(action)
    
    def set_gui(self):
        self.widget = QLineEdit(self.parent)
    
    def clear(self):
        self.widget.clear()
    
    def get(self):
        return self.widget.text()
    
    def insert(self, text):
        self.widget.insert(text)
    
    def set_text(self, text):
        self.widget.setText(text)
    
    def focus(self):
        self.widget.setFocus()
