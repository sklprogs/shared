#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtGui import QFont


class CheckBox:
    
    def __init__(self):
        self.set_gui()
    
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
        self.widget = QCheckBox()
    
    def set_font(self, family, size):
        self.widget.setFont(QFont(family, size))
    
    def get(self):
        return self.widget.isChecked()
    
    def enable(self):
        self.widget.setChecked(True)
    
    def disable(self):
        self.widget.setChecked(False)
    
    def toggle(self):
        if self.get():
            self.disable()
        else:
            self.enable()
    
    def set_text(self, text=''):
        if text:
            self.widget.setText(text)
