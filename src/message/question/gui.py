#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QMessageBox
from skl_shared.localize import _


class Message(QMessageBox):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
        
    def set_message(self, message):
        self.setText(message)
    
    def set_title(self):
        self.setWindowTitle(_('Question'))
        
    def set_icon(self):
        self.setIcon(QMessageBox.Icon.Question)
    
    def set_buttons(self):
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    
    def set_gui(self):
        self.set_title()
        self.set_icon()
        self.set_buttons()
    
    def show_blocked(self):
        if self.exec() == QMessageBox.StandardButton.Yes:
            return True


QUESTION = Message()
