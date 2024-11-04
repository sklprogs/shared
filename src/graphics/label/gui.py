#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont


class Label:
    
    def __init__(self):
        self.set_gui()
    
    def set_action(self, action=None):
        if action:
            self.action = action
        if self.action:
            self.widget.mousePressEvent = self.action
    
    def get_font_size(self):
        size = self.widget.font().pointSize()
        # We will get -1 if the font size was specified in pixels
        if size > 0:
            return size
    
    def set_font_size(self, size):
        qfont = self.widget.font()
        qfont.setPointSize(size)
        self.widget.setFont(qfont)
    
    def set_gui(self):
        self.widget = QLabel()
    
    def set_text(self, text):
        self.widget.setText(text)
    
    def set_font(self, family, size):
        self.widget.setFont(QFont(family, size))
