#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon


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
            self.widget.setIcon(QIcon(self.icon))
    
    def set_size(self):
        if self.width and self.height:
            self.widget.setIconSize(QSize(self.width, self.height))
    
    def set_border(self):
        if self.icon:
            self.widget.setStyleSheet('border: 0px')
    
    def set_action(self, action=None):
        if action:
            self.action = action
        if self.action:
            self.widget.clicked.connect(self.action)
    
    def set_gui(self):
        self.widget = QPushButton(self.text, self.parent)
        self.resize()
        self.set_icon()
        self.set_size()
        #FIX: this may cause the button to not show itself in complex widgets
        self.set_border()
        self.set_hint()
        self.set_action()
