#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6.QtWidgets


class Message(PyQt6.QtWidgets.QMessageBox):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def set_text(self, text):
        self.setText(text)
    
    def set_title(self, text):
        self.setWindowTitle(text)
