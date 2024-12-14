#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QProgressBar, QVBoxLayout

from skl_shared_qt.localize import _
from skl_shared_qt.graphics.label.controller import Label


class ProgressBar:
    
    def __init__(self):
        self.set_gui()
    
    def set_widgets(self):
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.widget = QProgressBar(self.window)
        self.label = Label(_('Details'))
    
    def add_widgets(self):
        self.window.setLayout(self.layout)
        self.layout.addWidget(self.label.widget)
        self.layout.addWidget(self.widget)
    
    def configure(self):
        self.label.change_font_size(2)
        self.window.setFixedWidth(300)
        self.widget.setValue(0)
    
    def set_gui(self):
        self.set_widgets()
        self.add_widgets()
        self.configure()
    
    def set_title(self, title):
        self.window.setWindowTitle(title)
    
    def set_info(self, info):
        self.label.set_text(info)
    
    def show(self):
        self.window.show()
    
    def close(self):
        self.window.close()
