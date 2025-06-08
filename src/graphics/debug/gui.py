#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QTextDocument, QTextCursor, QFont, QShortcut, QKeySequence
from skl_shared.graphics.root.controller import ROOT


class Debug(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def centralize(self):
        self.move(ROOT.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def fill(self, text):
        self.textbox.clear()
        self.cursor.insertText(text, self.char_fmt)
        self.textbox.moveCursor(self.cursor.MoveOperation.Start)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def set_layout(self):
        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
    
    def set_gui(self):
        self.set_layout()
        self.textbox = QTextEdit()
        self.doc = QTextDocument()
        self.cursor = QTextCursor(self.doc)
        self.char_fmt = self.cursor.charFormat()
        self.textbox.setDocument(self.doc)
        self.textbox.setReadOnly(True)
        self.font = QFont('Mono', 11)
        self.char_fmt.setFont(self.font)
        self.layout_.addWidget(self.textbox)
        self.setLayout(self.layout_)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def show_maximized(self):
        self.showMaximized()
