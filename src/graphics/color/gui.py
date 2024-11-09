#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtGui import QColor

class Color:
    
    def __init__(self, color):
        ''' This accepts everything without exceptions - None, '', hex value,
            color name, even gibberish. Default color is black.
        '''
        self.qcolor = QColor(color)
    
    def get_hex(self):
        return self.qcolor.name()
    
    def modify(self, factor):
        darker = self.qcolor.darker(factor).name()
        lighter = self.qcolor.lighter(factor).name()
        return(darker, lighter)
