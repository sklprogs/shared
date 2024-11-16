#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QComboBox
from PyQt6.QtGui import QFont


class OptionMenu:
    
    def __init__(self):
        self.widget = QComboBox()
    
    def get_font_size(self):
        size = self.widget.font().pointSize()
        # We will get -1 if the font size was specified in pixels
        if size > 0:
            return size
    
    def set_font_size(self, size):
        qfont = self.widget.font()
        qfont.setPointSize(size)
        self.widget.setFont(qfont)
    
    def set_font(self, family, size):
        self.widget.setFont(QFont(family, size))
    
    def enable(self):
        self.widget.setEnabled(True)
    
    def disable(self):
        self.widget.setEnabled(False)
        
    def set(self, item):
        self.widget.setCurrentText(item)
    
    def fill(self, items):
        self.widget.clear()
        self.widget.addItems(items)

    def get(self):
        return self.widget.currentText()
    
    def get_index(self):
        return self.widget.currentIndex()
    
    def set_index(self, index_):
        return self.widget.setCurrentIndex(index_)
