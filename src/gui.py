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



class Button:
    
    def __init__ (self, text='', action=None, parent=None, width=36, height=36
                 ,hint='' ,active='', inactive=''
                 ):
        self.parent = parent
        self.text = text
        self.action = action
        self.width = width
        self.height = height
        self.hint = hint
        self.active = active
        self.icon = self.inactive = inactive
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
    
    def set_default(self, Default=True):
        self.widget.setAutoDefault(Default)
    
    def activate(self):
        if self.icon == self.inactive:
            self.icon = self.active
            self.set_icon()

    def inactivate(self):
        if self.icon == self.active:
            self.icon = self.inactive
            self.set_icon()
    
    def set_hint(self):
        if self.hint:
            self.widget.setToolTip(self.hint)
    
    def resize(self):
        self.widget.resize(self.width, self.height)
    
    def set_icon(self):
        ''' Setting a button image with
            button.setStyleSheet('image: url({})'.format(path)) causes
            tooltip glitches.
        '''
        if self.icon:
            self.widget.setIcon(PyQt6.QtGui.QIcon(self.icon))
    
    def set_size(self):
        if self.width and self.height:
            self.widget.setIconSize(PyQt6.QtCore.QSize(self.width, self.height))
    
    def set_border(self):
        if self.icon:
            self.widget.setStyleSheet('border: 0px')
    
    def set_action(self, action=None):
        if action:
            self.action = action
        if self.action:
            self.widget.clicked.connect(self.action)
    
    def set_gui(self):
        self.widget = PyQt6.QtWidgets.QPushButton(self.text, self.parent)
        self.resize()
        self.set_icon()
        self.set_size()
        #FIX: this may cause the button to not show itself in complex widgets
        self.set_border()
        self.set_hint()
        self.set_action()



class Objects:

    def __init__(self):
        self.root = self.warning = self.error = self.question \
                  = self.info = self.entry = self.icon = self.screen = None
    
    def get_screen(self):
        if self.screen is None:
            self.screen = Screen()
        return self.screen
    
    def get_icon(self):
        if self.icon is None:
            self.icon = PyQt6.QtGui.QIcon(ICON)
        return self.icon
    
    def get_root(self):
        if self.root is None:
            self.root = PyQt6.QtWidgets.QApplication(sys.argv)
        return self.root

    def start(self):
        self.get_root()

    def end(self):
        sys.exit(self.root.exec())

    def get_warning(self):
        if self.warning is None:
            self.warning = Message().get_warning()
        return self.warning

    def get_error(self):
        if self.error is None:
            self.error = Message().get_error()
        return self.error

    def get_question(self):
        if self.question is None:
            self.question = Message().get_question()
        return self.question

    def get_info(self):
        if self.info is None:
            self.info = Message().get_info()
        return self.info



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
        self.widget = PyQt6.QtWidgets.QCheckBox()
    
    def set_font(self, family, size):
        self.widget.setFont(PyQt6.QtGui.QFont(family, size))
    
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



''' If there are issues with import or tkinter's wait_variable, put this
    beneath 'if __name__'.
'''
objs = Objects()


if __name__ == '__main__':
    objs.start()
    objs.end()
