#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.graphics.debug.gui import Debug as guiDebug


class Debug:

    def __init__(self, func='__main__', mes=''):
        self.set_gui()
        if mes:
            self.reset(func, mes)
    
    def reset(self, func, mes):
        self.set_title(func)
        self.fill(mes)
    
    def set_gui(self):
        self.gui = guiDebug()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind(('Escape',), self.close)
    
    def fill(self, text):
        self.gui.fill(text)
    
    def set_title(self, title):
        self.gui.set_title(title)
    
    def show(self):
        self.gui.show_maximized()
    
    def close(self):
        self.gui.close()


DEBUG = Debug()
