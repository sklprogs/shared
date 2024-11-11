#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import PyQt6
import PyQt6.QtWidgets
from skl_shared_qt.localize import _


ICON = ''


class Screen:
    
    def __init__(self):
        self.screen = sh.objs.get_root().primaryScreen().size()
    
    def get_width(self):
        return self.screen.width()
    
    def get_height(self):
        return self.screen.height()



class Debug(PyQt6.QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(objs.get_icon())
    
    def centralize(self):
        self.move(objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def fill(self, text):
        self.textbox.clear()
        self.cursor.insertText(text, self.char_fmt)
        self.textbox.moveCursor(self.cursor.MoveOperation.Start)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def set_layout(self):
        self.layout_ = PyQt6.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
    
    def set_gui(self):
        self.set_layout()
        self.textbox = PyQt6.QtWidgets.QTextEdit()
        self.doc = PyQt6.QtGui.QTextDocument()
        self.cursor = PyQt6.QtGui.QTextCursor(self.doc)
        self.char_fmt = self.cursor.charFormat()
        self.textbox.setDocument(self.doc)
        self.textbox.setReadOnly(True)
        self.font = PyQt6.QtGui.QFont('Mono', 11)
        self.char_fmt.setFont(self.font)
        self.layout_.addWidget(self.textbox)
        self.setLayout(self.layout_)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def show_maximized(self):
        self.showMaximized()



class FileDialog:
    
    def __init__(self, parent=None):
        #NOTE: A widget is required here, not a wrapper
        self.parent = parent
    
    def set_icon(self):
        self.parent.setWindowIcon(objs.get_icon())
    
    def set_parent(self):
        if not self.parent:
            self.parent = PyQt6.QtWidgets.QWidget()
    
    def save(self, caption, folder, filter_):
        # Empty output is ('', '')
        return PyQt6.QtWidgets.QFileDialog.getSaveFileName (parent = self.parent
                                                           ,caption = caption
                                                           ,directory = folder
                                                           ,filter = filter_
                                                           )[0]



class Top(PyQt6.QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def add_widget(self, widget):
        self.layout.addWidget(widget)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_gui(self):
        self.widget = self
        self.layout = PyQt6.QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)



class OptionMenu:
    
    def __init__(self):
        self.widget = PyQt6.QtWidgets.QComboBox()
    
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
        self.widget.setFont(PyQt6.QtGui.QFont(family, size))
    
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
