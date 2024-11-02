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
        
    def set_icon(self, obj):
        self.setIcon(obj)
    
    def get_error(self):
        self.set_title(_('Error'))
        self.set_icon(PyQt6.QtWidgets.QMessageBox.Icon.Critical)
        return self
    
    def get_warning(self):
        self.set_title(_('Warning'))
        self.set_icon(PyQt6.QtWidgets.QMessageBox.Icon.Warning)
        return self
    
    def get_info(self):
        self.set_title(_('Info'))
        self.set_icon(PyQt6.QtWidgets.QMessageBox.Icon.Information)
        return self
    
    def get_debug(self):
        self.set_title(_('Debug'))
        self.set_icon(PyQt6.QtWidgets.QMessageBox.Icon.Information)
        return self
    
    def get_question(self):
        self.set_title(_('Question'))
        self.set_icon(PyQt6.QtWidgets.QMessageBox.Icon.Question)
        return self
